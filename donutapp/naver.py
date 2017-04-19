# -*- coding: utf-8 -*- 
import urllib2
import lxml
from bs4 import BeautifulSoup
from background_task import background
from datetime import datetime

# URL 쿼리 설정 
TARGET_URL_BEFORE_QUERY = 'https://search.naver.com/search.naver?where=news&se=0&query='
TARGET_URL_BEFORE_FRONT_DATE = '&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds='
TARGET_URL_BEFORE_BACK_DATE = '&docid=&nso=so%3Ar%2Cp%3Afrom'
TARGET_URL_REST = '%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0'


# URL 쿼리 생성 
def createUrlQuery(value, day):
	front_date = day.strftime('%Y.%m.%d') # URL 앞부분 날짜 포맷
	back_date = day.strftime('%Y%m%d') # URL 뒷부분 날짜 포맷
	query = TARGET_URL_BEFORE_QUERY \
							+ urllib2.quote(value.encode('utf-8')) \
							+ TARGET_URL_BEFORE_FRONT_DATE \
							+ front_date + '&de=' \
							+ front_date + TARGET_URL_BEFORE_BACK_DATE \
							+ back_date + 'to' \
							+ back_date \
							+ TARGET_URL_REST
	return query

 
# 뉴스 건수 추출 
def getNumberOfNews(query):
	try:
		# 사람이 검색하는 것처럼 속임 
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = { 'User-Agent' : user_agent }
		r = urllib2.Request(query, headers=headers)
		html = urllib2.urlopen(r)
	except Exception as e:
		# html.close()
		print e
		return 0

	soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

	if not soup.find('div', 'title_desc all_my'):
		html.close()
		print "no news found"
		return 0

	counts_str = soup.find('div', 'title_desc all_my').select('span')[0].text.split('/')
	counts = int(filter(lambda x: x.isdigit(), counts_str[1])) # 숫자 추출 
	html.close()
	return  counts

# 크롤링 메인 모듈 
def get_counts(value, day):
	print "searching..."
	query = createUrlQuery(value, day)
	counts = getNumberOfNews(query)
	return counts