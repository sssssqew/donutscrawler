# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Word, Count
from django.core import serializers

import csv
import json
import collections

def delete_spaces(words):
	w_list = []
	words = words.split(',')
	for word in words:
		w_list.append(word.strip())
	return w_list

# csv에서 같은 단어인데도 불구하고 띄워쓰기 등에 따라 중복 저장되기도 함 
def save_model(words):
	for word in words:
		try:
			word_model = Word.objects.get(value=word)
			print word
		except:
			word_model = Word(value=word)
			word_model.publish()
			word_model.save() 

def str_date(date):
	date_str = False
	if date:
		date_str = date.strftime('%Y-%m-%d')
	return date_str



# Create your views here.
def create(request):
	return render(request, "donutapp/create.html")

def store_single(request):
	words = request.POST.get('words')
	words = delete_spaces(words)
	print words
	save_model(words) 

	return HttpResponse("store single")

def store_multi(request):
	if 'file' in request.FILES:
		words = []
		file = request.FILES['file']
		csvReader = csv.reader(file)

		for line in csvReader:
			words.append(line[0].decode('euc-kr'))

	save_model(words)

	return HttpResponse("store multi")

def show(request, value):
	word = Word.objects.get(value=value)
	counts = Count.objects.filter(word_id=word.id)
	date = []
	data = []

	for count in counts:
		date.append(count.crawled_date)
		data.append(count.value)

	tuples = sorted(zip(date, data))
	date, data = [t[0].strftime('%Y-%m-%d') for t in tuples], [t[1] for t in tuples]
 
	date.insert(0, 'x')
	data.insert(0, value)
	columns = [date, data]

	context = {'columns': json.dumps(columns), 'word':word}
	return render(request, "donutapp/show.html", context)

def index(request):
	word_list = Word.objects.all()
	query = request.GET.get("search_box")

	if query:
		word_list = word_list.filter(
			Q(value__icontains=query) |
			Q(donut__icontains=query)
		).distinct()

	paginator = Paginator(word_list, 6)
	page = request.GET.get('page')

	try:
		words = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		words = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		words = paginator.page(paginator.num_pages)

	context = {'words': words}
	return render(request, "donutapp/index.html", context)

def counts_word(request, value):
	word = Word.objects.get(value=value)
	counts = Count.objects.filter(word_id=word.id)

	s_date = request.GET.get("s_date")
	e_date = request.GET.get("e_date")
	type = request.GET.get("type")

	# conditional query 
	if s_date:
		counts = counts.filter(crawled_date__gte=s_date).distinct()
	if e_date:
		counts = counts.filter(crawled_date__lte=e_date).distinct()
	if type:
		counts = counts.filter(type=type).distinct()

	cook_json = collections.OrderedDict()
	cook_json['word'] = word.value 
	cook_json['donut'] = word.donut 
	cook_json['created_date'] = str_date(word.created_date)
	cook_json['updated_date'] = str_date(word.updated_date)
	cook_json['history'] =  []
	for count in counts:
		cook_json['history'].append({
			'value': count.value,
			'type': count.type,
			'crawled_date': str_date(count.crawled_date),
			'created_date': str_date(count.created_date),
			'updated_date': str_date(count.updated_date)
		})

	return HttpResponse(json.dumps(cook_json, indent=4))

def counts_latest(request):
	# words = Word.objects.all()
	
	return HttpResponse("show counts for latest data")



