from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import Question, Choice
from django.utils import timezone
from django.urls import reverse
import os


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output = ", ".join([q.question_text for q in latest_question_list])
    # print(os.path.relpath())
    # template = loader.get_template("polls\index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls\\templates\index.html", context)

def add_question(request, question_text):

    new_question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
    new_question.save()
    return HttpResponse('Donewhell')

# Leave the rest of the views (detail, results, vote) unchanged

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404(f"Question does not exist. There is only {len(Question.objects.all())} questions")
    # return render(request, "polls/detail.html", {"question": question})
    return render(request, 'polls\\templates\detail.html', {"question": question})


def results(request, question_id):

    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))