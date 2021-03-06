import decimal

from django.conf import settings

from bughouse.ratings.engines.base import BaseRatingsEngine

from bughouse.models import (
    WHITE,
    BLACK,
    OVERALL_OVERALL,
    OVERALL_WHITE,
    OVERALL_BLACK,
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

    wtlr = wt.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)
    ltlr = lt.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)

    wtp, ltp = compute_team_ratings(wtlr, ltlr)

    new_wtr = wtlr + (wtp * provisional_modifier(wt))
    wtr, _ = game.team_ratings.update_or_create(
        team=wt, key=OVERALL_OVERALL, defaults={'rating': new_wtr}
    )

    new_ltr = ltlr + (ltp * provisional_modifier(lt))
    ltr, _ = game.team_ratings.update_or_create(
        team=lt, key=OVERALL_OVERALL, defaults={'rating': new_ltr}
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


def compute_points_for_matchup(w_lr, wp_lr, l_lr, lp_lr):
    """
    This is a helper method.
    """
    wp, wpp, lp, lpp = compute_individual_ratings(
        winner=w_lr,
        winner_partner=wp_lr,
        loser=l_lr,
        loser_partner=lp_lr,
    )

    return wp, wpp, lp, lpp


def rate_players(game):
    """
    Given a game, compute the lifetime ratings for the players involved.
    """
    wtw = game.winning_team.white_player
    wtb = game.winning_team.black_player
    ltw = game.losing_team.white_player
    ltb = game.losing_team.black_player
    lc = game.losing_color

    wtw_lr = wtw.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)
    wtb_lr = wtb.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)
    ltw_lr = ltw.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)
    ltb_lr = ltb.get_rating_at_datetime(game.created_at, key=OVERALL_OVERALL)

    if lc == game.BLACK:
        wtwp, wtbp, ltbp, ltwp = compute_points_for_matchup(
            wtw_lr, wtb_lr, ltb_lr, ltw_lr,
        )
    else:
        wtbp, wtwp, ltwp, ltbp = compute_points_for_matchup(
            wtb_lr, wtw_lr, ltw_lr, ltb_lr,
        )

    new_wtwr = wtw_lr + (wtwp * provisional_modifier(wtw))
    wtwr, _ = game.player_ratings.update_or_create(
        player=wtw, key=OVERALL_OVERALL, defaults={'rating': new_wtwr}
    )
    new_wtbr = wtb_lr + (wtbp * provisional_modifier(wtb))
    wtbr, _ = game.player_ratings.update_or_create(
        player=wtb, key=OVERALL_OVERALL, defaults={'rating': new_wtbr}
    )
    new_ltwr = ltw_lr + (ltwp * provisional_modifier(ltw))
    ltwr, _ = game.player_ratings.update_or_create(
        player=ltw, key=OVERALL_OVERALL, defaults={'rating': new_ltwr}
    )
    new_ltbr = ltb_lr + (ltbp * provisional_modifier(ltb))
    ltbr, _ = game.player_ratings.update_or_create(
        player=ltb, key=OVERALL_OVERALL, defaults={'rating': new_ltbr}
    )

    return wtwr, wtbr, ltwr, ltbr


def rate_players_as_color(game, color):
    wtw = game.winning_team.white_player
    wtb = game.winning_team.black_player
    ltw = game.losing_team.white_player
    ltb = game.losing_team.black_player
    lc = game.losing_color

    if color == WHITE:
        key = OVERALL_WHITE
    elif color == BLACK:
        key = OVERALL_BLACK

    wtw_lr = wtw.get_rating_at_datetime(game.created_at, key=key)
    wtb_lr = wtb.get_rating_at_datetime(game.created_at, key=key)
    ltw_lr = ltw.get_rating_at_datetime(game.created_at, key=key)
    ltb_lr = ltb.get_rating_at_datetime(game.created_at, key=key)

    if lc == BLACK:
        wtwp, wtbp, ltbp, ltwp = compute_points_for_matchup(
            wtw_lr, wtb_lr, ltb_lr, ltw_lr,
        )
    else:
        wtbp, wtwp, ltwp, ltbp = compute_points_for_matchup(
            wtb_lr, wtw_lr, ltw_lr, ltb_lr,
        )

    if color == WHITE:
        new_wtwr = wtw_lr + (wtwp * provisional_modifier(wtw))
        wtwr, _ = game.player_ratings.update_or_create(
            player=wtw, key=OVERALL_WHITE, defaults={'rating': new_wtwr}
        )
        new_ltwr = ltw_lr + (ltwp * provisional_modifier(ltw))
        ltwr, _ = game.player_ratings.update_or_create(
            player=ltw, key=OVERALL_WHITE, defaults={'rating': new_ltwr}
        )
        return wtwr, ltwr
    elif color == BLACK:
        new_wtbr = wtb_lr + (wtbp * provisional_modifier(wtb))
        wtbr, _ = game.player_ratings.update_or_create(
            player=wtb, key=OVERALL_BLACK, defaults={'rating': new_wtbr}
        )
        new_ltbr = ltb_lr + (ltbp * provisional_modifier(ltb))
        ltbr, _ = game.player_ratings.update_or_create(
            player=ltb, key=OVERALL_BLACK, defaults={'rating': new_ltbr}
        )
        return wtbr, ltbr
    else:
        raise ValueError("Unknown Color")


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


class OverallPlayerRatingsAsWhite(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_players_as_color(game, color=WHITE)


class OverallPlayerRatingsAsBlack(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_players_as_color(game, color=BLACK)


class OverallTeamRatings(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_teams(game)
