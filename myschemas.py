from google.appengine.api import users
from google.appengine.ext import ndb


class Chichar(ndb.Model):
    """A main model for representing a chichar."""
    chichar       = ndb.StringProperty(indexed=True)
    translation   = ndb.StringProperty(indexed=False)
    pronunciation = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)


class Sentence(ndb.Model):
    """A main model for representing a sentence."""
    chichar       = ndb.StringProperty(indexed=False)
    translation   = ndb.StringProperty(indexed=False)
    pronunciation = ndb.StringProperty(indexed=False)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    charlist      = ndb.StructuredProperty(Chichar,repeated=True)


class ViewStat(ndb.Model):
    """A main model for representing a vuew stat"""
    email         = ndb.StringProperty(indexed=True)
    chichar       = ndb.StructuredProperty(Chichar)
    sentence      = ndb.StructuredProperty(Sentence)
    date          = ndb.DateTimeProperty(auto_now_add=True)
