# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Word(models.Model):
	value = models.CharField(max_length=30)
	donut = models.CharField(max_length=50,  blank=True, null=True)
	created_date = models.DateTimeField(blank=True, null=True)
	updated_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.created_date = timezone.now()
		
	def change(self):
		self.updated_date = timezone.now()

	def __str__(self):
		return self.value.encode('utf-8')

class Count(models.Model):
	word = models.ForeignKey(Word)
	value = models.IntegerField(default = 0)
	type = models.CharField(max_length=50,  blank=True, null=True)
	crawled_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(blank=True, null=True)
	updated_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.created_date = timezone.now()
		
	def change(self):
		self.updated_date = timezone.now()

	def __str__(self):
		return self.value.encode('utf-8')