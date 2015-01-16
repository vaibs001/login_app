from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render

from polls.models import Question

def index(request):
	latest_question_list= Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([p.question_text for p in latest_question_list])
	#template = loader.get_template('polls/index.html')
	context = {'latest_question_list': latest_question_list	}
	return render(request, 'polls/index.html', context)
	
def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
    	selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
    	return render(request, 'polls/detail.html', {
    		'question': p,
    		'error_message' : "You didn't select a choice.",
    		})
    else:
    	selected_choice.voted += 1
    	selected_choice.save()
    	return HttpResponseRedirect(reverse('polls:result', args=(p, id)))