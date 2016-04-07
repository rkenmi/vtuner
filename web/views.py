from django.shortcuts import render, get_object_or_404
# from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Question, Choice, MP3
from django.views import generic
from django.utils import timezone
from django.utils.text import slugify
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from wsgiref.util import FileWrapper
from web.vtunerRG.driver import ReplayGain
from threading import Timer
import os

# Create your views here.

def change_file(new_file_name):

    def timeout(args):
        print "[Timer expired] Deleting " + args
        os.remove(default_storage.path(args))

    try:
        tags = ReplayGain(default_storage.path(new_file_name))
        print tags
        new_file = FileWrapper(open(default_storage.path(new_file_name)))
        t = Timer(10, timeout, args=[new_file_name])
        t.start()
        return new_file
        #~
    except:
        message = 'Error: is the file a proper MP3?'

def verify_file(raw_file_name, form):
    # Retrieve mp3 object from the (user)submitted form
    obj = form.save(commit=False)
    storage = obj.mp3file.storage

    safe_file_name = slugify(raw_file_name, allow_unicode=True)
    safe_file_name = safe_file_name[:-3] + ".mp3"
    new_file_name = storage.get_available_name(safe_file_name)

    print "name: ", new_file_name
    obj.mp3file.name = new_file_name
    form.save()
    #new_file_name = u'%s' % new_file_name
    return new_file_name

def upload_file(request, raw_filename = '', message = ''):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            raw_filename = request.FILES['mp3file'].name
            if request.FILES['mp3file'].content_type == 'audio/mpeg':
                new_filename = verify_file(raw_filename, form)
                new_file = change_file(new_filename)

                response = HttpResponse(new_file, content_type='audio/mpeg')
                response['Content-Disposition'] = 'attachment; filename= %s' % new_filename.encode('utf-8')
                response['Content-Length'] = len(response.content)
                return response
            else:
                message = "Invalid file type"
    else:
        form = UploadFileForm()

    return render(request, 'web/upload.html', {
        'form': form,
        'filename': raw_filename,
        'message': message,
    })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'web/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('web:results', args=(question.id,)))
