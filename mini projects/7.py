# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cont=list()	# create Hand object

    def __str__(self):
       st="Hand contains "
       for card in self.cont:
            st+=str(card)+" "
       return st

    def add_card(self, card):
        self.cont.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value=0# compute the value of the hand, see Blackjack video
        flag=0
        for card in self.cont:	
            value+=VALUES[card.get_rank()]
            if card.get_rank()=="A" and flag==0:
                flag=1                
        if flag==1 and value+10<=21:
            value+=10
        return value            
            
    def draw(self, canvas, pos):
        for card in self.cont:	# draw a hand on the canvas, use the draw method for cards
            card.draw(canvas, pos)
            pos[0]+=1.5*CARD_SIZE[0]
            
# define deck class 
class Deck:
    def __init__(self):
        self.cont=list()	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cont.append(Card(suit, rank))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cont)    # use random.shuffle()

    def deal_card(self):
        return self.cont.pop()	# deal a card object from the deck
    
    def __str__(self):
       st="Deck contains "
       for card in self.cont:
            st+=str(card)+" "
       return st	# return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, pl_hand, dl_hand, score
    if in_play==True:
        outcome="You gave up and lost this round. New deal?"
        score-=1
        in_play=False
    else:
        deck=Deck()
        deck.shuffle()
        pl_hand=Hand()
        dl_hand=Hand()
        pl_hand.add_card(deck.deal_card())
        pl_hand.add_card(deck.deal_card())
        #print "player:"+str(pl_hand)
        dl_hand.add_card(deck.deal_card())
        dl_hand.add_card(deck.deal_card())  
        #print "dealer:"+str(dl_hand)
        outcome="Hit or stand?"
        in_play = True

def hit():
    # if the hand is in play, hit the player
    global in_play, pl_hand, deck, outcome, score
    if in_play==True and pl_hand.get_value()<=21:
        pl_hand.add_card(deck.deal_card())
        #print "player:"+str(pl_hand)
    # if busted, assign a message to outcome, update in_play and score
    if pl_hand.get_value()>21:
        outcome="You have busted. New deal?"
        #print outcome
        in_play=False
        score-=1
def stand():
    global in_play, dl_hand, pl_hand, score, outcome
    if in_play==False:
        st="You have busted. New deal?"
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    else:
        while dl_hand.get_value()<17:
           dl_hand.add_card(deck.deal_card()) 
        #print "dealer:"+str(dl_hand)
        if dl_hand.get_value()>21:
            st="You won! New deal?"
        else:
            #print "player:"+str(pl_hand)
            #print "dealer:"+str(dl_hand)
            if dl_hand.get_value()>=pl_hand.get_value():
                st="You lost. New deal?"
            else:
                st="You won! New deal?"            
    # assign a message to outcome, update in_play and score
    outcome=st
    if outcome=="You won! New deal?":
        score+=1
    else:
        score-=1
    in_play=False
    #print outcome
# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [50,50], 25, "Orange")
    canvas.draw_text(outcome, [175, 260], 20, "Orange")
    canvas.draw_text("Score:"+str(score), [300, 50], 25, "Red")
    canvas.draw_text("Dealer:", [100, 85], 20, "Orange")
    canvas.draw_text("Player:", [100, 260], 20, "Orange")
    dl_hand.draw(canvas, [100, 100])
    pl_hand.draw(canvas, [100, 300])
    if in_play==True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100+CARD_BACK_CENTER[0], 100+CARD_BACK_CENTER[1]], CARD_SIZE)
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric