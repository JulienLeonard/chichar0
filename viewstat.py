from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *

# [START removestats]
def removestats(request,chichar):
        views_query = ViewStat.query(chichar == chichar)
        views = views_query.fetch()
        for view in views:
            view.key.delete()
# [END removestats]

# [START ListViewStat]
class ListViewStats(webapp2.RequestHandler):
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
# [END ListViewStat]


def clearviewstats(request):
    viewstats_query = ViewStat.query()
    viewstats = viewstats_query.fetch()        
    for viewstat in viewstats:
        viewstat.key.delete()
    

# [START ClearViewStats]
class ClearViewStats(webapp2.RequestHandler):
    def post(self):
        clearviewstats()
        self.redirect('/')
# [END ClearViewStats]
