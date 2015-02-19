import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.module_loading import import_string

from bughouse.ratings.engines import export_ratings_data_to_csv


class Command(BaseCommand):
    help = 'Recompute all ratings using all active engines'

    def handle(self, *args, **options):
        for backend_path in settings.ELO_RATING_ENGINES:
            backend_klass = import_string(backend_path)
            backend = backend_klass()

            if not hasattr(backend, 'rating_key'):
                continue

            filename = "{engine}-ratings-{when}.csv".format(
                engine=backend_path.rpartition('.')[2],
                when=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            )

            try:
                export_ratings_data_to_csv(backend, filename)
            except NotImplemented:
                pass
