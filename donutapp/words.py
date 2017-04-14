# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def create(request):
	return render(request, "donutapp/create.html")

def store_single(request):
	return HttpResponse("store single")

def store_multi(request):
	return HttpResponse("store multi")

def show(request, value):
	return HttpResponse(value)

def index(request):
	return HttpResponse("index")

def counts_word(request, value):
	return HttpResponse("show counts for a word")

def counts_latest(request):
	return HttpResponse("show counts for latest data")



