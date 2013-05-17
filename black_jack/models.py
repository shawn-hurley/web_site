from django.db import models
from django.contrib.auth.models import User
from random import randrange
from random import shuffle
# Create your models here.


class Card(object):
    dict_of_card_values = {"s1": ["Ace of Spades", 11, "/static/cards/1.png"], "s2": ["2 of Spades", 2, "/static/cards/2.png"],
                           "s3": ["3 of Spades", 3, "/static/cards/3.png"], "s4": ["4 of Spades", 4, "/static/cards/4.png"],
                           "s5": ["5 of Spades", 5, "/static/cards/5.png"], "s6": ["6 of Spades", 6, "/static/cards/6.png"],
                           "s7": ["7 of Spades", 7, "/static/cards/7.png"], "s8": ["8 of Spades", 8, "/static/cards/8.png"],
                           "s9": ["9 of Spades", 9, "/static/cards/9.png"], "s10": ["10 of Spades", 10, "/static/cards/10.png"],
                           "s11": ["Jack of Spades", 10, "/static/cards/11.png"],
                           "s12": ["Queen of Spades", 10, "/static/cards/12.png"],
                           "s13": ["King of Spades", 10, "/static/cards/13.png"],
                           "h1": ["Ace of Hearts", 11, "/static/cards/14.png"], "h2": ["2 of Hearts", 2, "/static/cards/15.png"],
                           "h3": ["3 of Hearts", 3, "/static/cards/16.png"], "h4": ["4 of Hearts", 4, "/static/cards/17.png"],
                           "h5": ["5 of Hearts", 5, "/static/cards/18.png"], "h6": ["6 of Hearts", 6, "/static/cards/19.png"],
                           "h7": ["7 of Hearts", 7, "/static/cards/20.png"], "h8": ["8 of Hearts", 8, "/static/cards/21.png"],
                           "h9": ["9 of Hearts", 9, "/static/cards/22.png"], "h10": ["10 of Hearts", 10, "/static/cards/23.png"],
                           "h11": ["Jack of Hearts", 10, "/static/cards/24.png"],
                           "h12": ["Queen of Hearts", 10, "/static/cards/15.png"],
                           "h13": ["King of Hearts", 10, "/static/cards/26.png"],
                           "d1": ["Ace of diamonds", 11, "/static/cards/27.png"],
                           "d2": ["2 of diamonds", 2, "/static/cards/28.png"],
                           "d3": ["3 of diamonds", 3, "/static/cards/29.png"],
                           "d4": ["4 of diamonds", 4, "/static/cards/30.png"],
                           "d5": ["5 of diamonds", 5, "/static/cards/31.png"], "d6": ["6 of diamonds", 6, "/static/cards/32.png"],
                           "d7": ["7 of diamonds", 7, "/static/cards/33.png"], "d8": ["8 of diamonds", 8, "/static/cards/34.png"],
                           "d9": ["9 of diamonds", 9, "/static/cards/35.png"], "d10": ["10 of diamonds", 10, "/static/cards/36.png"],
                           "d11": ["Jack of diamonds", 10, "/static/cards/37.png"],
                           "d12": ["Queen of diamonds", 10, "/static/cards/38.png"],
                           "d13": ["King of diamonds", 10, "/static/cards/39.png"],
                           "c1": ["Ace of Clubs", 11, "/static/cards/40.png"], "c2": ["2 of Clubs", 2, "/static/cards/41.png"],
                           "c3": ["3 of Clubs", 3, "/static/cards/42.png"], "c4": ["4 of Clubs", 4, "/static/cards/43.png"],
                           "c5": ["5 of Clubs", 5, "/static/cards/44.png"], "c6": ["6 of Clubs", 6, "/static/cards/45.png"],
                           "c7": ["7 of Clubs", 7, "/static/cards/46.png"], "c8": ["8 of Clubs", 8, "/static/cards/47.png"],
                           "c9": ["9 of Clubs", 9, "/static/cards/48.png"], "c10": ["10 of Clubs", 10, "/static/cards/49.png"],
                           "c11": ["Jack of Clubs", 10, "/static/cards/50.png"],
                           "c12": ["Queen of Clubs", 10, "/static/cards/51.png"],
                           "c13": ["King of Clubs", 10, "/static/cards/52.png"]
                           }

    def generate_card(self):
        """Returns a random card's index"""
        return self.dict_of_card_values.keys()[randrange(0, 52)]

    def get_card_info(self, key):
        """Returns the list of information about that specific key"""
        return self.dict_of_card_values.get(key)
####### THIS WILL BE THE INSTANCE OF THE CARD
C = Card()


class Hand(models.Model):
    number_cards = models.PositiveIntegerField(default=0)
    value = models.PositiveIntegerField(default=0)
    cards = models.CharField(max_length=180)

    def __unicode__(self):
        return u"%s" % self.cards

    def get_cards(self):
        """This assume the string of cards is a comma separated list of key values for the card.
        It returns the cards as a list of key
        """
        cards = self.cards.split(' ')
        newcards = []
        for card in cards:
            newcards.append(C.get_card_info(card.strip(',')))

        return newcards

    def add_card(self, card):
        """Will add a card to a hand
        Simple checking to change ace to 1 if needed
        Will update number of cards as well as value of the hand
        """
        def ace_switched(cards, hand_value):
            """Will check to see if the ace has already been changed to 1"""
            value = 0
            for card in cards.split(" "):
                value = value + C.get_card_info(card.strip(","))[1]
            if hand_value == value:
                return True
            else:
                return False

        if self.number_cards is None:
            self.number_cards = 0
            self.value = 0
        self.number_cards += 1
        self.value += C.get_card_info(card)[1]
        #This will make sure that our string is formatted correctly
        if len(self.cards) == 0:
            self.cards = card
        else:
            self.cards = self.cards + ", " + card
        #This is where we should change the Ace if we need to
        if self.value > 21:
            for card in self.cards.split(" "):
                cinfo = C.get_card_info(card.strip(","))
                if (cinfo[0].split(' ')[0] == 'Ace') & ace_switched(self.cards, self.value):
                    self.value -= 10
                    break

    def get_value_of_hand(self):
        """Get hand value"""
        return self.value

    def get_number_of_cards(self):
        #Get number of cards
        return self.number_cards


class Player(models.Model):
    """The player will keep track of a single players game
        It will keep track of login information by extending the User model from django.
        It will keep track of the money, winning streak, longest winning streak, and bet(this should change often).
        It should also have a hand, which we will use a built in class for this object.
        """
    user = models.ForeignKey(User)
    money = models.DecimalField("Money", max_digits=7, decimal_places=2)
    winning_streak = models.PositiveIntegerField()
    longest_winning_streak = models.PositiveIntegerField()
    bet = models.PositiveIntegerField()
    hand = models.ForeignKey(Hand, null=True, blank=True, default=None)

    def __unicode__(self):
        """Returns the unicode for the Player object"""
        return u"%s" % self.user

    def lose(self):
        """Should do all the things to itself when it loses. remove bet from money, remove wining streak"""
        self.money -= self.bet
        self.winning_streak = 0
        self.save()

    def win(self):
        """Should do all the things to itself when it wins. add bet to money, increment winning streak, check longest
            winning streak and update"""
        self.money += self.bet
        self.winning_streak += 1
        if self.winning_streak > self.longest_winning_streak:
            self.longest_winning_streak = self.winning_streak
        self.save()



class Dealer(models.Model):
    """There should be a single dealer for a player, they should have a hand, and nothing else"""
    player = models.ForeignKey(Player)
    hand = models.ForeignKey(Hand)