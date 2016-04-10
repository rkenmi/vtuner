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

def change_file(new_file_name, custom_gain):

    def timeout(args):
        print "[Timer expired] Deleting " + args
        os.remove(default_storage.path(args))

    try:
        tags = ReplayGain(default_storage.path(new_file_name), custom_gain)
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

    #print request.is_ajax()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            raw_filename = request.FILES['mp3file'].name
            filetype = request.FILES['mp3file'].content_type
            if filetype == 'audio/mpeg' or filetype == 'audio/mp3':
                if 'custom_val' in request.POST:
                    custom_gain = request.POST['custom_val']
                else:
                    custom_gain = None
                print custom_gain
                new_filename = verify_file(raw_filename, form)
                new_file = change_file(new_filename, custom_gain)
                response = HttpResponse(new_file, content_type='application/download')
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
