# -*- coding: utf-8 -*-
from .models import Word, Count
from . import naver 
from crawl import save_counts

from datetime import datetime
from datetime import timedelta
import pytz

from django.core.mail import send_mail


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

	print days[0]

	for word in words:
		save_counts(word, days)
	
	counts = Count.objects.filter(crawled_date = days[0])
	print words.count()
	print counts.count()

	failed_words_count = words.count() - counts.count()
	print failed_words_count

	send_mail('[도넛크롤러] 크롤링 결과', '금일 크롤링을 완료했습니다.' , 'sy.lee@dna.uno', ['sy.lee@dna.uno'], fail_silently=False)

	# print subject
	# print content



	

