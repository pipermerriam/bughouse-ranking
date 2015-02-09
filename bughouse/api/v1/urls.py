from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'games', views.GameViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'players/(?P<player_pk>\d+)/ratings', views.PlayerRatingsViewSet)

urlpatterns = router.urls
