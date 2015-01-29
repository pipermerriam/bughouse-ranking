from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from . import views


urlpatterns = patterns(
    '',
    url(r'^api/', include('bughouse.api.urls')),
    url(r'^$', views.ReportGameView.as_view(), name='report-game'),
    url(r'^report-game/$', views.ReportGameView.as_view(), name='report-game'),
    url(r'^add-player/$', views.CreatePlayerView.as_view(), name='create-player'),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
