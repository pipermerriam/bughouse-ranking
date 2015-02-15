from django.conf import settings

from bughouse.models import EXPERIMENTAL_BATMAN
from bughouse.ratings.utils import round_it
from bughouse.ratings.engines.base import BaseRatingsEngine


def elo_chance_to_lose(player, other):
    """
    other_rank + 400 * (wins - losses)
    ----------------------------------
               games

    new = old + C * (score - expected)

    Probability = 1 / (1 + (10 ^ -((White Rating - Black Rating) / 400)))

    Black Adjustment = Int (-1 * (White Adjustment * Black's DeltaK / White's DeltaK))

    White Adjustment = Int (DeltaK * (Score - Probability) )

    1-0, score = 1.
    1/2-1/2, score = 0.5.
    0-1, score = 0.
    """
    diff = player - other
    return 1.0 / (1 + pow(10, (diff / 400.0)))


def adjust_ratings(player, opponent, partner, opponent_partner, scalar=3):
    """
    Adjust a player's ELO rating based on his partner matchup.
    """
    partner_probability = abs(0.5 - elo_chance_to_lose(
        opponent_partner,
        partner,
    ))
    partner_diff = partner - opponent_partner
    diff = (player + partner_diff * partner_probability * scalar) - opponent
    return round_it(opponent + diff)


def points_from_probability(probability_to_win, victory_condition_constant):
    return round_it(
        (1 - probability_to_win) * victory_condition_constant
    )


def compute_individual_ratings(winner, winner_partner, loser, loser_partner):
    w1_adjusted = adjust_ratings(winner, loser, winner_partner, loser_partner)
    w2_adjusted = adjust_ratings(winner_partner, loser_partner, winner, loser)
    l1_adjusted = adjust_ratings(loser, winner, loser_partner, winner_partner)
    l2_adjusted = adjust_ratings(loser_partner, winner_partner, loser, winner)

    w1_prob = 1 - elo_chance_to_lose(w1_adjusted, l1_adjusted)
    w2_prob = 1 - elo_chance_to_lose(w2_adjusted, l2_adjusted)
    l1_prob = elo_chance_to_lose(l1_adjusted, w1_adjusted)
    l2_prob = elo_chance_to_lose(l2_adjusted, w2_adjusted)

    w1_points = points_from_probability(w1_prob, settings.ELO_WIN_SELF)
    w2_points = points_from_probability(w2_prob, settings.ELO_WIN_PARTNER)
    l1_points = points_from_probability(l1_prob, settings.ELO_LOSE_SELF)
    l2_points = points_from_probability(l2_prob, settings.ELO_LOSE_PARTNER)

    # for debugger purposes.
    bases = (winner, winner_partner, loser, loser_partner)
    adjusted = (w1_adjusted, w2_adjusted, l1_adjusted, l2_adjusted)
    probs = (w1_prob, w2_prob, l1_prob, l2_prob)
    points = (w1_points, w2_points, l1_points, l2_points)

    return w1_points, w2_points, l1_points, l2_points


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

    wtw_lr = wtw.get_rating_at_datetime(game.created_at, key=EXPERIMENTAL_BATMAN)
    wtb_lr = wtb.get_rating_at_datetime(game.created_at, key=EXPERIMENTAL_BATMAN)
    ltw_lr = ltw.get_rating_at_datetime(game.created_at, key=EXPERIMENTAL_BATMAN)
    ltb_lr = ltb.get_rating_at_datetime(game.created_at, key=EXPERIMENTAL_BATMAN)

    if lc == game.BLACK:
        wtwp, wtbp, ltbp, ltwp = compute_individual_ratings(
            wtw_lr, wtb_lr, ltb_lr, ltw_lr,
        )
    else:
        wtbp, wtwp, ltwp, ltbp = compute_individual_ratings(
            wtb_lr, wtw_lr, ltw_lr, ltb_lr,
        )

    new_wtwr = wtw_lr + wtwp
    wtwr, _ = game.player_ratings.update_or_create(
        player=wtw, key=EXPERIMENTAL_BATMAN, defaults={'rating': new_wtwr}
    )
    new_wtbr = wtb_lr + wtbp
    wtbr, _ = game.player_ratings.update_or_create(
        player=wtb, key=EXPERIMENTAL_BATMAN, defaults={'rating': new_wtbr}
    )
    new_ltwr = ltw_lr + ltwp
    ltwr, _ = game.player_ratings.update_or_create(
        player=ltw, key=EXPERIMENTAL_BATMAN, defaults={'rating': new_ltwr}
    )
    new_ltbr = ltb_lr + ltbp
    ltbr, _ = game.player_ratings.update_or_create(
        player=ltb, key=EXPERIMENTAL_BATMAN, defaults={'rating': new_ltbr}
    )

    return wtwr, wtbr, ltwr, ltbr


class BatmanRatings(BaseRatingsEngine):
    def compute_ratings(self, game):
        rate_players(game)


#
#  Stuff for testing.
#
def pad(s):
    return "{0:>4}".format(s)


def report_it(a, b, c, d, e=False):
    pa = int(chance_of_loss(a, b, c, d) * 100)
    pb = int(abs(100 - pa))
    pd = int(chance_of_loss(d, c, b, a) * 100)
    pc = int(abs(100 - pd))

    ra = int(elo_chance_to_lose(a, b) * 100)
    rb = int(abs(100 - ra))
    rd = int(elo_chance_to_lose(d, c) * 100)
    rc = int(abs(100 - rd))

    print "-----------------------------------"
    print "| {pa}% ({ra}%)  |  {pc}% ({rc}%) |".format(
        pa=pad(pa), ra=pad(ra), pc=pad(pc), rc=pad(rc),
    )
    print "-----------------------------------"
    print "|      {aa}      |      {cc}      |".format(aa=pad(a), cc=pad(c))
    print "-----------------------------------"
    print "|       vs       |       vs       |"
    print "-----------------------------------"
    print "|      {bb}      |      {dd}      |".format(bb=pad(b), dd=pad(d))
    print "-----------------------------------"
    print "| {pb}% ({rb}%)  |  {pd}% ({rd}%) |".format(
        pb=pad(pb), rb=pad(rb), pd=pad(pd), rd=pad(rd),
    )
    print "-----------------------------------"
