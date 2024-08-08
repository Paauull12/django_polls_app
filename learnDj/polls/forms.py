from django import forms
from .models import Comment, Question, Choice
from django.forms import inlineformset_factory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

ChoiceInlineFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=3)

