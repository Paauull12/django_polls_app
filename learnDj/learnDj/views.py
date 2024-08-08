from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    return HttpResponse('<h1> Hello </h1> <br> <h2> This is not a nice page, go to: <br> <a href="polls/">Here</a> </h2>')