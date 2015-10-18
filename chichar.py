from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts          import *
from chichartemplates import *
from myschemas        import *
from myadmin          import *
from modelutils       import *

from viewstat         import *

from utils import *

# [START chicharlist]
def chicharlist(request,detailed=False):
    # [START query]
    dict_name      = request.request.get('dict_name',CHICHARDICT)
    chichars_query = Chichar.query(ancestor=dict_key(dict_name)).order(-Chichar.date)
    chichars       = chichars_query.fetch()
    # [END query]

    charlist = ""
    if not detailed:
        for chichar in chichars:
            charlist = charlist + " " + chichar.chichar
    else:
        charlist = charlist + "<table>"
        for rowchichars in lsplit(chichars,10):
            charlist = charlist + "\n<tr>"
            for chichar in rowchichars:
                charlist = charlist + "<td><form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form></td>"
            charlist = charlist + "</tr>"
        charlist = charlist + "</table>"

    return charlist
# [END chicharlist]
    
# [START ListChiChar]
class ListChiChar(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        charlist = chicharlist(self,True)

        # Write the submission form and the footer of the page
        self.response.write(LIST_CHI_CHAR_TEMPLATE % charlist)

        self.response.write('</body></html>')
# [END ListChiChar]

# [START AddChiChar]
class AddChiChar(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user == None and user.email() == ADMIN_ID:
            self.response.write('<html><body>')
            charlist = chicharlist(self)
            self.response.write(ADD_CHI_CHAR_TEMPLATE % charlist)
            self.response.write('</body></html>')
        else:
            self.response.write('<html><body>Sorry, you must be ADMIN to access this page</body></html>')
# [END AddChiChar]

# [START DoAddChiChar]
class DoAddChiChar(webapp2.RequestHandler):
    def post(self):
        char           = self.request.get('chichar')
        translation    = self.request.get('translation')
        pronunciation  = self.request.get('pronunciation')
        chichar = addchichar(self,char,translation,pronunciation)
        self.redirect("/viewchichar/" + chichar.key.urlsafe())
# [END DoAddChiChar]

def clearchichars(request):
    chichar = Chichar()
    chichars_query = Chichar.query()
    chichars = chichars_query.fetch()
        
    for chichar in chichars:
        deletechichar(request,chichar.key.urlsafe())
        

# [START ClearChiChars]
class ClearChiChars(webapp2.RequestHandler):
    def post(self):
        clearchichars()
        self.redirect('/')
# [END ClearChiChars]


# [START ViewChiChar]
class ViewChiChar(webapp2.RequestHandler):
    def get(self,chicharid):
        self.response.write('<html><body>')

        #dict_name = self.request.get('dict_name', CHICHARDICT)
        #chichar = Chichar(parent=dict_key(dict_name));


        dict_name      = self.request.get('dict_name',CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        #sandy = sandy_key.get()
        #key = ndb.Key(Chichar, chicharid)
        #chichars_query = Chichar.query(Chichar.key == key)
        #chichar        = chichars_query.fetch(1)[0]
        chichar = chichar_key.get()

        user = users.get_current_user()

        if user:
            udict_name = self.request.get('dict_name', USERDICT)
            viewstat = ViewStat(parent=dict_key(udict_name))
            viewstat.email    = user.email()
            viewstat.chichar  = chichar
            viewstat.put()

        if not user == None and user.email() == ADMIN_ID:
            self.response.write(VIEW_CHI_CHAR_ADMIN_TEMPLATE % ( chichar.chichar, chichar.pronunciation, chichar.translation, chichar.key.urlsafe(),chichar.key.urlsafe(),chichar.key.urlsafe(),chichar.key.urlsafe()))
        else:
            self.response.write(VIEW_CHI_CHAR_USER_TEMPLATE % ( chichar.chichar, chichar.pronunciation, chichar.translation, chichar.key.urlsafe()))
            

        self.response.write('</body></html>')
# [END ViewChiChar]

# [START EditChiChar]
class EditChiChar(webapp2.RequestHandler):
    def get(self,chicharid):
        self.response.write('<html><body>')

        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()

        # Write the submission form and the footer of the page
        self.response.write(EDIT_CHI_CHAR_TEMPLATE % ( chichar.key.urlsafe(), chichar.chichar, chichar.pronunciation, chichar.translation,chichar.key.urlsafe()))

        self.response.write('</body></html>')

# [END EditChiChar]

# [START SaveChiChar]
class SaveChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        save = self.request.get('save')
        cancel = self.request.get('cancel')
        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()
        
        if save:
            chichar.chichar        = self.request.get('chichar')
            chichar.translation    = self.request.get('translation')
            chichar.pronunciation  = self.request.get('pronunciation')
            chichar.put()

        self.redirect("/viewchichar/" + chichar.key.urlsafe())
# [END SaveChiChar]
    
def deletechichar(request,chicharid):
    dict_name   = request.request.get('dict_name', CHICHARDICT)
    chichar_key = ndb.Key(urlsafe=chicharid)
    chichar     = chichar_key.get()
    chichar.key.delete()
    

# [START DeleteChiChar]
class DeleteChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        deletechichar(self,chicharid)
        self.redirect("/listchichars")

# [END DeleteChiChar]

# [START StatChiChars]
class StatChiChars(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        
        chichars       = getallchichars(self)

        chicharfreq = {}
        for chichar in chichars:
            chicharfreq[chichar.chichar] = 0

        sentences = getallsentences(self)
        for sentence in sentences:
            for chichar in getsentencechichars(self,sentence):
                chicharfreq[chichar.chichar] += 1

        sortlist = [(chicharfreq[char],char) for char in chicharfreq.keys()]
        sortlist.sort()

        charfreq = "<table>"
        for freqchar5 in lsplit(lreverse(sortlist),5):
            charfreq = charfreq + "<tr>"
            for (freq,char) in freqchar5:
                chichar = getchichar(self,char)
                charform = "<form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form>"
                charfreq = charfreq + "<td>" + charform + "</td><td> </td><td>" + str(freq) + "</td> <td></td>"
            charfreq = charfreq + "</tr>"
        charfreq = charfreq + "<table>"    

        # Write the submission form and the footer of the page
        self.response.write(STAT_CHI_CHAR_TEMPLATE % ( len(chichars), charfreq ))

        self.response.write('</body></html>')
# [END StatChiChars]

# [START ChiCharSentences]
class ChiCharSentences(webapp2.RequestHandler):
    def get(self,chicharid):
        self.response.write('<html><body>')

        chichar_key = ndb.Key(urlsafe=chicharid)
        chichar     = chichar_key.get()

        sdict_name      = self.request.get('dict_name',SENTENCEDICT)
        sentences_query = Sentence.query(ancestor=dict_key(sdict_name)).order(Sentence.date)
        sentences       = sentences_query.fetch()

        sentencelist = ""
        sentencelist = sentencelist + "<table>"
        for sentence in sentences:
            if chichar.chichar in sentence.chichar:
                sentenceform = "    <form action=\"/viewsentence/" + sentence.key.urlsafe() + "\" method=\"get\"><input type=\"submit\" value=\"+\"/></form>"
                sentencelist = sentencelist + "\n<tr><td>" + sentence.chichar  + "</td><td>" + sentence.translation + "</td><td>" + sentenceform + "</td></tr>"
        sentencelist = sentencelist + "</table>"
        
        self.response.write(CHI_CHAR_SENTENCES_TEMPLATE % ( chichar.chichar, sentencelist, chicharid) )
        self.response.write('</body></html>')
# [END ChiCharSentences]

# [START LoadChicharFile]
class LoadChicharFile(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(LOAD_CHICHARS)

        self.response.write('</body></html>')
# [END LoadChicharFile]

# [START LoadChichars]
class LoadChichars(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        sdict_name = self.request.get('dict_name', CHICHARDICT)

        for chicharline in self.request.get('chichars').split("\n"):
            if len(chicharline) > 0:                
                parts = chicharline.split(";")
                self.response.write("<div> new chichar</div>")
                for part in parts:
                    self.response.write("<div>  " + part + "</div>\n")

                if len(parts) == 3:

                    chi           = parts[0].strip()
                    translation   = parts[1].strip()
                    pronunciation = parts[2].strip()

                    cdict_name = self.request.get('dict_name', CHICHARDICT)
                    chichars_query = Chichar.query(Chichar.chichar == chi)
                    qresult = chichars_query.fetch(1)

                    if len(qresult) == 0:
                        self.response.write("need to add " + chi)
                        chichar = Chichar(parent=dict_key(cdict_name))
                        chichar.chichar        = chi
                        chichar.translation    = translation
                        chichar.pronunciation  = pronunciation
                        chichar.put()
                    else:
                    # TODO:check everything is the same  
                        self.response.write("char " + chi + " already known")
                        

        self.response.write('</body></html>')

# [END LoadChichars]


# [START StrokeChiChar]
class StrokeChiChar(webapp2.RequestHandler):
    def get(self,chicharid):
        self.response.write('<html><body>')

        chichar_key = ndb.Key(urlsafe=chicharid)
        chichar     = chichar_key.get()

        self.response.write(CHICHAR_STROKE_TEMPLATE % ( chichar.chichar, chicharid, chicharid, chichar.nstrokes, chichar.strokes, chicharid ) )
        self.response.write('</body></html>')
# [END StrokeChiChar]

# [START SaveStrokeChiChar]
class SaveStrokeChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        chichar_key = ndb.Key(urlsafe=chicharid)
        chichar     = chichar_key.get()

        nstrokes = self.request.get("charnstrokes");
        strokes  = self.request.get("charstrokes");

        puts("nstrokes",nstrokes,"strokes",strokes)
        
        chichar.nstrokes = nstrokes;
        chichar.strokes  = strokes;
        chichar.put()

        self.redirect("/strokechichar/" + chicharid)
# [END SaveStrokeChiChar]

# [START ClearStrokeChiChar]
class ClearStrokeChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        chichar_key = ndb.Key(urlsafe=chicharid)
        chichar     = chichar_key.get()

        chichar.nstrokes = "0";
        chichar.strokes  = "";
        chichar.put()

        self.redirect("/strokechichar/" + chicharid)
# [END SaveStrokeChiChar]


# [START ExportChiChar]
class ExportChiChars(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        for chichar in getallchichars(self):
            # self.response.write("<div>" + "@".join([chichar.chichar,chichar.translation,chichar.pronunciation.chichar.nstrokes,chichar.strokes]) + "</div>")
            spronunciation = iff(chichar.pronunciation == None,"None",chichar.pronunciation)
            stranslation = iff(chichar.translation == None,"None",chichar.translation)
            snstrokes = iff(chichar.nstrokes == None,"None",str(chichar.nstrokes))
            sstrokes  = iff(chichar.strokes == None,"None",chichar.strokes)
            self.response.write("<div>" + "@".join([chichar.chichar,stranslation,spronunciation,snstrokes,sstrokes]) + "</div>")
        self.response.write('</body></html>')
# [END ExportChiChar]



