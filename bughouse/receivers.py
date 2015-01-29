from ratings import rate_teams, rate_players 

def compute_game_ratings(sender, instance, created, raw, **kwargs):
    if raw:
       rate_teams(game)
       rate_players(game)
