__author__ = 'hurle1s'
from django.contrib import admin
from black_jack.models import *

admin.site.register(Player)
admin.site.register(Dealer)
admin.site.register(Hand)