from bughouse.models import EXPERIMENTAL_BATMAN
from bughouse.ratings.utils import (
    round_it,
    elo_chance_to_lose,
)
from bughouse.ratings.engines.base import BaseRatingsEngine


def get_delta_k(rating):
    """
    DeltaK = 32 where the players rating <= 2100.
    DeltaK = 24 where the players rating > 2100 and < 2400.
    DeltaK = 16 where the players rating > 2400.
    """
    if rating <= 2100:
        return 32
    elif 2100 < rating <= 2400:
        return 24
    else:
        return 16


def adjust_rating(player, partner, opponent, opponent_partner, scalar=2):
    """
    Adjust a player's ELO rating based on his partner matchup.
    """
    partner_probability = abs(0.5 - elo_chance_to_lose(
        opponent_partner,
        partner,
    ))
    partner_diff = partner - opponent_partner
    adjusted_rating = player + (partner_diff * partner_probability * scalar)
    return round_it(adjusted_rating)


def compute_points(delta_k, outcome_probability, other=False):
    """
    - If the outcome was likely, then you receive fewer points.
    - If the outcome was unlikely, then you receive more points.
    """
    if other:
        scale = 0.9
    else:
        scale = 1
    return round_it(
        delta_k * (1 - outcome_probability) * scale
    )


def compute_individual_ratings(winner, winner_partner, loser, loser_partner):
    w1_adjusted = adjust_rating(winner, winner_partner, loser, loser_partner)
    w2_adjusted = adjust_rating(winner_partner, winner, loser_partner, loser)
    l1_adjusted = adjust_rating(loser, loser_partner, winner, winner_partner)
    l2_adjusted = adjust_rating(loser_partner, loser, winner_partner, winner)

    w1_dk = get_delta_k(w1_adjusted)
    w2_dk = get_delta_k(w2_adjusted)
    l1_dk = get_delta_k(l1_adjusted)
    l2_dk = get_delta_k(l2_adjusted)

    w1_outcome_prob = 1 - elo_chance_to_lose(w1_adjusted, l1_adjusted)
    w2_outcome_prob = 1 - elo_chance_to_lose(w2_adjusted, l2_adjusted)
    l1_outcome_prob = elo_chance_to_lose(l1_adjusted, w1_adjusted)
    l2_outcome_prob = elo_chance_to_lose(l2_adjusted, w2_adjusted)

    # if your chance to win is high and you win - small addition
    # if your chance to win is low and you win - large deduction
    w1_points = compute_points(w1_dk, w1_outcome_prob)
    w2_points = compute_points(w2_dk, w2_outcome_prob, True)
    # if your chance to lose was high and you lose - small deduction
    # if your chance to lose was low and you lose - large addition
    l1_points = -1 * compute_points(l1_dk, l1_outcome_prob)
    l2_points = -1 * compute_points(l2_dk, l2_outcome_prob, True)

    # for debugger purposes.
    bases = (winner, winner_partner, loser, loser_partner)
    adjusted = (w1_adjusted, w2_adjusted, l1_adjusted, l2_adjusted)
    probs = (w1_outcome_prob, w2_outcome_prob, l1_outcome_prob, l2_outcome_prob)
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
    rating_key = EXPERIMENTAL_BATMAN

    def compute_ratings(self, game):
        rate_players(game)

    def adjust_rating(self, player, player_partner, opponent, opponent_partner):
        return adjust_rating(player, player_partner, opponent, opponent_partner)


#
#  Stuff for testing.
#
def pad(s):
    return "{0:>4}".format(s)


def report_it(a, b, c, d, e=False):
    aa = round_it(adjust_ratings(a, b, c, d))
    ba = round_it(adjust_ratings(b, a, d, c))
    ca = round_it(adjust_ratings(c, d, a, b))
    da = round_it(adjust_ratings(d, c, b, a))

    pa = int(elo_chance_to_lose(aa, ba) * 100)
    pb = int(abs(100 - pa))
    pc = int(elo_chance_to_lose(ca, da) * 100)
    pd = int(abs(100 - pc))

    ra = int(elo_chance_to_lose(a, b) * 100)
    rb = int(abs(100 - ra))
    rc = int(elo_chance_to_lose(c, d) * 100)
    rd = int(abs(100 - rc))

    print "-----------------------------------"
    print "| {pa}% ({ra}%)  |  {pc}% ({rc}%) |".format(
        pa=pad(pa), ra=pad(ra), pc=pad(pc), rc=pad(rc),
    )
    print "-----------------------------------"
    print "| {aa}  ({oa})   | {cc}  ({oc})   |".format(aa=pad(aa), cc=pad(ca), oa=pad(a), oc=pad(c))
    print "-----------------------------------"
    print "|       vs       |       vs       |"
    print "-----------------------------------"
    print "| {bb}  ({ob})    | {dd}  ({od})  |".format(bb=pad(ba), dd=pad(da), ob=pad(b), od=pad(d))
    print "-----------------------------------"
    print "| {pb}% ({rb}%)  |  {pd}% ({rd}%) |".format(
        pb=pad(pb), rb=pad(rb), pd=pad(pd), rd=pad(rd),
    )
    print "-----------------------------------"
