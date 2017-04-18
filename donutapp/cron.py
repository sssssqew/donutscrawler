# -*- coding: utf-8 -*-
from .models import Word, Count
from . import naver 
from crawl import save_counts

from datetime import datetime
from datetime import timedelta
import pytz


def my_scheduled_job():
	tz = pytz.timezone('Asia/Seoul')
	log_time = datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
	print "log time : " + log_time + "-----> cron job executed !!"

	# change data format 
	days = datetime.now(tz=tz) - timedelta(days=1)
	days = days.strftime("%Y-%m-%d")
	days = [datetime.strptime(days, "%Y-%m-%d")]
	# print days

	words = Word.objects.all()

	for word in words:
		save_counts(word, days)

