import datetime
import csv

from django.conf import settings
from django.utils.module_loading import import_string

from bughouse.ratings.utils import (
    elo_chance_to_win,
)
from bughouse.models import (
    Game,
    OVERALL_OVERALL,
)


def compute_ratings_for_game(game):
    for backend_path in settings.ELO_RATING_ENGINES:
        backend_klass = import_string(backend_path)
        backend = backend_klass()
        backend.compute_ratings(game)


CSV_HEADERS = (
    'game',
    'winning_team',
    'winning_team_rating',
    'winning_team_chance_to_win',
    'losing_team',
    'losing_team_rating',
    'losing_team_chance_to_win',
    'winning_white',
    'winning_white_rating',
    'winning_white_adjusted_rating',
    'winning_white_probability_to_win',
    'winning_black',
    'winning_black_rating',
    'winning_black_adjusted_rating',
    'winning_black_probability_to_win',
    'losing_white',
    'losing_white_rating',
    'losing_white_adjusted_rating',
    'losing_white_probability_to_win',
    'losing_black',
    'losing_black_rating',
    'losing_black_adjusted_rating',
    'losing_black_probability_to_win',
    'losing_color',
    'loss_type',
)


def export_ratings_data_to_csv(engine, filename=None):
    if filename is None:
        filename = "ratings-data-export-{when}.csv".format(
            when=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        )

    key = engine.rating_key

    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, CSV_HEADERS)
        writer.writeheader()
        for game in Game.objects.order_by('created_at'):
            ww = game.winning_team.white_player
            wb = game.winning_team.black_player
            lw = game.losing_team.white_player
            lb = game.losing_team.black_player

            wwr = game.winning_team.white_player.get_rating_at_datetime(game.created_at, key)
            wbr = game.winning_team.black_player.get_rating_at_datetime(game.created_at, key)
            lwr = game.losing_team.white_player.get_rating_at_datetime(game.created_at, key)
            lbr = game.losing_team.black_player.get_rating_at_datetime(game.created_at, key)

            wwar = engine.adjust_rating(wwr, wbr, lbr, lwr)
            wbar = engine.adjust_rating(wbr, wwr, lwr, lbr)
            lwar = engine.adjust_rating(lwr, lbr, wbr, wwr)
            lbar = engine.adjust_rating(lbr, lwr, wwr, wbr)

            wwp = elo_chance_to_win(wwar, lbar)
            wbp = elo_chance_to_win(wbar, lwar)
            lwp = elo_chance_to_win(lwar, wbar)
            lbp = elo_chance_to_win(lbar, wwar)

            wt = game.winning_team
            lt = game.losing_team

            wtr = game.winning_team.get_rating_at_datetime(game.created_at, OVERALL_OVERALL)
            ltr = game.losing_team.get_rating_at_datetime(game.created_at, OVERALL_OVERALL)

            wtp = elo_chance_to_win(wtr, ltr)
            ltp = elo_chance_to_win(ltr, wtr)

            row = {
                'game': game.pk,
                'winning_team': wt.pk,
                'winning_team_rating': wtr,
                'winning_team_chance_to_win': wtp,
                'losing_team': lt.pk,
                'losing_team_rating': ltr,
                'losing_team_chance_to_win': ltp,
                'winning_white': ww.pk,
                'winning_white_rating': wwr,
                'winning_white_adjusted_rating': wwar,
                'winning_white_probability_to_win': wwp,
                'winning_black': wb.pk,
                'winning_black_rating': wbr,
                'winning_black_adjusted_rating': wbar,
                'winning_black_probability_to_win': wbp,
                'losing_white': lw.pk,
                'losing_white_rating': lwr,
                'losing_white_adjusted_rating': lwar,
                'losing_white_probability_to_win': lwp,
                'losing_black': lb.pk,
                'losing_black_rating': lbr,
                'losing_black_adjusted_rating': lbar,
                'losing_black_probability_to_win': lbp,
                'losing_color': game.losing_color,
                'loss_type': game.loss_type,
            }
            writer.writerow(row)
