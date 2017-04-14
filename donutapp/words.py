# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Word

import csv

# ------------------------------------------------------------------------------------
def delete_spaces(words):
	w_list = []
	words = words.split(',')
	for word in words:
		w_list.append(word.strip())
	return w_list
#-------------------------------------------------------------------------------------
def save_model(words):
	for word in words:
		try:
			word_model = Word.objects.get(value=word)
		except:
			word_model = Word(value=word)
			word_model.publish()
			word_model.save() 
#-------------------------------------------------------------------------------------

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
	return HttpResponse(value)

def index(request):
	return HttpResponse("index")

def counts_word(request, value):
	return HttpResponse("show counts for a word")

def counts_latest(request):
	return HttpResponse("show counts for latest data")



