from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from sentencetemplates import *
from utils import *

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
            for chichar in sentence.charlist:
                chichars_query = Chichar.query(Chichar.chichar == chichar.chichar)
                qresult = chichars_query.fetch(1)
                if not len(qresult) == 0:
                    ochichar = qresult[0]
                    sentencelist = sentencelist + "<td><a href=\"/viewchichar/" + ochichar.key.urlsafe() + "\">" + ochichar.chichar + "</a></td>"
            sentencelist = sentencelist + "</tr>"
        sentencelist = sentencelist + "</table>"

        self.response.write(LIST_SENTENCE_TEMPLATE % sentencelist)

        self.response.write('</body></html>')
# [END ListSentences]


# [START LoadSentenceFile]
class LoadSentenceFile(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(LOAD_SENTENCES)

        self.response.write('</body></html>')
# [END LoadSentenceFile]

# [START LoadSentences]
class LoadSentences(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        sdict_name = self.request.get('dict_name', SENTENCEDICT)

        for sentence in self.request.get('sentences').split("\n"):
            if len(sentence) > 0:
                
                parts = sentence.split("\t")
                self.response.write("<div> new sentence</div>")
                for part in parts:
                    self.response.write("<div>  " + part + "</div>\n")

                if len(parts) == 3:
                    chichars  = lsubstract(list(parts[0].strip()),     [""," ","\n","\t",",","."])
                    pinyins   = lsubstract(parts[2].strip().split(" "),[""," ","\n","\t",",","."])
                    if not (len(chichars) == len(pinyins)):
                        self.response.write("<div>  error matching char " + "@".join(chichars) + " pynyin " + "@".join(pinyins) + "</div>\n")
                    else:
                        osentence = Sentence(parent=dict_key(sdict_name));
                        osentence.chichar        = parts[0].strip()
                        osentence.translation    = parts[1].strip()
                        osentence.pronunciation  = parts[2].strip()

                        charlist = []
                        cdict_name = self.request.get('dict_name', CHICHARDICT)
                        for (chi,pinyin) in zip(chichars,pinyins):
                            chichars_query = Chichar.query(Chichar.chichar == chi)
                            qresult = chichars_query.fetch(1)
                            if len(qresult) == 0:
                                self.response.write("need to add " + chi)
                                chichar = Chichar(parent=dict_key(cdict_name))
                                chichar.chichar        = chi
                                chichar.translation    = "TODO"
                                chichar.pronunciation  = pinyin
                                chichar.put()
                                charlist.append(chichar)
                            else:
                                charlist.append(qresult[0])
                            
            
                        osentence.charlist = charlist
                        osentence.put()


        self.response.write('</body></html>')

# [END LoadSentences]

# [START ClearSentences]
class ClearSentences(webapp2.RequestHandler):
    def post(self):
        sentence = Sentence()
        sentences_query = Sentence.query()
        sentences = sentences_query.fetch()
        
        for sentence in sentences:
            sentence.key.delete()

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
        for chichar10 in lsplit(sentence.charlist,10):
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
        save = self.request.get('save')
        cancel = self.request.get('cancel')
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
    

# [START DeleteSentence]
class DeleteSentence(webapp2.RequestHandler):
    def post(self,sentenceid):

        dict_name = self.request.get('dict_name', SENTENCEDICT)
        sentence_key = ndb.Key(urlsafe=sentenceid)
        # sentence = Sentence(parent=dict_key(dict_name));
        sentence = sentence_key.get()

        # removestats(self,sentence)

        sentence.key.delete()

        self.redirect("/listsentences")
# [END DeleteSentence]

