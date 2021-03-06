# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Word, Count, Donut

# from .models import Count

# Register your models here.
class WordAdmin(admin.ModelAdmin):
	search_fields = ['value','donut', 'created_date', 'updated_date']

class CountAdmin(admin.ModelAdmin):
	search_fields = ['type','crawled_date', 'created_date', 'updated_date']
	ordering = ('word', 'crawled_date',)

class DonutAdmin(admin.ModelAdmin):
	search_fields = ['name', 'created_date', 'updated_date']
	ordering = ('name', 'created_date',)
	
admin.site.register(Word, WordAdmin)
admin.site.register(Count, CountAdmin)
admin.site.register(Donut, DonutAdmin)
