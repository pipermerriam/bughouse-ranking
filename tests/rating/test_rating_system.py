from bughouse.ratings import rate_teams, rate_players

def test_rate_single_game(factories, models, elo_settings):
    game = factories.GameFactory()
    #team = factories.TeamFactory()
    #player = factories.PlayerFactory()

    #wtw = game.winning_team.white_player
    #ltb = game.losing_team.black_player

    #lc = game.losing_color
    #loss_type = game.loss_type

    #rating = models.TeamRating.objects.create(game = game, team = team, rating = 1000)
    #rating1 = models.PlayerRating.objects.create(game = game, player = player, rating = 1100)

    r1, r2 = rate_teams(game)
    assert r1.rating == 1008 
    assert r2.rating == 992


def test_rate_multiple_games(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()
    r1 = rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    r2 = rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    
    assert team_a.latest_rating == 1020
    assert team_b.latest_rating == 984 #976 

def test_provisional_limit(factories, models):
    team_a = factories.TeamFactory()
    team_b = factories.TeamFactory()
    
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    #rate_teams(factories.GameFactory(winning_team = team_a, losing_team = team_b))
    
    assert team_a.latest_rating == 1044 
    assert team_b.latest_rating == 968 


def test_individual_ratings(factories, models):
    # wtw = factories.PlayerFactory()
    #wtb = factories.PlayerFactory()
    #ltw = factories.PlayerFactory()
    #ltb = factories.PlayerFactory()
 
    game = factories.GameFactory()
    
    if game.losing_color == game.BLACK:    
        wtw, wtb, ltw, ltb = rate_players(game)
    
        assert wtw.player.latest_rating == 1012
        assert wtb.player.latest_rating == 1008 
        assert ltw.player.latest_rating == 992 
        assert ltb.player.latest_rating == 988 
    
    else:
        wtw, wtb, ltw, ltb = rate_players(game)
    
        assert wtw.player.latest_rating == 1008 
        assert wtb.player.latest_rating == 1012 
        assert ltw.player.latest_rating == 988
        assert ltb.player.latest_rating == 992 
