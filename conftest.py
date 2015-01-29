import pytest


@pytest.fixture()  # NOQA
def factories(db):
    import factory
    from tests.factories import (  # NOQA
        PlayerFactory,
        TeamFactory,
        GameFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.DjangoModelFactory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(db):
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )

@pytest.fixture()
def elo_settings(settings):
    settings.ELO_K = 10.0 
    settings.ELO_WIN_TEAM = 50 / settings.ELO_K
    settings.ELO_LOSE_TEAM = -  settings.ELO_WIN_TEAM
    settings.ELO_WIN_SELF = 55 / settings.ELO_K
    settings.ELO_WIN_PARTNER = 45 / settings.ELO_K
    settings.ELO_LOSE_SELF = - settings.ELO_WIN_SELF
    settings.ELO_LOSE_PARTNER = -settings.ELO_WIN_PARTNER

    settings.ELO_PARTNER_WEIGHT =  1.0/5.0
    settings.ELO_SELF_WEIGHT = 1 - settings.ELO_PARTNER_WEIGHT
    settings.ELO_PROVISIONAL_GAME_LIMIT = 10
    settings.ELO_PROVISIONAL_GAME_MODIFIER = 4

    return settings
