import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from myadmin     import *

from utils       import *
from chichar     import *
from sentence    import *
from word        import *
from viewstat    import *
from chartest    import *
from drawing     import *

from maintemplates import *

# [BEGIN main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        if not user == None and user.email() == ADMIN_ID:
            self.response.write(MAIN_PAGE_ADMIN_TEMPLATE % (url, url_linktext))
        else:
            self.response.write(MAIN_PAGE_USER_TEMPLATE % (url, url_linktext))

        self.response.write('</body></html>')
# [END main_page]

def tableclickchichars(chichars):
    result = "<table>"
    for chichar10 in lsplit(chichars,10):
        result += "<tr>"
        for chichar in chichar10:
            result += "<td>"
            result += "<form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form>"
            result += "</td>"
        result += "</tr>"
    result += "<table>"
    return result

# [BEGIN main_page]
class MainSearch(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        string = self.request.get('searchquery')

        if string == "":
            string = ""
            chars = ""
            words = ""
            sentences = ""
        else:
            chichars_query = Chichar.query(Chichar.chichar == string)
            qresult = chichars_query.fetch()
            if len(qresult) > 0:
                chars = tableclickchichars(qresult)
            else:
                chichars_query = Chichar.query(Chichar.translation == string)
                qresult = chichars_query.fetch()
                if len(qresult) > 0:
                    chars = tableclickchichars(qresult)
                else:
                    chichars_query = Chichar.query(Chichar.pronunciation == string)
                    qresult = chichars_query.fetch()
                    if len(qresult) > 0:
                        chars = tableclickchichars(qresult)
                    else:
                        if len(string) == 1:
                            chars = "char unknown, to be added"
                        else:
                            chars = "no result"

            words = "TODO"
            sentences = "TODO"

        self.response.write( SEARCH_GENERAL % (string, chars, words, sentences ) )
        self.response.write('</body></html>')
# [END main_page]

# [BEGIN main_page]
class MainLoad(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(LOAD_GENERAL)

        self.response.write('</body></html>')
# [END main_page]


def checkaddchar(request,chi,translation,pronunciation):
    cdict_name = request.request.get('dict_name', CHICHARDICT)
    chichars_query = Chichar.query(Chichar.chichar == chi)
    qresult = chichars_query.fetch(1)

    charresult = None
    if len(qresult) == 0:
        request.response.write("need to add " + chi)
        chichar = Chichar(parent=dict_key(cdict_name))
        chichar.chichar        = chi
        chichar.translation    = translation
        chichar.pronunciation  = pronunciation
        chichar.put()
        charresult = chichar
    else:
        # TODO:check everything is the same  
        request.response.write("char " + chi + " already known")
        charresult = qresult[0]
    return charresult

def checkaddsentence(request,chi,translation,pronunciation):
    sdict_name = request.request.get('dict_name', SENTENCEDICT)
    sentences_query = Sentence.query(Sentence.chichar == chi)
    qresult = sentences_query.fetch(1)
    if len(qresult) == 0:
        charlist = []
        chichars  = lsubstract(list(chi.strip()),     [""," ","\n","\t",",","."])
        pinyins   = lsubstract(pronunciation.strip().split(" "),[""," ","\n","\t",",","."])
        if not (len(chichars) == len(pinyins)):
            request.response.write("<div>  error matching char " + "@".join(chichars) + " pynyin " + "@".join(pinyins) + "</div>\n")
        else:
            request.response.write("need to add sentence " + chi)
            osentence = Sentence(parent=dict_key(sdict_name));
            osentence.chichar        = chi
            osentence.translation    = translation
            osentence.pronunciation  = pronunciation

            for (chi,pinyin) in zip(chichars,pinyins):
                char = checkaddchar(request,chi,None,pinyin)
                charlist.append(char)
            osentence.charlist = charlist
            osentence.put()
    else:
        request.response.write("sentence " + chi + " already known")
    

def checkaddword(request,chi,translation,pronunciation):
    wdict_name = request.request.get('dict_name', WORDDICT)
    words_query = Word.query(Word.chichar == chi)
    qresult = words_query.fetch(1)
    if len(qresult) == 0:
        charlist = []
        chichars  = lsubstract(list(chi.strip()),     [""," ","\n","\t",",","."])
        pinyins   = lsubstract(pronunciation.strip().split(" "),[""," ","\n","\t",",","."])
        if not (len(chichars) == len(pinyins)):
            request.response.write("<div>  error matching char " + "@".join(chichars) + " pynyin " + "@".join(pinyins) + "</div>\n")
        else:
            request.response.write("need to add word " + chi)
            oword = Word(parent=dict_key(wdict_name));
            oword.chichar        = chi
            oword.translation    = translation
            oword.pronunciation  = pronunciation

            for (chi,pinyin) in zip(chichars,pinyins):
                char = checkaddchar(request,chi,None,pinyin)
                charlist.append(char)
            oword.charlist = charlist
            oword.put()
    else:
        request.response.write("word " + chi + " already known")
    


# [BEGIN main_page]
class DoMainLoad(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        for dataline in self.request.get('dataentry').split("\n"):
            if len(dataline) > 0:
                parts = dataline.split(";")
                chichar       = parts[0].strip()
                translation   = parts[1].strip()
                pronunciation = parts[2].strip()
            
                if len(chichar) == 1:
                    # this is a new char
                    checkaddchar(self,chichar,translation,pronunciation)
                else:
                    if len(translation.split(" ")) > 1:
                        # this is a sentence
                        checkaddsentence(self,chichar,translation,pronunciation)
                    else:
                        checkaddword(self,chichar,translation,pronunciation)

        self.response.write('</body></html>')
# [END main_page]

# [BEGIN main_page]
class MainClear(webapp2.RequestHandler):
    def post(self):

        clearchichars(self)
        clearwords(self)
        clearsentences(self)

        user = users.get_current_user()

        if user:
            clearviewstats(self)
            clearchartests(self)

        self.redirect("/")

# [END main_page]



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/mainsearch',           MainSearch),
    ('/mainsearch/(.*)',      MainSearch),
    ('/mainload',             MainLoad),
    ('/domainload',           DoMainLoad),
    ('/mainclear',            MainClear),

    ('/listchichars',         ListChiChar),
    ('/addchichar',           AddChiChar),
    ('/doaddchichar',         DoAddChiChar),
    ('/viewchichar/(.*)',     ViewChiChar),
    ('/editchichar/(.*)',     EditChiChar),
    ('/savechichar/(.*)',     SaveChiChar),
    ('/deletechichar/(.*)',   DeleteChiChar),
    ('/clearchichars',        ClearChiChars),
    ('/loadchiccharfile',     LoadChicharFile),
    ('/loadchichars',         LoadChichars),
    ('/statchichars',         StatChiChars),
    ('/chicharsentences/(.*)',ChiCharSentences),

    ('/listsentences',        ListSentences),
    ('/addsentence',          AddSentence),
    ('/doaddsentence',        DoAddSentence),
    ('/viewsentence/(.*)',    ViewSentence),
    ('/editsentence/(.*)',    EditSentence),
    ('/savesentence/(.*)',    SaveSentence),
    ('/deletesentence/(.*)',  DeleteSentence),
    ('/clearsentences',       ClearSentences),
    ('/loadsentencefile',     LoadSentenceFile),
    ('/loadsentences',        LoadSentences),
    ('/statsentences',        StatSentences),

    ('/listwords',        ListWords),
    ('/addword',          AddWord),
    ('/doaddword',        DoAddWord),
    ('/viewword/(.*)',    ViewWord),
    ('/editword/(.*)',    EditWord),
    ('/saveword/(.*)',    SaveWord),
    ('/deleteword/(.*)',  DeleteWord),
    ('/clearwords',       ClearWords),
    ('/loadwordfile',     LoadWordFile),
    ('/loadwords',        LoadWords),
    ('/statwords',        StatWords),

    ('/char2pinyintest',      Char2PinyinTest),
    ('/def2chartest',         Def2CharTest),
    ('/checkchar2pinyintest', CheckChar2PinyinTest),
    ('/checkdef2chartest',    CheckDef2CharTest),
    ('/charteststats',        CharTestStats),

    ('/listviewstats',        ListViewStats),
    ('/clearviewstats',       ClearViewStats),

    ('/sandboxdraw',          SandboxDraw),

], debug=True)
