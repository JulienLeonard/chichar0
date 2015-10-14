from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from booktemplates import *

from utils       import *
from modelutils  import *


# [START ListBooks]
class ListBooks(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        sdict_name      = self.request.get('dict_name',USERDICT)

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
                        book = Book(parent=dict_key(udict_name));
                        book.name        = parts[0].strip()
                        book.description = parts[1].strip()
                        book.put()
                    else:
                        if not chapter == None:
                            chapter.units = unitlist
                            chapter.book  = book
                            chapter.put()
                            unitlist = []
                        chapter = Chapter(parent=dict_key(udict_name));
                        chapter.name        = parts[0].strip();
                        chapter.description = parts[1].strip();

                if len(parts) == 3:
                    chichar       = parts[0].strip()
                    translation   = parts[1].strip()
                    pronunciation = parts[2].strip()
            
                    newdata = allocatedata(self,chichar,translation,pronunciation)

                    if newdata:
                        unit = Unit(parent=dict_key(udict_name));
                        unit.unittype = datatype(newdata)
                        unit.unitkey  = newdata.key.urlsafe()
                        unit.put()
                        unitlist.append(unit)
                    else:
                        self.response.write("Cannot allocate " + dataline )
        
        chapter.units = unitlist
        chapter.book  = book
        chapter.put()
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

        chaptercontent  = "<table>"
        chapters_query = Chapter.query().order(Chapter.date)
        chapters       = chapters_query.fetch()
        for chapter in chapters:
            if chapter.book.name == book.name:
                chaptercontent  = chaptercontent + "<tr>" + "<td>" + chapter.name + "</td><td>" + chapter.description + "</td>" + "</tr>\n"
        chaptercontent  = chaptercontent + "</table>"

        charcontent     = "TODO"
        wordcontent     = "TODO"
        sentencecontent = "TODO"

        self.response.write(VIEW_BOOK_TEMPLATE % ( book.name, book.description, chaptercontent, charcontent, wordcontent, sentencecontent ))


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
