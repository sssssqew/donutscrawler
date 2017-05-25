# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Word, Count, Donut
from django.core import serializers

import csv
import json
import collections

from datetime import datetime
from datetime import timedelta

from django.core.files.base import ContentFile

import os

def delete_spaces(words):
	w_list = []
	words = words.split(',')
	for word in words:
		w_list.append(word.strip())
	return w_list

# 도넛도 함께 추가하는 코드
# csv에서 같은 단어인데도 불구하고 띄워쓰기 등에 따라 중복 저장되기도 함 
# def save_model(words, donut):
# 	for i, word in enumerate(words):
# 		try:
# 			word_model = Word.objects.get(value=word)
# 			print word
# 		except:
# 			word_model = Word(value=word, donut=donut[i])
# 			word_model.publish()
# 			word_model.save() 

# csv에서 같은 단어인데도 불구하고 띄워쓰기 등에 따라 중복 저장되기도 함 
def save_model(words, donuts):
	for i, word in enumerate(words):
		# 워드 생성 
		try:
			word_model = Word.objects.get(value=word)
			print word
		except:
			word_model = Word(value=word)
			word_model.publish()
			word_model.save()

		# 도넛생성
		try:
			donut_model = Donut.objects.get(name = donuts[i])
			print donuts[i]
		except:
			donut_model = Donut(name = donuts[i])
			donut_model.publish()
			donut_model.save()

		# 도넛 - 워드 연결 
		try:
			donut_model.word.add(word_model)
		except:
			print "either word or donut model dose not exits in db"

def str_date(date):
	date_str = False
	if date:
		date_str = date.strftime('%Y-%m-%d')
	return date_str

def make_json(word, counts):
	donuts = word.donut_set.all()
	cook_json = collections.OrderedDict()

	donutlist = []
	# 한 단어당 도넛 중복 가능성 
	for donut in donuts:
		donutlist.append(donut.name)

	cook_json['donut'] = donutlist
	cook_json['word'] = word.value
	cook_json['created_date'] = str_date(word.created_date)
	cook_json['updated_date'] = str_date(word.updated_date)
	cook_json['history'] =  []

	# sort counts by crawled_date
	counts = sorted(counts, key=lambda m: (m.crawled_date,))

	for count in counts:
		cook_json['history'].append({
			'value': count.value,
			'type': count.type,
			'crawled_date': str_date(count.crawled_date),
			'created_date': str_date(count.created_date),
			'updated_date': str_date(count.updated_date)
		})
	return cook_json


# Create your views here.
def create(request):
	return render(request, "donutapp/create.html")

def store_single(request):
	words = request.POST.get('words')
	words = delete_spaces(words)
	print words
	save_model(words) 

	return HttpResponseRedirect(reverse('words_index'))

def store_multi(request):
	if 'file' in request.FILES:
		words = []
		donuts = []
		file = request.FILES['file']
		csvReader = csv.reader(file)

		for line in csvReader:
			words.append(line[2].decode('euc-kr'))
			donuts.append(line[1].decode('euc-kr'))

	save_model(words, donuts)
	# save_model(words)

	return HttpResponseRedirect(reverse('words_index'))

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
	query = request.GET.get("search_box")

	if query:
		try:
			donut = Donut.objects.get(name__icontains=query)
			word_list = donut.word.all()
		except:
			word_list = Word.objects.filter(
				Q(value__icontains=query) 
				# | Q(donut__icontains=query)
			).distinct()
	else:
		word_list = Word.objects.all()

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

	cook_json = make_json(word, counts)

	return HttpResponse(json.dumps(cook_json, indent=4))

def counts_latest(request):
	words = Word.objects.all()
	type = request.GET.get("type")
	date = request.GET.get("date")
	cook_json_all = []

	for word in words:
		counts = Count.objects.filter(word_id=word.id)
		if type:
			counts = counts.filter(type=type).distinct()
		if date:
			counts = counts.filter(crawled_date=datetime.strptime(date, "%Y-%m-%d")).distinct()

		cook_json = make_json(word, counts)
		cook_json_all.append(cook_json)

	return HttpResponse(json.dumps(cook_json_all, indent=4))


def rank(request):
	# words = Word.objects.all()
	page = request.GET.get('page')
	date = request.GET.get("date")
	date_target = datetime.strptime(date, "%Y-%m-%d")
	scope = int(request.GET.get('scope') or 15) 
	
	ranks = {}

	# get donut list
	cnt = 0
	donuts = Donut.objects.all()
	for donut in donuts:
		total = 0
		# print "----------------------------------------------------"
		# print donut[0].encode('utf-8') # str
		if donut: 
			donut_str = donut.name.encode('utf-8')
			print str(donut_str)
			# print "----------------------------------------------------"
			wordsInDonut = donut.word.all()
			cnt += 1
 
			for wordInDonut in wordsInDonut:
				# 도너츠 이미지 저장
				# img_path =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'upload')+'/' + str(cnt) + '.jpg'
				# print img_path
				# try:
				# 	if img_path:
				# 		with open(img_path) as f:
				# 			data = f.read()
				# 		wordInDonut.img.save(str(cnt) + '.jpg', ContentFile(data))
				# except:
				# 	print "no image !!"
				
				# print wordInDonut.value
				try:
					count = Count.objects.get(word_id=wordInDonut.id, crawled_date = date_target)
					total += count.value
				except:
					total += 0
			ranks[donut_str] = total

	print cnt 
	ranks = sorted(ranks.items(), key=lambda r: r[1], reverse=True)
	ranks_top = ranks[:scope]

	paginator = Paginator(ranks_top, 15)
	try:
		ranks_top = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		ranks_top = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		ranks_top = paginator.page(paginator.num_pages)

	# return HttpResponse(json.dumps(ranks_top, indent=4)) # JSON
	context = {'ranks':ranks_top, 'date':date, 'scope':scope}
	return render(request, "donutapp/ranks.html", context)




