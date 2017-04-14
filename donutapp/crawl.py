# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def store_single(request, value):
	return HttpResponse("crawl single")

def store_multi(request):
	return HttpResponse("crawl multi")