# Author: Christopher Allison
# Copyright: 2016 Christopher Allison

"""
A module to ease the creation of card games in written in python

The Card class is the representation of a single card, including it's
image and the back image.

The Stack class is the representation of a stack of playing cards.

To Use:
from playingcards import Card
from playingcards import Stack
"""

import os.path
import random

class Card:
  """Representation of a Playing Card"""
  def __init__(self,index,facedown=False):
    """Set up the card

    index: card number between 1 and 51 - 1=Ace of Spades, 15=Two of Diamonds, 27=Ace of Hearts, 40=Two of Clubs
    facedown: True or False, default False - when facedown operations that return the image of the card or 
              a string representation of the card return the image of the back of the card or the string 'Facedown'
    """
    self.cardnames=["Back","Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
    modpath=os.path.abspath(os.path.dirname(__file__))
    self.imgdir=os.path.join(modpath,"img")
    self.imgfile=""
    self.backimg=""
    self.facedown=facedown
    self.index=index
    if self.index<14:
      self.suitname="Spades"
      self.value=index
    elif self.index<27:
      self.suitname="Diamonds"
      self.value=index-13
    elif self.index<40:
      self.suitname="Hearts"
      self.value=index-26
    else:
      self.suitname="Clubs"
      self.value=index-39
    self.cardname=self.cardnames[self.value]
    self.imgfn="%d.png" % index
    if os.path.isdir(self.imgdir):
      imgpath=os.path.join(self.imgdir,self.imgfn)
      self.backimg=os.path.join(self.imgdir,"back.png")
      if os.path.exists(imgpath):
        self.imgfile=imgpath

  def name(self):
    """Return a string representation of the card or 'Facedown' if the card is facedown

    input: none
    return: string
    """
    if self.facedown:
      return "Facedown"
    return "%s of %s" % (self.cardname,self.suitname)

  def suit(self):
    """Return the suit of the card as string

    input: none
    return: string
    """
    return self.suitname

  def indexname(self):
    """Return a string representation of the value of the card

    input: none
    return: string
    """
    return self.cardname

  def image(self):
    """Return the fully-qualified path name of the image file
       representing this card

    input: none
    return: string (filename)
    """
    if self.facedown:
      return self.backimg
    return self.imgfile

  def flip(self):
    """Flips the card
       Returns the fully-qualified path name of the image file
       representing either the card face or the back of the card

    input: none
    return: string (filename)
    """
    self.facedown=False if self.facedown else True
    return self.image()

  def isdown(self):
    """Returns True if card is currently facedown

    input: none
    returns: boolean
    """
    return self.facedown

class Stack:
  """Representation of a stack of playing cards"""
  def __init__(self,numberofdecks=0,noaces=0):
    """Setup the stack

    numberofdecks: if >0 then the stack will be initialised with that number of 
                   decks of cards.
    noaces: if >0 then the stack will be initialised with
            a full deck of cards minus the Aces.

    If both numberofdecks and noaces are used together then a deck of 100 cards
    will be created with only 4 Aces in it (probably not what you want).
    """
    self.cards=[]
    if numberofdecks>0:
      self.initfull(numberofdecks)
    if noaces>0:
      self.initnoaces()
    random.seed()

  def addnewcard(self,index):
    """Creates a new Card and adds it to the bottom of the Stack

    index: Card number 1-51
    returns: None
    """
    self.cards.append(Card(index))

  def addcard(self,card):
    """Adds the card to the bottom of the Stack

    card: Card to add to the Stack
    returns: None
    """
    self.cards.append(card)

  def addtopcard(self,card):
    """Adds the card to the top of the Stack

    card: Card to add the Stack
    returns: None
    """
    self.cards.insert(0,card)

  def initfull(self,numberofdecks=1):
    """Initialises the Stack with the required number of cards

    numberofdecks: integer - This number of 52 card decks will be setup
    returns: None
    """
    for y in range(numberofdecks):
      for x in range(1,53):
        self.addnewcard(x)

  def initnoaces(self):
    """Initialiases the Stack with a full deck minus the Aces

    input: None
    returns: None
    """
    self.initfull(1)
    t=[]
    t=self.getcard(39)
    t=self.getcard(26)
    t=self.getcard(13)
    t=self.getcard(0)
    t=None

  def length(self):
    """Returns the number of cards in the stack

    input: None
    returns: integer
    """
    return len(self.cards)

  def shuffle(self):
    """Randomises the order of the cards in the stack

    input: None
    returns: None
    """
    random.shuffle(self.cards)

  def topcard(self):
    """Returns the top card without removing it from the Stack

    input: None
    returns: Card
    """
    if len(self.cards):
      return self.cards[0]
    return None

  def bottomcard(self):
    """Returns the bottom card without removing it from the Stack

    input: None
    returns: Card
    """
    if len(self.cards):
      return self.cards[len(self.cards)-1]
    return None

  def getbottomcard(self):
    """Returns the bottom card removing it from the Stack

    input: None
    returns: Card
    """
    if len(self.cards):
      return self.cards.pop()
    return None

  def gettopcard(self):
    """Returns the top card removing it from the Stack

    input: None
    returns: Card
    """
    l=len(self.cards)
    if l:
      c=self.topcard()
      self.cards=self.cards[1:]
      return c
    return None

  def getcard(self,index):
    """Returns the n card and removes it from the Stack
       if index > len(self.cards) then None is returned

    index: card number to remove from the stack (0 based)
    returns: Card or None
    """
    l=len(self.cards)
    if l>index:
      c=self.cards[index]
      if index > 0:
        t=self.cards[:index]
        t.extend(self.cards[index+1:])
        self.cards=t
      else:
        self.cards=self.cards[1:]
      return c
    return None

  def getncards(self,n):
    """Returns the top n cards and removes them from the Stack
       If n > len(self.cards) then len(self.cards) cards are
       returned (or None if there are no cards in this Stack)

    n: number of cards to remove
    returns: [Cards]
    """
    l=len(self.cards)
    if l>n:
      t=self.cards[:n]
      self.cards=self.cards[n:]
    else:
      t=self.cards
      self.cards=[]
    return t

  def addncards(self,ncards):
    """Adds the list of cards to the bottom of this Stack

    ncards: [Cards]
    returns: None
    """
    if len(ncards) > 0:
      for card in ncards:
        self.addcard(card)

  def status(self):
    """Returns a string representation of the status of this Stack
       <number of cards in Stack> Card name of top card

       i.e. "12 cards: Five of Clubs"

    input: None
    returns: String
    """
    c=self.topcard()
    if c!=None:
      s=c.name()
    else:
      s=""
    return "%d cards: %s" % (self.length(),s)
