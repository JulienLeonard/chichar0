import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mytemplates import *
from mydicts     import *
from myadmin     import *
from myschemas   import *

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

def chicharlist(request,detailed=False):
    # [START query]
    dict_name      = request.request.get('dict_name',CHICHARDICT)
    chichars_query = Chichar.query(ancestor=dict_key(dict_name)).order(-Chichar.date)
    chichars       = chichars_query.fetch()
    # [END query]

    charlist = ""
    if detailed:
        charlist = charlist + "<table>"
    for chichar in chichars:
        if not detailed:
            charlist = charlist + " " + chichar.chichar
        else:            
            charlist = charlist + "\n<tr>" + "<td><form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form></td>"  +" <td> " + chichar.translation + "</td><td> " + chichar.pronunciation + "</td></tr>"
    if detailed:
        charlist = charlist + "</table>"

    return charlist
    

# [START main_page]
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

# [END main_page]

# [START main_page]
class ListChiChar(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        charlist = chicharlist(self,True)

        # Write the submission form and the footer of the page
        self.response.write(LIST_CHI_CHAR_TEMPLATE % charlist)

        self.response.write('</body></html>')
# [END main_page]

# [START main_page]
class ListViewStat(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write('<h1>Views list</h1>')

        udict_name      = self.request.get('dict_name',USERDICT)
        
        cuser = users.get_current_user()

        if cuser:
            views_query = ViewStat.query(ViewStat.email == cuser.email()).order(-ViewStat.date)
            views       = views_query.fetch()
            for view in views:
                self.response.write("new view")
                if view.chichar:
                    self.response.write("chichar " + view.chichar.chichar)
                if view.sentence:   
                    self.response.write("sentence " + view.sentence.chichar)
        else:
            self.response.write("You need to login to see your stats")
        self.response.write('</body></html>')

# [END main_page]




# [START main_page]
class ListSentences(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        sdict_name      = self.request.get('dict_name',SENTENCEDICT)
        cdict_name      = self.request.get('dict_name',CHICHARDICT)

        sentences_query = Sentence.query(ancestor=dict_key(sdict_name)).order(-Sentence.date)
        sentences       = sentences_query.fetch()
        # [END query]

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

        # Write the submission form and the footer of the page
        self.response.write(LIST_SENTENCE_TEMPLATE % sentencelist)

        self.response.write('</body></html>')

# [END main_page]


# [START main_page]
class LoadSentenceFile(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(LOAD_SENTENCES)

        self.response.write('</body></html>')

# [END main_page]

def lsubstract(list1,list2):
    result = []
    for item1 in list1:
        if not item1 in list2:
            result.append(item1)
    return result


# [START main_page]
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
                    osentence = Sentence(parent=dict_key(sdict_name));
                    osentence.chichar        = parts[0].strip()
                    osentence.translation    = parts[1].strip()
                    osentence.pronunciation  = parts[2].strip()

                    chichars  = lsubstract(list(parts[0].strip()),     [""," ","\n","\t",",","."])
                    pinyins   = lsubstract(parts[2].strip().split(" "),[""," ","\n","\t",",","."])
                    if not (len(chichars) == len(pinyins)):
                        self.response.write("<div>  error matching char " + "@".join(chichars) + " pynyin " + "@".join(pinyins) + "</div>\n")

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

# [END main_page]



# [START guestbook]
class DoAddChiChar(webapp2.RequestHandler):
    def post(self):
        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar = Chichar(parent=dict_key(dict_name));
        chichar.chichar        = self.request.get('chichar')
        chichar.translation    = self.request.get('translation')
        chichar.pronunciation  = self.request.get('pronunciation')
        chichar.put()

        self.redirect("/viewchichar/" + chichar.key.urlsafe())

# [END guestbook]

# [START guestbook]
class ClearChiChars(webapp2.RequestHandler):
    def post(self):
        chichar = Chichar()
        chichars_query = Chichar.query()
        chichars = chichars_query.fetch()
        
        for chichar in chichars:
            chichar.key.delete()

        self.redirect('/')
# [END guestbook]

# [START guestbook]
class ClearSentences(webapp2.RequestHandler):
    def post(self):
        sentence = Sentence()
        sentences_query = Sentence.query()
        sentences = sentences_query.fetch()
        
        for sentence in sentences:
            sentence.key.delete()

        self.redirect('/')
# [END guestbook]



# [START main_page]
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
            self.response.write(VIEW_CHI_CHAR_ADMIN_TEMPLATE % ( chichar.chichar, chichar.translation, chichar.pronunciation,chichar.key.urlsafe(),chichar.key.urlsafe()))
        else:
            self.response.write(VIEW_CHI_CHAR_USER_TEMPLATE % ( chichar.chichar, chichar.translation, chichar.pronunciation))
            

        self.response.write('</body></html>')
# [END main_page]

# [START main_page]
class EditChiChar(webapp2.RequestHandler):
    def get(self,chicharid):
        self.response.write('<html><body>')

        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()

        # Write the submission form and the footer of the page
        self.response.write(EDIT_CHI_CHAR_TEMPLATE % ( chichar.key.urlsafe(), chichar.chichar, chichar.translation, chichar.pronunciation,chichar.key.urlsafe()))

        self.response.write('</body></html>')

# [END main_page]

# [START main_page]
class SaveChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()
        chichar.chichar        = self.request.get('chichar')
        chichar.translation    = self.request.get('translation')
        chichar.pronunciation  = self.request.get('pronunciation')
        chichar.put()

        self.redirect("/viewchichar/" + chichar.key.urlsafe())
# [END main_page]


def removestats(request,chichar):
        views_query = ViewStat.query(chichar == chichar)
        views = views_query.fetch()
        for view in views:
            view.key.delete()
    

# [START main_page]
class DeleteChiChar(webapp2.RequestHandler):
    def post(self,chicharid):

        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()

        # removestats(self,chichar)

        chichar.key.delete()

        self.redirect("/listchichars")
# [END main_page]


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addchichar',          AddChiChar),
    ('/listchichars',        ListChiChar),
    ('/doaddchichar',        DoAddChiChar),
    ('/viewchichar/(.*)',    ViewChiChar),
    ('/editchichar/(.*)',    EditChiChar),
    ('/savechichar/(.*)',    SaveChiChar),
    ('/deletechichar/(.*)',  DeleteChiChar),
    ('/clearchichars',       ClearChiChars),
    ('/loadsentencefile',    LoadSentenceFile),
    ('/loadsentences',       LoadSentences),
    ('/listsentences',       ListSentences),
    ('/clearsentences',      ClearSentences),
    ('/listviewstats',       ListViewStat),
    
], debug=True)
