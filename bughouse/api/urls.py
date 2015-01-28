from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^v1/', include('bughouse.api.v1.urls', namespace='v1')),
)
