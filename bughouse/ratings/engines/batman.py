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


def chance_of_loss(player, other, partner, other_other, invert=False):
    """
    Given 4 ratings (white, white_opponent, black, black_opponent)

    return the probability that white will lose.

    if invert == True, return the probability that black will lose.
    """
    partner_probability = abs(0.5 - elo_chance_to_lose(
        other_other,
        partner,
    ))
    differential = partner - other_other
    diff = (player + differential * partner_probability * 4) - other
    if invert:
        print "Raw Probability", abs(1 - elo_chance_to_lose(player, other))
        return abs(1 - (1.0 / (pow(10, (diff / 400.0)) + 1.0)))
    else:
        print "Raw Probability", elo_chance_to_lose(player, other)
        return 1.0 / (pow(10, (diff / 400.0)) + 1.0)

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
    print "| {pa}% ({ra}%)  |  {pc}% ({rc}%) |".format(pa=pad(pa), ra=pad(ra), pc=pad(pc), rc=pad(rc))
    print "-----------------------------------"
    print "|      {aa}      |      {cc}      |".format(aa=pad(a), cc=pad(c))
    print "-----------------------------------"
    print "|       vs       |       vs       |"
    print "-----------------------------------"
    print "|      {bb}      |      {dd}      |".format(bb=pad(b), dd=pad(d))
    print "-----------------------------------"
    print "| {pb}% ({rb}%)  |  {pd}% ({rd}%) |".format(pb=pad(pb), rb=pad(rb), pd=pad(pd), rd=pad(rd))
    print "-----------------------------------"

def test_it():
    #report_it(1000, 1000, 1100, 900)
    #report_it(1000, 1000, 900, 1100)
    report_it(1050, 950, 900, 1100)
    report_it(1100, 900, 950, 1050, True)
    #report_it(1000, 1000, 100)
    #report_it(1000, 1000, -100)
    #report_it(1100, 900, 200)
    #report_it(1100, 900, -200)
    #report_it(1100, 900, 100)
    #report_it(1100, 900, -100)
    #report_it(900, 1100, 200)
    #report_it(900, 1100, -200)
    #report_it(900, 1100, 100)
    #report_it(900, 1100, -100)
