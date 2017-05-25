# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Donut, Word
import time

def home(request):
	donuts = Donut.objects.all()

	for donut in donuts:
		print "-------------------------"
		print donut.name.encode('utf-8') # error fixed
		print "-------------------------"
		wordsInDonut = donut.word.all()
		if wordsInDonut:
			for wordInDonut in wordsInDonut:
				print wordInDonut.value.encode('utf-8')
			print "-------------------------"
			time.sleep(0.2)
	return render(request, "donutapp/home.html")