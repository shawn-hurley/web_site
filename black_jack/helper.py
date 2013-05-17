__author__ = 'hurle1s'
from models import Player, Dealer


def get_player(request, context):
    """This should return the context including the the player"""
    context['player'] = Player.objects.get(user__username=request.META["USER"])
    return context


def get_dealer(request, context):
    """This should return the context including the dealer, requires that the player has already been found, if not
        It will call get_player.
    """
    try:
        context['dealer'] = Dealer.objects.get(player=context['player'])
    except Exception:
        context = get_player(request, context)
        try:
            context['dealer'] = Dealer.objects.get(player=context['player'])
        except Exception:
            context['dealer'] = Dealer(player=context['player'])

    return context