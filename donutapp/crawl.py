# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import timedelta

# 날짜 생성 
def createPeriod(s_date, e_date):
	days = []
	d = datetime.strptime(s_date, "%Y-%m-%d")
	e = datetime.strptime(e_date, "%Y-%m-%d")
	
	while(d <= e):
		days.append(d)
		d = d + timedelta(days=1)
	return days


# Create your views here.
def store_single(request, value):
	s_date = request.POST.get("s_date")
	e_date = request.POST.get("e_date")
	print s_date
	print e_date
	print value
	days = createPeriod(s_date, e_date)
	print days
	return HttpResponse("crawl single")

def store_multi(request):
	return HttpResponse("crawl multi")