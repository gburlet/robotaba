'''
Copyright (C) 2013 Gregory Burlet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'robotaba.views.home', name='home_url'),
    url(r'^search/', 'robotaba.views.search', name='search_url'),
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
