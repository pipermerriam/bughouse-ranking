import decimal

from django.conf import settings

from bughouse.ratings.engines.base import BaseRatingsEngine

from bughouse.models import (
    OVERALL_OVERALL,
)
from bughouse.ratings.utils import (
    win_probability_from_rating,
)


def rate_teams(game):
    """
    Given a game, compute the lifetime overally rating.
    """
    wt = game.winning_team
    lt = game.losing_team

    wtlr = wt.get_rating_at_datetime(game.created_at)
    ltlr = lt.get_rating_at_datetime(game.created_at)

    team_ratings = compute_team_ratings(wtlr, ltlr)

    new_wtr = wtlr + (team_ratings[0] * provisional_modifier(wt))
    wtr, _ = game.team_ratings.update_or_create(
        team=wt, defaults={'rating': new_wtr}
    )

    new_ltr = ltlr + (team_ratings[1] * provisional_modifier(lt))
    ltr, _ = game.team_ratings.update_or_create(
        team=lt, defaults={'rating': new_ltr}
    )

    return wtr, ltr


def provisional_modifier(player_or_team):
    """
    A multiplier applied to the first N games a player plays in an attempt to
    move them more quickly to their appropriate rating.

    # TODO: this should probably be removed at some point as it adds complexity
    # that isn't necessary in the long term.
    """
    if player_or_team.total_games < settings.ELO_PROVISIONAL_GAME_LIMIT:
        return settings.ELO_PROVISIONAL_GAME_MODIFIER
    else:
        return 1


def _rate_players(game, winner, winner_partner, loser, loser_partner):
    w_lr = winner.get_rating_at_datetime(game.created_at)
    wp_lr = winner_partner.get_rating_at_datetime(game.created_at)
    l_lr = loser.get_rating_at_datetime(game.created_at)
    lp_lr = loser_partner.get_rating_at_datetime(game.created_at)

    wp, wpp, lp, lpp = compute_individual_ratings(
        winner=w_lr,
        winner_partner=wp_lr,
        loser=l_lr,
        loser_partner=lp_lr,
    )

    new_wr = w_lr + (wp * provisional_modifier(winner))
    wr, _ = game.player_ratings.update_or_create(
        player=winner, key=OVERALL_OVERALL, defaults={'rating': new_wr}
    )
    new_wpr = wp_lr + (wpp * provisional_modifier(winner_partner))
    wpr, _ = game.player_ratings.update_or_create(
        player=winner_partner, key=OVERALL_OVERALL, defaults={'rating': new_wpr}
    )
    new_lr = l_lr + (lp * provisional_modifier(loser))
    lr, _ = game.player_ratings.update_or_create(
        player=loser, key=OVERALL_OVERALL, defaults={'rating': new_lr}
    )
    new_lpr = lp_lr + (lpp * provisional_modifier(loser_partner))
    lpr, _ = game.player_ratings.update_or_create(
        player=loser_partner, key=OVERALL_OVERALL, defaults={'rating': new_lpr}
    )

    return wr, wpr, lr, lpr


def rate_players(game):
    """
    Given a game, compute the lifetime ratings for the players involved.
    """
    wtw = game.winning_team.white_player
    wtb = game.winning_team.black_player
    ltw = game.losing_team.white_player
    ltb = game.losing_team.black_player
    lc = game.losing_color

    if lc == game.BLACK:
        wtwr, wtbr, ltbr, ltwr = _rate_players(
            game,
            wtw, wtb, ltb, ltw,
        )
    else:
        wtbr, wtwr, ltwr, ltbr = _rate_players(
            game,
            wtb, wtw, ltw, ltb,
        )

    return wtwr, wtbr, ltwr, ltbr


def weighted_rating(self_rating, partner_rating, self_weight=None, partner_weight=None):
    """
    Given a team, compute a player's weighted rating.
    """
    if self_weight is None:
        self_weight = settings.ELO_SELF_WEIGHT

    if partner_weight is None:
        partner_weight = settings.ELO_PARTNER_WEIGHT

    return (self_rating * self_weight) + (partner_rating * partner_weight)


def points_from_probability(probability_to_win, victory_condition_constant):
    return int(
        decimal.Decimal((1 - probability_to_win) * victory_condition_constant).quantize(
            decimal.Decimal('1'),
            rounding=decimal.ROUND_HALF_EVEN,
        )
    )


def compute_individual_ratings(winner, winner_partner, loser, loser_partner):
    w1_weighted = weighted_rating(winner_partner, winner)
    w2_weighted = weighted_rating(winner, winner_partner)
    l1_weighted = weighted_rating(loser_partner, loser)
    l2_weighted = weighted_rating(loser, loser_partner)

    w1_points = points_from_probability(
        win_probability_from_rating(l1_weighted, w1_weighted), settings.ELO_WIN_SELF,
    )
    w2_points = points_from_probability(
        win_probability_from_rating(l2_weighted, w2_weighted), settings.ELO_WIN_PARTNER,
    )
    l1_points = points_from_probability(
        1 - win_probability_from_rating(w1_weighted, l1_weighted), settings.ELO_LOSE_SELF,
    )
    l2_points = points_from_probability(
        1 - win_probability_from_rating(w2_weighted, l2_weighted), settings.ELO_LOSE_PARTNER,
    )

    return w1_points, w2_points, l1_points, l2_points


def compute_team_ratings(r_winning_team, r_losing_team):
    w_points = points_from_probability(
        win_probability_from_rating(r_winning_team, r_losing_team), settings.ELO_WIN_TEAM,
    )
    l_points = - w_points

    return w_points, l_points


class OverallPlayerRatings(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_players(game)


class OverallTeamRatings(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_teams(game)
