from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from .models import MP3
from django.views import generic
from django.utils import timezone
from django.utils.text import slugify
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from wsgiref.util import FileWrapper
from web.app.driver import ReplayGain
from threading import Timer
import os


def change_file(new_file_name, custom_gain):
    """ Applys ReplayGain to the file and renames the file. Serves the file
        afterwards.

        Parameters:
            new_file_name : String that contains the new file name
            custom_gain : float that contains new custom gain value

        Returns:
            new_file : The new data file to be sent through HttpResponse
    """
    def timeout(args):
        """ After a certain time period, delete the file from the local system.

            Parameters:
                args : A list which contains the file name to be deleted
        """
        print "[Timer expired] Deleting " + args
        os.remove(default_storage.path(args))

    try:
        tags = ReplayGain(default_storage.path(new_file_name), custom_gain)
        print tags
        new_file = FileWrapper(open(default_storage.path(new_file_name)))
        t = Timer(10, timeout, args=[new_file_name])
        t.start()
        return new_file
    except:
        message = 'Error: is the file a proper MP3?'


def fix_name(raw_file_name, form):
    """ Given a raw file name, generate a safe file name for serving

        Parameters:
            raw_file_name : String that contains the old file name
            form : Django Form object

        Returns:
            new_file_name : a new safe file name for serving
    """
    # Retrieve mp3 object from the (user)submitted form
    obj = form.save(commit=False)
    storage = obj.mp3file.storage

    safe_file_name = slugify(raw_file_name, allow_unicode=True)
    safe_file_name = safe_file_name[:-3] + ".mp3"
    new_file_name = storage.get_available_name(safe_file_name)

    print "name: ", new_file_name
    obj.mp3file.name = new_file_name
    form.save()
    #  new_file_name = u'%s' % new_file_name
    return new_file_name


def upload_file(request, raw_filename='', message=''):
    """ Upload a file. If the file is a valid MP3 type, the upload process is
        started.

        Parameters:
            request         : the HTTP GET or POST request
            raw_filename    : the original file name via upload
            message         : a message to be returned in response

        Returns:
            JsonResponse if the request method is POST, otherwise HttpResponse
    """
    if request.method == 'POST':
        raw_filename = request.FILES['mp3file'].name
        form = UploadFileForm(request.POST, request.FILES)
        if request.FILES['mp3file'].size > 15000000:
            print "SIZE: ", request.FILES['mp3file'].size
            message = "File size too large"
            return JsonResponse({
                'error': 1,
                'message': message,
                'filename': raw_filename
            })
        elif form.is_valid():
            filetype = request.FILES['mp3file'].content_type
            if filetype == 'audio/mpeg' or filetype == 'audio/mp3':
                if 'custom_val' in request.POST:
                    custom_gain = request.POST['custom_val']
                else:
                    custom_gain = None
                print custom_gain
                new_filename = fix_name(raw_filename, form)
                new_file = change_file(new_filename, custom_gain)
                response = HttpResponse(
                    new_file, content_type='application/download'
                )
                cd = 'attachment; filename= %s' % new_filename.encode('utf-8')
                response['Content-Disposition'] = cd
                response['Content-Length'] = len(response.content)
                return response
            else:
                message = "Invalid file type"
                return JsonResponse({
                    'error': 2,
                    'message': message,
                    'filename': raw_filename
                })
    else:
        form = UploadFileForm()

    return render(request, 'web/upload.html', {
        'form': form,
        'filename': raw_filename,
        'message': message,
    })
