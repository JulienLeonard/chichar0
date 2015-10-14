from google.appengine.api import users
from google.appengine.ext import ndb

class Book(ndb.Model):
    """A main model for representing a sequence of chapters."""
    name          = ndb.StringProperty(indexed=True)
    description   = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class Unit(ndb.Model):
    """A main model for representing a learnable unit (type is Chichar, Sentence or Word)."""
    unittype = ndb.StringProperty(indexed=False)
    unitkey  = ndb.StringProperty(indexed=False)
    date     = ndb.DateTimeProperty(auto_now_add=True)

class Chapter(ndb.Model):
    """A main model for representing a sequence of units to be trained."""
    name        = ndb.StringProperty(indexed=True)
    description = ndb.StringProperty(indexed=False)
    units       = ndb.StructuredProperty(Unit,repeated=True)
    book        = ndb.StructuredProperty(Book)
    date        = ndb.DateTimeProperty(auto_now_add=True)

class Chichar(ndb.Model):
    """A main model for representing a chichar."""
    chichar       = ndb.StringProperty(indexed=True)
    translation   = ndb.StringProperty(indexed=True)
    pronunciation = ndb.StringProperty(indexed=True)
    nstrokes      = ndb.StringProperty(indexed=True)
    strokes       = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class Sentence(ndb.Model):
    """A main model for representing a sentence."""
    chichar       = ndb.StringProperty(indexed=True)
    translation   = ndb.StringProperty(indexed=True)
    pronunciation = ndb.StringProperty(indexed=True)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    
class Word(ndb.Model):
    """A main model for representing a word."""
    chichar       = ndb.StringProperty(indexed=True)
    translation   = ndb.StringProperty(indexed=True)
    pronunciation = ndb.StringProperty(indexed=True)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    
class ViewStat(ndb.Model):
    """A main model for representing a vuew stat"""
    email         = ndb.StringProperty(indexed=True)
    chichar       = ndb.StructuredProperty(Chichar)
    sentence      = ndb.StructuredProperty(Sentence)
    date          = ndb.DateTimeProperty(auto_now_add=True)

class CharTest(ndb.Model):
    """A main model for representing a char test""" 
    email    = ndb.StringProperty(indexed=True)
    testtype = ndb.StringProperty(indexed=True)
    chichar  = ndb.StructuredProperty(Chichar)
    result   = ndb.StringProperty(indexed=True)
    date     = ndb.DateTimeProperty(auto_now_add=True)

