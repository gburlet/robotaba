from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'robotaba.views.home'),
    url(r'^upload/$', 'robotaba.views.upload_audio', name="audio_upload"),
    url(r'^transcribe/(?P<audio_id>\d+)/$', 'transcribe.views.index'),
    url(r'^admin/', include(admin.site.urls))
)
