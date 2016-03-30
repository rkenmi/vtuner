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

class IndexView(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'web/detail.html'
    def get_queryset(self):
    	return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'web/results.html'

class UploadView(generic.TemplateView):
    model = MP3
    form = UploadFileForm()
    template_name = 'web/upload.html'

def upload_file(request, filename = '', message = ''):

    def timeout(args):
        print "[Timer expired] Deleting " + args
        os.remove(default_storage.path(args))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            storage = obj.mp3file.storage
            raw_file_name = request.FILES['mp3file'].name
            safe_file_name = slugify(raw_file_name)
            safe_file_name = safe_file_name[:-3] + ".mp3"
            new_file_name = storage.get_available_name(safe_file_name)
            print "name: ", new_file_name
            obj.mp3file.name = new_file_name
            form.save()
            try:
                ReplayGain(default_storage.path(new_file_name))
                new_file = FileWrapper(open(default_storage.path(new_file_name)))
                t = Timer(10, timeout, args=[new_file_name])
                t.start()
                response = HttpResponse(new_file, content_type='audio/mpeg')
                response['Content-Disposition'] = 'attachment; filename="%s"' % new_file_name
                response['Content-Length'] = len(response.content)
                return response
            except:
                message = 'Error: is the file a proper MP3?'
    else:
        form = UploadFileForm()

    return render(request, 'web/upload.html', {
        'form': form,
        'filename': filename,
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
