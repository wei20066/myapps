from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import render,get_object_or_404
from django.http import *
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from .forms import UploadFileForm
from .function import *
from mysite.settings import *
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context, request))
	
	
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
	#try:
        #question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
        #raise Http404("Question does not exist")
		#return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', context)



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):     
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()       
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 注意获取数据的方式
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})
	
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
'''



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
	
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):     
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()       
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 注意获取数据的方式
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@csrf_exempt	
def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        import os
        f = open(os.path.join(BASE_DIR, 'polls\static', 'pic', file_obj.name), 'wb')
        print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        print('11111')
        return HttpResponse('OK')

def upload_iframe(request):
    if request.method == 'POST':
        print(request.POST.get('user', None))
        print(request.POST.get('password', None))
        file_obj = request.FILES.get('file')
        import os
        f = open(os.path.join(BASE_DIR, 'polls\static', 'pic', file_obj.name), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('OK')

def upload(request):
    if request.method == 'POST':# 获取对象
        obj = request.FILES.get('fafafa')
        import os # 上传文件的文件名 
        f = open(os.path.join(BASE_DIR, 'polls\static', 'pic', obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        return  HttpResponse('OK')
    return render(request, 'upload.html')
