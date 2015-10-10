import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from myadmin     import *

from utils       import *
from chichar     import *
from sentence    import *
from viewstat    import *

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

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addchichar',           AddChiChar),
    ('/listchichars',         ListChiChar),
    ('/doaddchichar',         DoAddChiChar),
    ('/viewchichar/(.*)',     ViewChiChar),
    ('/editchichar/(.*)',     EditChiChar),
    ('/savechichar/(.*)',     SaveChiChar),
    ('/deletechichar/(.*)',   DeleteChiChar),
    ('/clearchichars',        ClearChiChars),
    ('/loadsentencefile',     LoadSentenceFile),
    ('/loadsentences',        LoadSentences),
    ('/listsentences',        ListSentences),
    ('/viewsentence/(.*)',    ViewSentence),
    ('/editsentence/(.*)',    EditSentence),
    ('/deletesentence/(.*)',  DeleteSentence),
    ('/clearsentences',       ClearSentences),
    ('/listviewstats',        ListViewStats),
    ('/clearviewstats',       ClearViewStats),
    ('/statchichars',         StatChiChars),
    ('/chicharsentences/(.*)',ChiCharSentences),
    
], debug=True)
