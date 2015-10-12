from google.appengine.api import users
from google.appengine.ext import ndb

CHICHARDICT  = 'chichardict'
SENTENCEDICT = 'sentencedict'
WORDDICT = 'worddict'
USERDICT     = 'userdict'

def dict_key(dict_name=CHICHARDICT):
    """Constructs a Datastore key for a Dict entity.
    We use Dict_name as the key.
    """
    return ndb.Key('Dict', dict_name)
