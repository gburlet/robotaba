from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from robotaba.models import MetaMusic
from pitchestimate.models import MeiPitch
from tabulate.models import Tabulate
from tabulate.forms import UploadScoreForm
from tabulate.resources.meitoalphatex import meitoalphatex

import os

def upload_score(request):
    '''
    Handle score file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadScoreForm(request.POST, request.FILES)
        if form.is_valid():
            # check extension of uploaded score file
            input_file = request.FILES['score_file']
            _, input_ext = os.path.splitext(input_file.name)
            if input_ext == '.xml':
                # TODO: convert to mei
                pass
            elif input_ext != '.mei':
                raise ValueError('Input file must be a MusicXML or Mei file')

            pmei = MeiPitch(mei_file=input_file)
            pmei.save()

            frets = request.POST['num_frets']
            capo = request.POST['capo']
            tuning = request.POST['tuning']

            # redirect and construct the Tabulate object in the process view to allow
            # the input file to be processed multiple times by the user
            # to get different tablature output, if desired.
            return HttpResponseRedirect('/tabulate/%d/?frets=%s&capo=%s&tuning=%s' % (pmei.id, frets, capo, tuning))
    else:
        # serve the form
        form = UploadScoreForm()

    return render_to_response('uploadscore.html', {'form': form}, context_instance=RequestContext(request))

def process(request, pmei_id):
    # query db for the mei file containing the pitch information
    pmei = get_object_or_404(MeiPitch, pk=pmei_id)

    try:
        frets = int(request.GET['frets'])
        capo = int(request.GET['capo'])
        tuning = request.GET['tuning']
    except KeyError:
        return HttpResponse("Need to specify number of frets, capo position, and guitar tuning")

    taber = Tabulate(fk_pmei=pmei, num_frets=frets, tuning=tuning, capo=capo)
    # writing to the database writes the start timestamp
    taber.save()

    # TODO: create spinner on interface
    mei_tab_path = taber.gen_tab()

    alpha_tex = meitoalphatex(mei_tab_path)

    # TODO: create tab viewer url instead of rendering to response here
    return render_to_response('displaytab.html', {'alphatex': alpha_tex}, context_instance=RequestContext(request))
