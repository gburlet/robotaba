from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

import os

from robotaba.models import Audio, MetaMusic
from tabulate.models import MeiTab
from robotaba.resources.meitoalphatex import meitoalphatex
from robotaba.forms import UploadTablatureForm

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

def about(request):
    '''
    Serve the about page
    '''

    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    '''
    Serve the contact page
    '''

    return render_to_response('contact.html', context_instance=RequestContext(request))

def upload_tablature(request):
    '''
    Handle score file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadTablatureForm(request.POST, request.FILES)
        if form.is_valid():
            # check extension of uploaded score file
            input_file = request.FILES['score_file']

            # TODO: try and parse this information from the XML file
            meta = MetaMusic(
                title=request.POST['title'], 
                artist=request.POST['artist'],
                copyright=request.POST['copyright']
            )
            meta.save()

            filename, input_ext = os.path.splitext(input_file.name)
            if input_ext == '.xml':
                # convert the MusicXML file to Mei format
                tmei = MeiTab(fk_mid=meta)
                tmei.convert_musicxml(filename+'.mei', request.FILES['score_file'].read())
            elif input_ext == '.mei':
                # the uploaded file is an mei file, put it directly into the model
                tmei = MeiTab(mei_file=input_file, fk_mid=meta)
                tmei.save()
            else:
                raise ValueError('Input file must be a MusicXML or Mei file')

            # display the uploaded tab
            return HttpResponseRedirect('/display/%d' % tmei.id)
    else:
        # serve the form
        form = UploadTablatureForm()

    return render_to_response('uploadtablature.html', {'form': form}, context_instance=RequestContext(request))

def display(request, tmei_id):
    # query db for the mei tab file
    tmei = get_object_or_404(MeiTab, pk=tmei_id)

    alpha_tex = meitoalphatex(tmei.mei_file.path)

    return render_to_response('displaytab.html', {'alphatex': alpha_tex}, context_instance=RequestContext(request))
