from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from . import views


urlpatterns = patterns(
    '',
    url(r'^api/', include('bughouse.api.urls')),
    url(r'^report-game/$', views.ReportGameView.as_view(), name='report-game'),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
