from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'robotaba.views.home', name='home_url'),
    url(r'^about/', 'robotaba.views.about', name='about_url'),
    url(r'^contact/', 'robotaba.views.contact', name='contact_url'),
    url(r'^transcribe/upload/$', 'transcribe.views.upload_audio', name='transcribe_upload'),
    url(r'^transcribe/(?P<audio_id>\d+)/$', 'transcribe.views.process'),
    url(r'^pitchestimate/upload/$', 'pitchestimate.views.upload_audio', name='pitchestimate_upload'),
    url(r'^pitchestimate/(?P<audio_id>\d+)/$', 'pitchestimate.views.process'),
    url(r'^tabulate/upload/$', 'tabulate.views.upload_score', name='tabulate_upload'),
    url(r'^tabulate/(?P<pmei_id>\d+)/$', 'tabulate.views.process'),
    url(r'^display/upload/$', 'robotaba.views.upload_tablature', name='display_upload'),
    url(r'^display/(?P<tmei_id>\d+)/$', 'robotaba.views.display'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls))
)
