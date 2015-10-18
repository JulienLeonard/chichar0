from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from booktemplates import *

from utils       import *
from modelutils  import *


def addbook(request,bookname,bookdescription):
    udict_name      = request.request.get('dict_name',USERDICT)
    book = Book(parent=dict_key(udict_name));
    book.name        = bookname
    book.description = bookdescription
    book.put()
    return book
        
def addchapter(request,bookname,chaptername,chapterdescr):
    udict_name      = request.request.get('dict_name',USERDICT)
    chapter = Chapter(parent=dict_key(udict_name));
    chapter.name        = chaptername;
    chapter.description = chapterdescr;
    chapter.book        = bookname;
    chapter.put()
    return chapter

def addunit(request,chaptername,newdata):
    udict_name      = request.request.get('dict_name',USERDICT)
    unit = Unit(parent=dict_key(udict_name));
    unit.unittype = datatype(newdata)
    unit.unitkey  = newdata.key.urlsafe()
    unit.chichar  = newdata.chichar
    unit.chapter  = chaptername
    unit.put()
    return unit

def checkcreateuserbook(request):
    user = users.get_current_user()
    if not user == None:
         userbookname =  user.email() + "'s Book"
         if getbook(request,userbookname) == None:
             addbook(request,userbookname,"Your personal book")



# [START ListBooks]
class ListBooks(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        sdict_name      = self.request.get('dict_name',USERDICT)

        checkcreateuserbook(self)

        books_query = Book.query(ancestor=dict_key(sdict_name)).order(-Book.date)
        books       = books_query.fetch()

        booklist = ""
        booklist = booklist + "<table>"
        for book in books:
            booklist = booklist + "\n<tr><td>" + book.name  +" </td><td> " + book.description + "</td>"
            viewbookform = "<form action=\"/viewbook/" + book.key.urlsafe() + "\" method=\"get\"><div class=\"charaction\"><input type=\"submit\" value=\"+\"></div></form>"
            booklist = booklist + "<td>" + viewbookform + "</td>"
            booklist = booklist + "</tr>"
        booklist = booklist + "</table>"

        self.response.write(LIST_BOOK_TEMPLATE % booklist)

        self.response.write('</body></html>')
# [END ListBooks]


# [START LoadBook]
class LoadBookPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(LOAD_BOOK)

        self.response.write('</body></html>')
# [END LoadBook]

# [START LoadBooks]
class LoadBook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>')

        udict_name = self.request.get('dict_name', USERDICT)

        book        = None
        chapterlist = []
        unitlist    = []
        chapter     = None

        for dataline in self.request.get('bookcontent').split("\n"):
            if len(dataline) > 0:
                parts = dataline.split(";")

                puts("parts",parts)

                if len(parts) == 2:
                    if book == None:
                        bookname  = parts[0].strip()
                        bookdescr = parts[1].strip()
                        obook = getbook(self,bookname)
                        if obook == None:
                            book = addbook(self,bookname,bookdescr)
                        else:
                            self.response.write("<div>Book " + obook.name + " already known</div>" )
                            book = obook
                    else:
                        chaptername  = parts[0].strip()
                        chapterdescr = parts[1].strip()

                        ochapter = getchapter(self,book.name,chaptername)
                        if ochapter == None:
                            chapter = addchapter(self,bookname,chaptername,chapterdescr)
                        else:
                            self.response.write("<div>   Chapter " + ochapter.name + " already known</div>" )
                            chapter = ochapter


                if len(parts) == 3:
                    chichar       = parts[0].strip()
                    translation   = parts[1].strip()
                    pronunciation = parts[2].strip()
            
                    ounit  = getunit(self,chapter.name,chichar)

                    if ounit == None:
                        newdata = allocatedata(self,chichar,translation,pronunciation)

                        if newdata:
                            unit = addunit(self,chaptername,newdata)
                        else:
                            self.response.write("<div>Cannot allocate " + dataline + "</div>")
                    else:
                        self.response.write("<div>Unit " + ounit.chichar + " already known</div>" )
                        unit = ounit
                        
        removeduplicatechichars(self)

        self.response.write('</body></html>')

# [END LoadBooks]

def clearbooks(request):
    books_query = Book.query()
    books       = books_query.fetch()
        
    for book in books:
        deletebook(request,book.key.urlsafe())

    chapters_query = Chapter.query()
    chapters       = chapters_query.fetch()
        
    for chapter in chapters:
        deletechapter(request,chapter.key.urlsafe())

    units_query = Unit.query()
    units       = units_query.fetch()
        
    for unit in units:
        deleteunit(request,unit.key.urlsafe())

    checkcreateuserbook(request)
        

# [START ClearBooks]
class ClearBooks(webapp2.RequestHandler):
    def post(self):
        clearbooks(self)
        self.redirect('/')
# [END ClearBooks]

# [START ViewBook]
class ViewBook(webapp2.RequestHandler):
    def get(self,bookid):
        self.response.write('<html><body>')

        #dict_name = self.request.get('dict_name', USERDICT)
        #book = Book(parent=dict_key(dict_name));


        dict_name  = self.request.get('dict_name',USERDICT)
        book_key   = ndb.Key(urlsafe=bookid)
        book = book_key.get()

        content  = "<table>"
        chapters_query = Chapter.query(Chapter.book == book.name).order(Chapter.date)
        for chapter in chapters_query.fetch():
            content  = content + "<tr>" + "<td>" + chapter.name + "</td><td>" + "</td>" + "</tr>\n"
            
            for unit in Unit.query(Unit.chapter == chapter.name).order(Chapter.date):
                content  = content + "<tr>" + "<td></td><td>" + unit.chichar + "</td></tr>\n"

        content  = content + "</table>"

        self.response.write(VIEW_BOOK_TEMPLATE % ( book.name, book.description, book.key.urlsafe(), content ))

        self.response.write('</body></html>')
# [END ViewBook]

    
def deletebook(request,bookid):
    dict_name   = request.request.get('dict_name', USERDICT)
    book_key = ndb.Key(urlsafe=bookid)
    book     = book_key.get()
    book.key.delete()

def deletechapter(request,chapterid):
    dict_name   = request.request.get('dict_name', USERDICT)
    chapter_key = ndb.Key(urlsafe=chapterid)
    chapter     = chapter_key.get()
    chapter.key.delete()

def deleteunit(request,unitid):
    dict_name   = request.request.get('dict_name', USERDICT)
    unit_key = ndb.Key(urlsafe=unitid)
    unit     = unit_key.get()
    unit.key.delete()


# [START DeleteBook]
class DeleteBook(webapp2.RequestHandler):
    def post(self,bookid):
        deletebook(self,bookid)
        self.redirect("/listbooks")
# [END DeleteBook]

# [START LearnBook]
class LearnBook(webapp2.RequestHandler):
    def post(self,bookid):
        #deletebook(self,bookid)
        #self.redirect("/listbooks")
        self.response.write('<html><body>')
        
        self.response.write('</body></html>')
# [END LearnBook]


# [START StatBooks]
class StatBooks(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        
        dict_name   = self.request.get('dict_name',USERDICT)
        books_query = Book.query(ancestor=dict_key(dict_name)).order(-Book.date)
        books       = books_query.fetch()

        # Write the submission form and the footer of the page
        self.response.write(STAT_BOOK_TEMPLATE % ( len(books) ))

        self.response.write('</body></html>')
# [END StatChiChars]

# [START ExportBook]
class ExportBook(webapp2.RequestHandler):
    def get(self,bookid):
        self.response.write('<html><body>')

        dict_name  = self.request.get('dict_name',USERDICT)
        book_key   = ndb.Key(urlsafe=bookid)
        book = book_key.get()

        self.response.write("<div>" + ";".join([book.name,book.description]) + "</div>")
        chapters_query = Chapter.query(Chapter.book == book.name).order(Chapter.date)
        for chapter in chapters_query.fetch():
            self.response.write("<div>" + ";".join([chapter.name,chapter.description]) + "</div>")

            for unit in Unit.query(Unit.chapter == chapter.name).order(Chapter.date):
                data = getunitdata(self,unit)
                self.response.write("<div>" + ";".join([data.chichar,data.translation,data.pronunciation]) + "</div>")

        self.response.write('</body></html>')
# [END ExportBook]
