from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Question, Choice, Comment, Like, UniqueVote
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from .forms import CommentForm, QuestionForm, ChoiceInlineFormSet, ChoiceForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all().order_by('is_for_adults')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['allowed_context_count_adults'] = Question.objects.filter(is_allowed=True, is_for_adults=True).count()
        context['allowed_context_count_minor'] = Question.objects.filter(is_allowed=True, is_for_adults=False).count()

        return context


@login_required
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.user = request.user
            comment.save()
            return redirect('polls:detail', pk=question_id)
    else:
        form = CommentForm()

    return render(request, 'polls/add_comment.html', {'form': form, 'question': question})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.user:
        return redirect('polls:detail', pk=question.id)

    if question:
        question.delete()

    return redirect('polls:index')

@login_required
def delete_commment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.user:
        return redirect('polls:detail', pk=comment.question.id)

    if comment:
        comment.delete()

    return redirect('polls:detail', pk=comment.question.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.user:
        return redirect('polls:detail', pk=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('polls:detail', pk=comment.question.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        'question': comment.question,
        'form': form,
        'comment': comment,
    }

    return render(request, 'polls/edit_comment.html', context)

@login_required
def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceInlineFormSet(request.POST, instance=Question())

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            formset.instance = question
            formset.save()
            return redirect('polls:index')
    else:
        question_form = QuestionForm()
        formset = ChoiceInlineFormSet(instance=Question())

    return render(request, 'polls/add_question.html', {
        'question_form': question_form,
        'formset': formset,
    })

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.user:
        return redirect('polls:detail', pk=question.id)

    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=1, can_delete=True)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.filter(question=question))

        if question_form.is_valid() and formset.is_valid():
            # Save the question form
            question_form.save()

            # Save the choice forms
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                else:
                    if form.instance.pk is None:
                        form.instance.question = question
                    form.save()
            return redirect('polls:detail', pk=question.id)
    else:
        question_form = QuestionForm(instance=question)
        formset = ChoiceFormSet(queryset=Choice.objects.filter(question=question))

    context = {
        'question_form': question_form,
        'formset': formset,
        'question': question,
    }

    return render(request, 'polls/edit_question.html', context)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        like.delete()

    return redirect('polls:detail', pk=comment.question.id)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = self.object

        user_has_voted = UniqueVote.objects.filter(user=self.request.user, question=question).exists()

        context['user_has_voted'] = user_has_voted
        context['comments'] = question.comments.all()

        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context ={
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        is_unique = UniqueVote.objects.get(user=request.user, question=question)

        messages.error(request, "You have already voted on this question.")
        return redirect('polls:detail', pk=question.id)

    except UniqueVote.DoesNotExist:
        try:
            # Attempt to get the selected choice
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the voting form with an error message if no choice was selected
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            # Record the user's vote
            selected_choice.votes += 1
            selected_choice.save()

            # Create a UniqueVote entry to prevent multiple votes from the same user
            unique_vote = UniqueVote(user=request.user, question=question)
            unique_vote.save()

            # Redirect to the results page
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
