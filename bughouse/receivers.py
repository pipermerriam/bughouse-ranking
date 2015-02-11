from django.conf import settings
from django.utils.module_loading import import_string


def compute_ratings(sender, instance, created, raw, **kwargs):
    if not raw:
        for backend_path in settings.ELO_RATING_ENGINES:
            backend_klass = import_string(backend_path)
            backend = backend_klass()
            backend.compute_ratings(instance)
