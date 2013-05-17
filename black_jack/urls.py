__author__ = 'hurle1s'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^main', 'black_jack.views.main'),
    url(r'start_game', 'black_jack.views.start_game'),
    url(r'playing', 'black_jack.views.playing'),
    url(r'hit', 'black_jack.views.hit'),
    url(r'finish', 'black_jack.views.finish'),
    url(r'bet', 'black_jack.views.bet'),

)