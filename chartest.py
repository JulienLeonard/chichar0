from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts           import *
from chartesttemplates import *
from myschemas         import *
from myadmin           import *

from viewstat          import *

from utils import *

def getnextcharquestion(request,user,testtype):
    dict_name      = request.request.get('dict_name',CHICHARDICT)
    chichars_query = Chichar.query(ancestor=dict_key(dict_name)).order(Chichar.date)
    chichars       = chichars_query.fetch(1)
    return chichars[0]


# [START Char2PinyinTest]
class Char2PinyinTest(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')


        user = users.get_current_user()
        if user == None:
            self.response.write("You must be loged in to train")
        else:
            testtype = "char2pinyin"
            chichar = getnextcharquestion(self,user,testtype)

            dict_name = self.request.get('dict_name', USERDICT)
            chartest = CharTest(parent=dict_key(dict_name));
            chartest.email      = user.email()
            chartest.testtype   = testtype
            chartest.chichar    = chichar
            chartest.put()

            self.response.write(CHAR2PINYIN_TEMPLATE % chichar.chichar)

        self.response.write('</body></html>')
# [END Char2PinyinTest]

# [START Char2PinyinTest]
class CheckChar2PinyinTest(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        dict_name      = self.request.get('dict_name',USERDICT)
        chartest_query = CharTest.query(ancestor=dict_key(dict_name)).order(-CharTest.date)
        chartest       = chartest_query.fetch(1)[0]

        answer        = self.request.get('chartestpinyin')
        if answer.strip() == chartest.chichar.pronunciation:
            result = "Correct ! " + chartest.chichar.chichar + " pinyin is " + chartest.chichar.pronunciation
            chartest.result = "OK"
            chartest.put()
        else:
            result = "Error ! " + chartest.chichar.chichar + " pinyin is " + chartest.chichar.pronunciation + " and not " + answer + ". Try again soon !"
            chartest.result = "KO"
            chartest.put()

        self.response.write( CHAR2PINYIN_CHECK_TEMPLATE % result)
        
        self.response.write('</body></html>')
# [END Char2PinyinTest]

# [START Char2PinyinTest]
class Def2CharTest(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        user = users.get_current_user()
        if user == None:
            self.response.write("You must be loged in to train")
        else:
            testtype = "def2char"
            chichar = getnextcharquestion(self,user,testtype)

            dict_name = self.request.get('dict_name', USERDICT)
            chartest = CharTest(parent=dict_key(dict_name));
            chartest.email      = user.email()
            chartest.testtype   = testtype
            chartest.chichar    = chichar
            chartest.put()

            self.response.write(DEF2CHAR_TEMPLATE % (chichar.translation, chichar.pronunciation))
        
        self.response.write('</body></html>')
# [END Char2PinyinTest]

# [START CheckDef2CharTest]
class CheckDef2CharTest(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        dict_name      = self.request.get('dict_name',USERDICT)
        chartest_query = CharTest.query(ancestor=dict_key(dict_name)).order(-CharTest.date)
        chartest       = chartest_query.fetch(1)[0]

        answer        = self.request.get('chartestchichar')
        if answer.strip() == chartest.chichar.chichar:
            result = "Correct ! " + chartest.chichar.translation + " char is " + chartest.chichar.chichar
            chartest.result = "OK"
            chartest.put()
        else:
            result = "Error ! " + chartest.chichar.translation + " char is " + chartest.chichar.chichar + " and not " + answer + ". Try again soon !"
            chartest.result = "KO"
            chartest.put()

        self.response.write( DEF2CHAR_CHECK_TEMPLATE % result)
        
        self.response.write('</body></html>')
# [END CheckDef2CharTest]

# [START CharTestStats]
class CharTestStats(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        # [START query]
        dict_name      = self.request.get('dict_name',CHICHARDICT)
        chichars_query = Chichar.query(ancestor=dict_key(dict_name)).order(Chichar.date)
        chichars       = chichars_query.fetch()
        # [END query]

        chartestresult = {}
        for chichar in chichars:
            chartestresult[chichar.chichar] = {}
            for testtype in ["char2pinyin","def2char"]:
                chartestresult[chichar.chichar][testtype] = {}
                chartestresult[chichar.chichar][testtype]["OK"] = 0
                chartestresult[chichar.chichar][testtype]["KO"] = 0
            chartestresult[chichar.chichar]["total"] = 0
                

        udict_name     = self.request.get('dict_name',USERDICT)
        chartest_query = CharTest.query(ancestor=dict_key(udict_name))
        for chartest in chartest_query.fetch():
            if chartest.chichar.chichar in chartestresult:
                if chartest.result == None:
                    chartest.result = "KO"
                    chartest.put()
                chartestresult[chartest.chichar.chichar][chartest.testtype][chartest.result] += 1
                chartestresult[chartest.chichar.chichar]["total"] += 1
                

        sortlist = [(chartestresult[chichar.chichar]["total"],chichar.chichar) for chichar in chichars]
        sortlist.sort()

        content = "<table>"
        for (total,chichar) in lreverse(sortlist):
            content = content + "\n<tr>"
            # content = content + "<td><form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form></td>"
            content = content + "<td>" + chichar + "</td><td>" + str(total) + "</td><td>" + str(chartestresult[chichar]["char2pinyin"]["OK"]) + "</td><td>" + str(chartestresult[chichar]["char2pinyin"]["KO"]) + "</td><td>" + str(chartestresult[chichar]["def2char"]["OK"]) + "</td><td>" + str(chartestresult[chichar]["def2char"]["KO"]) + "</td>"
            content = content + "</tr>"
        content = content + "</table>"

        self.response.write(content)

        self.response.write('</body></html>')
# [END CharTestStats]

def clearchartests(request):
    chartests_query = CharTest.query()
    chartests = chartests_query.fetch()        
    for chartest in chartests:
        chartest.key.delete()
