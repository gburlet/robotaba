from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'robotaba.views.home'),
    url(r'^transcribe/upload/$', 'transcribe.views.upload_audio', name='transcribe_upload'),
    url(r'^transcribe/(?P<audio_id>\d+)/$', 'transcribe.views.process'),
    url(r'^pitchestimate/upload/$', 'pitchestimate.views.upload_audio', name='pitchestimate_upload'),
    url(r'^pitchestimate/(?P<audio_id>\d+)/$', 'pitchestimate.views.process'),
    url(r'^tabulate/upload/$', 'tabulate.views.upload_score', name='tabulate_upload'),
    url(r'^tabulate/(?P<pmei_id>\d+)/$', 'tabulate.views.process'),
    url(r'^tabulate/display/(?P<tmei_id>\d+)/$', 'tabulate.views.display'),
    url(r'^admin/', include(admin.site.urls))
)
