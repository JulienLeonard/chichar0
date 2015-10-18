from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from sentencetemplates import *
from utils import *
from modelutils import *

# [START ListSentences]
class ListSentences(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        sdict_name      = self.request.get('dict_name',SENTENCEDICT)
        cdict_name      = self.request.get('dict_name',CHICHARDICT)

        sentences_query = Sentence.query(ancestor=dict_key(sdict_name)).order(-Sentence.date)
        sentences       = sentences_query.fetch()

        sentencelist = ""
        sentencelist = sentencelist + "<table>"
        for sentence in sentences:
            sentencelist = sentencelist + "\n<tr><td>" + sentence.chichar  +" </td><td> " + sentence.translation + "</td>"
            for ochichar in getsentencechichars(self,sentence):
                sentencelist = sentencelist + "<td><a href=\"/viewchichar/" + ochichar.key.urlsafe() + "\">" + ochichar.chichar + "</a></td>"
            viewsentenceform = "<form action=\"/viewsentence/" + sentence.key.urlsafe() + "\" method=\"get\"><div class=\"charaction\"><input type=\"submit\" value=\"+\"></div></form>"
            sentencelist = sentencelist + "<td>" + viewsentenceform + "</td>"
            sentencelist = sentencelist + "</tr>"
        sentencelist = sentencelist + "</table>"

        self.response.write(LIST_SENTENCE_TEMPLATE % sentencelist)

        self.response.write('</body></html>')
# [END ListSentences]


def clearsentences(request):
    sentence        = Sentence()
    sentences_query = Sentence.query()
    sentences       = sentences_query.fetch()
        
    for sentence in sentences:
        deletesentence(request,sentence.key.urlsafe())
        

# [START ClearSentences]
class ClearSentences(webapp2.RequestHandler):
    def post(self):
        clearsentences(self)
        self.redirect('/')
# [END ClearSentences]

# [START ViewSentence]
class ViewSentence(webapp2.RequestHandler):
    def get(self,sentenceid):
        self.response.write('<html><body>')

        #dict_name = self.request.get('dict_name', SENTENCEDICT)
        #sentence = Sentence(parent=dict_key(dict_name));


        dict_name      = self.request.get('dict_name',SENTENCEDICT)
        sentence_key = ndb.Key(urlsafe=sentenceid)
        #sandy = sandy_key.get()
        #key = ndb.Key(Sentence, sentenceid)
        #sentences_query = Sentence.query(Sentence.key == key)
        #sentence        = sentences_query.fetch(1)[0]
        sentence = sentence_key.get()

        user = users.get_current_user()

        if user:
            udict_name = self.request.get('dict_name', USERDICT)
            viewstat = ViewStat(parent=dict_key(udict_name))
            viewstat.email    = user.email()
            viewstat.sentence  = sentence
            viewstat.put()

        
        sentencechars = "<table>"
        for chichar10 in lsplit(getsentencechichars(self,sentence),10):
            sentencechars = sentencechars + "<tr>"
            for lchichar in chichar10:
                chichars_query = Chichar.query(Chichar.chichar == lchichar.chichar)
                qresult = chichars_query.fetch(1)
                chichar = qresult[0]
                sentencechars = sentencechars + "<td><form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form></td>"
            sentencechars = sentencechars + "</tr>"
        sentencechars = sentencechars + "</table>"

        if not user == None and user.email() == ADMIN_ID:
            self.response.write(VIEW_SENTENCE_ADMIN_TEMPLATE % ( sentence.chichar, sentence.pronunciation, sentence.translation, sentencechars, sentence.key.urlsafe(),sentence.key.urlsafe()))
        else:
            self.response.write(VIEW_SENTENCE_USER_TEMPLATE % ( sentence.chichar, sentence.pronunciation, sentence.translation, sentencechars))
            

        self.response.write('</body></html>')
# [END ViewSentence]

# [START AddSentence]
class AddSentence(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user == None and user.email() == ADMIN_ID:
            self.response.write('<html><body>')
            self.response.write(ADD_SENTENCE_TEMPLATE)
            self.response.write('</body></html>')
        else:
            self.response.write('<html><body>Sorry, you must be ADMIN to access this page</body></html>')
# [END AddSentence]

# [START DoAddSentence]
class DoAddSentence(webapp2.RequestHandler):
    def post(self):
        dict_name = self.request.get('dict_name', SENTENCEDICT)
        sentence = Sentence(parent=dict_key(dict_name));
        sentence.chichar        = self.request.get('sentencechichar')
        sentence.translation    = self.request.get('sentencetranslation')
        sentence.pronunciation  = self.request.get('sentencepronunciation')
        sentence.put()

        self.redirect("/viewsentence/" + sentence.key.urlsafe())
# [END DoAddSentence]


# [START EditSentence]
class EditSentence(webapp2.RequestHandler):
    def get(self,sentenceid):
        self.response.write('<html><body>')

        dict_name = self.request.get('dict_name', SENTENCEDICT)
        sentence_key = ndb.Key(urlsafe=sentenceid)
        # sentence = Sentence(parent=dict_key(dict_name));
        sentence = sentence_key.get()

        # Write the submission form and the footer of the page
        self.response.write(EDIT_SENTENCE_TEMPLATE % ( sentence.key.urlsafe(), sentence.chichar, sentence.translation, sentence.pronunciation,sentence.key.urlsafe()))

        self.response.write('</body></html>')

# [END EditSentence]

# [START SaveSentence]
class SaveSentence(webapp2.RequestHandler):
    def post(self,sentenceid):
        save      = self.request.get('save')
        cancel    = self.request.get('cancel')
        dict_name = self.request.get('dict_name', SENTENCEDICT)
        sentence_key = ndb.Key(urlsafe=sentenceid)
        # sentence = Sentence(parent=dict_key(dict_name));
        sentence = sentence_key.get()
        
        if save:
            sentence.chichar        = self.request.get('sentence')
            sentence.translation    = self.request.get('translation')
            sentence.pronunciation  = self.request.get('pronunciation')
            sentence.put()

        self.redirect("/viewsentence/" + sentence.key.urlsafe())
# [END SaveSentence]
    
def deletesentence(request,sentenceid):
    dict_name   = request.request.get('dict_name', SENTENCEDICT)
    sentence_key = ndb.Key(urlsafe=sentenceid)
    sentence     = sentence_key.get()
    sentence.key.delete()


# [START DeleteSentence]
class DeleteSentence(webapp2.RequestHandler):
    def post(self,sentenceid):
        deletesentence(self,sentenceid)
        self.redirect("/listsentences")
# [END DeleteSentence]

# [START StatSentences]
class StatSentences(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        
        dict_name      = self.request.get('dict_name',SENTENCEDICT)
        sentences_query = Sentence.query(ancestor=dict_key(dict_name)).order(-Sentence.date)
        sentences       = sentences_query.fetch()

        # Write the submission form and the footer of the page
        self.response.write(STAT_SENTENCE_TEMPLATE % ( len(sentences) ))

        self.response.write('</body></html>')
# [END StatChiChars]
