from django.conf.urls import url
from . import words
from . import crawl 

# url order is very important 
urlpatterns = [
	url(r'^words/$', words.index, name='words_index'),
	url(r'^words/create/$', words.create, name='words_create'),
	url(r'^words/store-single/$', words.store_single, name='words_store_single'),
	url(r'^words/store-multi/$', words.store_multi, name='words_store_multi'),
	url(r'^words/crawl/$', crawl.store_multi, name='crawl_store_multi'),
	url(r'^words/last-counts/$', words.counts_latest, name='words_counts_latest'),
	url(r'^words/(?P<value>.+)/counts$', words.counts_word, name='words_counts_word'),
	url(r'^words/(?P<value>.+)/crawl$', crawl.store_single, name='crawl_store_single'),
	url(r'^words/(?P<value>.+)/$', words.show, name='words_show'),
]