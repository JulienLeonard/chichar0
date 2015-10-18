from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from wordtemplates import *
from utils import *
from modelutils import *

def deleteword(request,wordid):
    dict_name   = request.request.get('dict_name', WORDDICT)
    word_key = ndb.Key(urlsafe=wordid)
    word     = word_key.get()
    word.key.delete()

def clearwords(request):
    words_query = Word.query()
    words       = words_query.fetch()
        
    for word in words:
        deleteword(request,word.key.urlsafe())

# [START ListWords]
class ListWords(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        sdict_name      = self.request.get('dict_name',WORDDICT)
        cdict_name      = self.request.get('dict_name',CHICHARDICT)

        words_query = Word.query(ancestor=dict_key(sdict_name)).order(-Word.date)
        words       = words_query.fetch()

        wordlist = ""
        wordlist = wordlist + "<table>"
        for word in words:
            wordlist = wordlist + "\n<tr><td>" + word.chichar  +" </td><td> " + word.translation + "</td>"
            for ochichar in getwordchichars(self,word):
                wordlist = wordlist + "<td><a href=\"/viewchichar/" + ochichar.key.urlsafe() + "\">" + ochichar.chichar + "</a></td>"
            viewwordform = "<form action=\"/viewword/" + word.key.urlsafe() + "\" method=\"get\"><div class=\"charaction\"><input type=\"submit\" value=\"+\"></div></form>"
            wordlist = wordlist + "<td>" + viewwordform + "</td>"
            wordlist = wordlist + "</tr>"
        wordlist = wordlist + "</table>"

        self.response.write(LIST_WORD_TEMPLATE % wordlist)

        self.response.write('</body></html>')
# [END ListWords]


# [END LoadWords]

def clearwords(request):
    word        = Word()
    words_query = Word.query()
    words       = words_query.fetch()
        
    for word in words:
        deleteword(request,word.key.urlsafe())
        

# [START ClearWords]
class ClearWords(webapp2.RequestHandler):
    def post(self):
        clearwords(self)
        self.redirect('/')
# [END ClearWords]

# [START ViewWord]
class ViewWord(webapp2.RequestHandler):
    def get(self,wordid):
        self.response.write('<html><body>')

        #dict_name = self.request.get('dict_name', WORDDICT)
        #word = Word(parent=dict_key(dict_name));


        dict_name      = self.request.get('dict_name',WORDDICT)
        word_key = ndb.Key(urlsafe=wordid)
        #sandy = sandy_key.get()
        #key = ndb.Key(Word, wordid)
        #words_query = Word.query(Word.key == key)
        #word        = words_query.fetch(1)[0]
        word = word_key.get()

        user = users.get_current_user()

        if user:
            udict_name = self.request.get('dict_name', USERDICT)
            viewstat = ViewStat(parent=dict_key(udict_name))
            viewstat.email    = user.email()
            viewstat.word  = word
            viewstat.put()

        
        wordchars = "<table>"
        for chichar10 in lsplit(getwordchichars(self,word),10):
            wordchars = wordchars + "<tr>"
            for lchichar in chichar10:
                chichars_query = Chichar.query(Chichar.chichar == lchichar.chichar)
                qresult = chichars_query.fetch(1)
                chichar = qresult[0]
                wordchars = wordchars + "<td><form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form></td>"
            wordchars = wordchars + "</tr>"
        wordchars = wordchars + "</table>"

        if not user == None and user.email() == ADMIN_ID:
            self.response.write(VIEW_WORD_ADMIN_TEMPLATE % ( word.chichar, word.pronunciation, word.translation, wordchars, word.key.urlsafe(),word.key.urlsafe()))
        else:
            self.response.write(VIEW_WORD_USER_TEMPLATE % ( word.chichar, word.pronunciation, word.translation, wordchars))
            

        self.response.write('</body></html>')
# [END ViewWord]

# [START AddWord]
class AddWord(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user == None and user.email() == ADMIN_ID:
            self.response.write('<html><body>')
            self.response.write(ADD_WORD_TEMPLATE)
            self.response.write('</body></html>')
        else:
            self.response.write('<html><body>Sorry, you must be ADMIN to access this page</body></html>')
# [END AddWord]

# [START DoAddWord]
class DoAddWord(webapp2.RequestHandler):
    def post(self):
        dict_name = self.request.get('dict_name', WORDDICT)
        word = Word(parent=dict_key(dict_name));
        word.chichar        = self.request.get('wordchichar')
        word.translation    = self.request.get('wordtranslation')
        word.pronunciation  = self.request.get('wordpronunciation')
        word.put()

        self.redirect("/viewword/" + word.key.urlsafe())
# [END DoAddWord]


# [START EditWord]
class EditWord(webapp2.RequestHandler):
    def get(self,wordid):
        self.response.write('<html><body>')

        dict_name = self.request.get('dict_name', WORDDICT)
        word_key = ndb.Key(urlsafe=wordid)
        # word = Word(parent=dict_key(dict_name));
        word = word_key.get()

        # Write the submission form and the footer of the page
        self.response.write(EDIT_WORD_TEMPLATE % ( word.key.urlsafe(), word.chichar, word.translation, word.pronunciation,word.key.urlsafe()))

        self.response.write('</body></html>')

# [END EditWord]

# [START SaveWord]
class SaveWord(webapp2.RequestHandler):
    def post(self,wordid):
        save      = self.request.get('save')
        cancel    = self.request.get('cancel')
        dict_name = self.request.get('dict_name', WORDDICT)
        word_key = ndb.Key(urlsafe=wordid)
        # word = Word(parent=dict_key(dict_name));
        word = word_key.get()
        
        if save:
            word.chichar        = self.request.get('word')
            word.translation    = self.request.get('translation')
            word.pronunciation  = self.request.get('pronunciation')
            word.put()

        self.redirect("/viewword/" + word.key.urlsafe())
# [END SaveWord]
    
def deleteword(request,wordid):
    dict_name   = request.request.get('dict_name', WORDDICT)
    word_key = ndb.Key(urlsafe=wordid)
    word     = word_key.get()
    word.key.delete()


# [START DeleteWord]
class DeleteWord(webapp2.RequestHandler):
    def post(self,wordid):
        deleteword(self,wordid)
        self.redirect("/listwords")
# [END DeleteWord]

# [START StatWords]
class StatWords(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        
        dict_name      = self.request.get('dict_name',WORDDICT)
        words_query = Word.query(ancestor=dict_key(dict_name)).order(-Word.date)
        words       = words_query.fetch()

        # Write the submission form and the footer of the page
        self.response.write(STAT_WORD_TEMPLATE % ( len(words) ))

        self.response.write('</body></html>')
# [END StatChiChars]

