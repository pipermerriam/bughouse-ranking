from django.conf import settings
import decimal 


def rate_teams(game):
   wt = game.winning_team
   lt = game.losing_team
   team_ratings = compute_team_ratings(wt.latest_rating, lt.latest_rating)

   wtr, _ = game.team_ratings.update_or_create(
       team = wt, **{'rating': 
           wt.latest_rating + (team_ratings[0] * provisional_modifier(wt))
           }
   )
   ltr, _ = game.team_ratings.update_or_create(
       team = lt, **{'rating': 
           lt.latest_rating + (team_ratings[1] * provisional_modifier(lt))
           }
        )

   return wtr, ltr 

def provisional_modifier(player_or_team):
    if player_or_team.total_games < settings.ELO_PROVISIONAL_GAME_LIMIT:
        return settings.ELO_PROVISIONAL_GAME_MODIFIER
    else:
        return 1

def rate_players(game):
    wtw = game.winning_team.white_player
    wtb = game.winning_team.black_player
    ltw = game.losing_team.white_player
    ltb = game.losing_team.black_player
    lc = game.losing_color

    if lc == game.BLACK:
        irs = compute_individual_ratings(wtw.latest_rating, wtb.latest_rating, ltb.latest_rating, ltw.latest_rating)
    
        wtwr, _ = game.player_ratings.update_or_create(
            player = wtw, **{'rating':
               wtw.latest_rating + (irs[0] * provisional_modifier(wtw))
               }
            )
        wtbr, _ = game.player_ratings.update_or_create(
            player = wtb, **{'rating':
               wtb.latest_rating + (irs[1] * provisional_modifier(wtb))
               }
            )
        ltwr, _ = game.player_ratings.update_or_create(
            player = ltw, **{'rating':
               ltw.latest_rating + (irs[3] * provisional_modifier(ltw))
               }
            )
        ltbr, _ = game.player_ratings.update_or_create(
            player = ltb, **{'rating':
               ltb.latest_rating + (irs[2] * provisional_modifier(ltb))
               }
            )

        return wtwr, wtbr, ltwr, ltbr
    
    else:
        irs = compute_individual_ratings(wtb.latest_rating, wtw.latest_rating, ltw.latest_rating, ltb.latest_rating)
        
        wtwr, _ = game.player_ratings.update_or_create(
            player = wtw, **{'rating':
               wtw.latest_rating + (irs[1] * provisional_modifier(wtw))
               }
            )
    
        wtbr, _ = game.player_ratings.update_or_create(
            player = wtb, **{'rating':
               wtb.latest_rating + (irs[0] * provisional_modifier(wtb))
               }
            )
        ltwr, _ = game.player_ratings.update_or_create(
            player = ltw, **{'rating':
               lwt.latest_rating + (irs[2] * provisional_modifier(ltw))
               }
            )
        
        ltbr, _ = game.player_ratings.update_or_create(
            player = ltb, **{'rating':
               ltb.latest_rating + (irs[3] * provisional_modifier(ltb))
               }
            )

        return wtwr, wtbr, ltwr, ltbr

def win_probability_from_rating(r1, r2):
    diff = r1 - r2
    return 1.0 / ( pow(10,( diff / 400.0)) +1.0)


def weighted_rating(self_rating, partner_rating, self_weight = None, partner_weight = None):
    if self_weight == None:
        self_weight = settings.ELO_SELF_WEIGHT
    
    if partner_weight == None:
        partner_weight = settings.ELO_PARTNER_WEIGHT
    
    return (self_rating * self_weight) + (partner_rating * partner_weight) 

def points_from_probability(probability_to_win, victory_condition_constant):
    return int(decimal.Decimal( (1 - probability_to_win) * victory_condition_constant).quantize(
            decimal.Decimal('1'),
            rounding=decimal.ROUND_HALF_EVEN,
        ))

def compute_individual_ratings(r_winner, r_winner_p, r_loser, r_loser_partner):
    w1_weighted = weighted_rating(r_winner_p, r_winner)
    w2_weighted = weighted_rating( r_winner,r_winner_p)
    l1_weighted = weighted_rating(r_loser_partner, r_loser)
    l2_weighted = weighted_rating(r_loser, r_loser_partner)

    w1_points = points_from_probability(win_probability_from_rating(l1_weighted, w1_weighted), settings.ELO_WIN_SELF)
    w2_points = points_from_probability(win_probability_from_rating(l2_weighted, w2_weighted), settings.ELO_WIN_PARTNER )
    l1_points = points_from_probability(1 - win_probability_from_rating(w1_weighted, l1_weighted), settings.ELO_LOSE_SELF)
    l2_points = points_from_probability(1 - win_probability_from_rating(w2_weighted, l2_weighted), settings.ELO_LOSE_PARTNER)

    return  w1_points,  w2_points,  l1_points,  l2_points

def compute_team_ratings(r_winning_team, r_losing_team):
    w_points = points_from_probability(win_probability_from_rating(r_winning_team, r_losing_team), settings.ELO_WIN_TEAM) 
    l_points = - w_points

    return  w_points,  l_points


