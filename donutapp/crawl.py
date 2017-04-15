# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Word, Count
from . import naver 

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


def save_counts(word, days):
	for day in days:
		try: 
			count = Count.objects.get(word_id=word.id, crawled_date = day)
			print "crawling data exists"
		except:
			counts = naver.get_counts(word.value, day)
			print counts

			count = Count(
				word_id = word.id, 
				value = counts, 
				type = "navernews",
				crawled_date = day
			)
			count.publish()
			count.save()


# Create your views here.
def store_single(request, value):
	word = Word.objects.get(value = value)
	# print word

	s_date = request.POST.get("s_date")
	e_date = request.POST.get("e_date")
	days = createPeriod(s_date, e_date)
	# print days

	save_counts(word, days)

	counts = Count.objects.all()
	for count in counts:
		print count.value
		print count.type
		print count.crawled_date

	return HttpResponse("crawl single")

def store_multi(request):
	words = Word.objects.all()

	s_date = request.POST.get("s_date")
	e_date = request.POST.get("e_date")
	days = createPeriod(s_date, e_date)
	# print days

	for word in words:
		save_counts(word, days)

		counts = Count.objects.filter(word_id=word.id)
		for count in counts:
			print count.value
			print count.type
			print count.crawled_date

	return HttpResponse("crawl multi")