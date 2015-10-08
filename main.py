import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import webapp2

ADMIN_ID = "jblondinet@gmail.com"

MAIN_PAGE_ADMIN_TEMPLATE = """\
    <form action="/addchichar?" method="get">
      <div><input type="submit" value="Add char"></div>
    </form>
    <form action="/listchichar?" method="get">
      <div><input type="submit" value="List chars"></div>
    </form>
    <a href="%s">%s</a>
"""

MAIN_PAGE_USER_TEMPLATE = """\
    <form action="/listchichar?" method="get">
      <div><input type="submit" value="List chars"></div>
    </form>
    <a href="%s">%s</a>
"""


ADD_CHI_CHAR_TEMPLATE = """\
    <form action="/doaddchichar?" method="post">
      <div><textarea name="chichar"        rows="1" cols="60"></textarea></div>
      <div><textarea name="translation"    rows="1" cols="60"></textarea></div>
      <div><textarea name="pronunciation"  rows="1" cols="60"></textarea></div>
      <div><input type="submit" value="Add char"></div>
    </form>
    <hr>
    %s
"""

LIST_CHI_CHAR_TEMPLATE = """\
    <hr>
    %s
    <hr>
"""

VIEW_CHI_CHAR_TEMPLATE = """\
    <form action="/editchichar/%s" method="post">
       <div><textarea name="chichar"        rows="1" cols="60">%s</textarea></div>
       <div><textarea name="translation"    rows="1" cols="60">%s</textarea></div>
       <div><textarea name="pronunciation"  rows="1" cols="60">%s</textarea></div>
       <div><input type="submit" value="Edit char"></div>
    </form>
    <form action="/deletechichar/%s" method="post">
      <div><input type="submit" value="Delete char"></div>
    </form>
"""


CHICHARDICT = 'chichardict'

def dict_key(dict_name=CHICHARDICT):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Dict', dict_name)




# [START chichar]
class Chichar(ndb.Model):
    """A main model for representing a chichar."""
    chichar       = ndb.StringProperty(indexed=False)
    translation   = ndb.StringProperty(indexed=False)
    pronunciation = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END chichar]

# [START main_page]
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
    chichars    = chichars_query.fetch(10)
    # [END query]

    charlist = ""
    for chichar in chichars:
        if not detailed:
            charlist = charlist + " " + chichar.chichar
        else:
            query_params = {'chichar': chichar.chichar}
            charlist = charlist + "\n<br> <a href=\"./viewchichar/" + chichar.key.urlsafe()  + "\"> " + chichar.chichar +" </a> </br>"
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



# [START guestbook]
class DoAddChiChar(webapp2.RequestHandler):
    def post(self):
        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar = Chichar(parent=dict_key(dict_name));
        chichar.chichar        = self.request.get('chichar')
        chichar.translation    = self.request.get('translation')
        chichar.pronunciation  = self.request.get('pronunciation')
        chichar.put()

        self.redirect('/addchichar')
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

        # Write the submission form and the footer of the page
        self.response.write(VIEW_CHI_CHAR_TEMPLATE % (chichar.key.urlsafe(), chichar.chichar, chichar.translation, chichar.pronunciation,chichar.key.urlsafe()))

        self.response.write('</body></html>')
# [END main_page]

# [START main_page]
class EditChiChar(webapp2.RequestHandler):
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

# [START main_page]
class DeleteChiChar(webapp2.RequestHandler):
    def post(self,chicharid):
        dict_name = self.request.get('dict_name', CHICHARDICT)
        chichar_key = ndb.Key(urlsafe=chicharid)
        # chichar = Chichar(parent=dict_key(dict_name));
        chichar = chichar_key.get()
        chichar.key.delete()

        self.redirect("/listchichar")
# [END main_page]




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addchichar',          AddChiChar),
    ('/listchichar',         ListChiChar),
    ('/doaddchichar',        DoAddChiChar),
    ('/viewchichar/(.*)',    ViewChiChar),
    ('/editchichar/(.*)',    EditChiChar),
    ('/deletechichar/(.*)',  DeleteChiChar),
    
], debug=True)
