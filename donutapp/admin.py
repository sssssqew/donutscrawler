# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Word

# Register your models here.
class WordAdmin(admin.ModelAdmin):
	search_fields = ['value','donut', 'created_date', 'updated_date']
	
admin.site.register(Word, WordAdmin)
