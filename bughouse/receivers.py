from ratings import rate_teams, rate_players 

def compute_game_ratings(sender, instance, created, raw, **kwargs):
    if not raw:
       rate_teams(instance)
       rate_players(instance)
