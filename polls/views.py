from django.template import loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choise, Question

# Get questions and display them
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choises
def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {'question': question})

# Get question and display results
def results(request, question_id):
    question =  get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {'question': question})
    
# Vote for a question choise
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choise = question.choise_set.get(pk=request.POST['choise'])
    except(KeyError, Choise.DoesNotExist):
        # Redispley the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did'n select a choise.",
        })
    else:
        selected_choise.votes += 1
        selected_choise.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))