import os
import unittest

from playingcards import Card
from playingcards import Stack

class testCardsClass(unittest.TestCase):
  def setUp(self):
    self.modpath=os.path.abspath(os.path.dirname(__file__))

  def test_correct_card(self):
    c=Card(7,False)
    self.assertEqual(c.name(),"Seven of Spades")

  def test_correct_index(self):
    c=Card(7,False)
    self.assertEqual(c.index,7)

  def test_correct_suit(self):
    c=Card(15,False)
    self.assertEqual(c.suit(),"Diamonds")

  def test_facedown(self):
    c=Card(7,True)
    self.assertEqual(c.name(),"Facedown")

  def test_isdown(self):
    c=Card(7,True)
    self.assertEqual(c.isdown(),True)

  def test_imgfile(self):
    c=Card(7,False)
    ipath=os.path.abspath(os.path.join(self.modpath,"img"))
    ifn=os.path.join(ipath,"7.png")
    bfn=os.path.join(ipath,"back.png")
    imgfn=c.image()
    if imgfn == ifn:
      c.flip()
      imgfn=c.image()
      self.assertEqual(imgfn,bfn)
    else:
      self.assertEqual(imgfn,ifn)

  def test_stacklength(self):
    s=Stack(1)
    self.assertEqual(s.length(),52)

  def test_stack(self):
    s=Stack(1)
    self.assertEqual(s.topcard().name(),"Ace of Spades")

  def test_noaces(self):
    s=Stack(noaces=1)
    self.assertEqual(s.topcard().name(),"Two of Spades")

  def test_get_bottom_card(self):
    s=Stack(1)
    c=s.getbottomcard()
    l=s.length()
    if l < 52:
      self.assertEqual(c.name(),"King of Clubs")
    else:
      self.assertEqual(l,51)

  def test_getncards(self):
    s=Stack(1)
    cs=s.getncards(5)
    l=s.length()
    if l < 48:
      self.assertEqual(len(cs),5)
    else:
      self.assertEqual(l,47)

  def test_addncards(self):
    s=Stack(1)
    cs=s.getncards(5)
    l=s.length()
    if l < 48:
      s.addncards(cs)
      self.assertEqual(s.length(),52)
    else:
      self.assertEqual(l,47)
