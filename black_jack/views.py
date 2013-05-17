# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from models import Player, Hand, Card, Dealer
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from helper import get_dealer, get_player

##Main Game Page Loader

# CARD INSTANCE FOR USE OF ENTIRE CLASS
C = Card()
#@login_required("/login/")


def main(request, template='main_game.html'):
    context = {}
    if request.POST:
        return HttpResponseBadRequest("Please do not post")
    else:
        get_player(request, context)
        return render(template, context, context_instance=RequestContext(request))


def start_game(request):
    context = {}
    if request.POST:
        return HttpResponseBadRequest("Please do not post")
    else:
        context = get_dealer(request, context)
        hand = Hand()
        hand.add_card(C.generate_card())
        hand.add_card(C.generate_card())
        hand.save()
        context['player'].hand = hand
        context['player'].save()
        dealhand = Hand()
        dealhand.add_card(C.generate_card())
        dealhand.save()
        context['dealer'].hand = dealhand
        context['dealer'].save()
        print context['dealer'].hand
        return HttpResponseRedirect('/game/playing')


def playing(request, template="running_game.html"):
    context = {}
    if request.POST:
        return HttpResponseBadRequest("Please do not post")
    else:
        context = get_dealer(request, context)
        return render(template, context, context_instance=RequestContext(request))


def hit(request):
    context = {}
    if request.POST:
        return HttpResponseBadRequest("Please do not post")
    else:
        context = get_player(request, context)
        context['player'].hand.add_card(C.generate_card())
        context['player'].hand.save()
        if context['player'].hand.value <= 21:
            return HttpResponseRedirect('/game/playing')
        else:
            return HttpResponseRedirect('/game/finish')


def bet(request):
    """This is the api for setting the bet"""
    context = {}
    if request.GET:
        context['player'] = Player.objects.get(user__username=request.META["USER"])
        context['dealer'] = Dealer.objects.get(player=context['player'])
        if int(context['player'].money) > int(request.GET['bet']):
            context['player'].bet = request.GET['bet']
            context['player'].save()
            return HttpResponse("Success")


def finish(request):
    def pick_winner(context):
        if context['player'].hand.value > 21:
            context['winner'] = "Dealer"
        elif context['dealer'].hand.value > 21:
            context['winner'] = context['player'].user.username
        elif context['player'].hand.value == context['dealer'].hand.value:
            context['winner'] = "Dealer"
        elif context['player'].hand.value < context['dealer'].hand.value:
            context['winner'] = "Dealer"
        else:
            context['winner'] = context['player'].user.username

        return context
    context = {}
    if request.POST:
        return HttpResponseBadRequest("Please do not post")
    else:
        context = get_dealer(request, context)
        while context['dealer'].hand.value < 17:
            context['dealer'].hand.add_card(C.generate_card())
            context['dealer'].hand.save()
            context['dealer'].save()
        context = pick_winner(context)
        if context['winner'] == "Dealer":
            context['player'].lose()
        else:
            context['player'].win()

        return render("final.html", context, context_instance=RequestContext(request))