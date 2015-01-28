from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'games', views.GameViewSet)

urlpatterns = router.urls
