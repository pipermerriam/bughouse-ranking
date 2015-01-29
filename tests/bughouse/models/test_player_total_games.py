def test_total_games(factories):
    player = factories.PlayerFactory()
    factories.GameFactory(winning_team__white_player=player)
    factories.GameFactory(winning_team__white_player=player)

    factories.GameFactory(winning_team__black_player=player)
    factories.GameFactory(winning_team__black_player=player)

    factories.GameFactory(losing_team__white_player=player)
    factories.GameFactory(losing_team__white_player=player)

    factories.GameFactory(losing_team__black_player=player)
    factories.GameFactory(losing_team__black_player=player)

    assert player.total_games == 8
