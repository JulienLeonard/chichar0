MAIN_PAGE_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Chars</h1> 
    <div>
    <form action="/addchichar" method="get">
      <div><input type="submit" value="Add char"></div>
    </form>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List chars"></div>
    </form>
    <form action="/clearchichars" method="post">
      <div><input type="submit" value="Clear all chars"></div>
    </form>
    </div>
    <h1>Sentences</h1> 
    <div>
    <form action="/listsentences" method="get">
      <div><input type="submit" value="Sentences"></div>
    </form>
    <form action="/loadsentencefile" method="get">
      <div><input type="submit" value="Load sentence file"></div>
    </form>
    <form action="/clearsentences" method="post">
      <div><input type="submit" value="Clear all sentences"></div>
    </form>
    </div>
    <h1>Training</h1> 
    <div>
    TODO
    </div>
    <h1>Stats</h1>
    <form action="/listviewstats" method="get">
      <div><input type="submit" value="Viewstats"></div>
    </form>
    <a href="%s">%s</a>
"""

MAIN_PAGE_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Chars</h1>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List chars"></div>
    </form>
    <h1>Sentences</h1>
    <form action="/listsentences" method="get">
      <div><input type="submit" value="Sentences"></div>
    </form>
    <h1>Training</h1>
    <div>TODO</div>
    <h1>Stats</h1>
    <form action="/listviewstats" method="get">
      <div><input type="submit" value="Viewstats"></div>
    </form>
    <a href="%s">%s</a>
"""


ADD_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/doaddchichar" method="post">
      <div><textarea name="chichar"        rows="1" cols="40"></textarea></div>
      <div><textarea name="translation"    rows="1" cols="40"></textarea></div>
      <div><textarea name="pronunciation"  rows="1" cols="40"></textarea></div>
      <div><input type="submit" value="Add char"></div>
    </form>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    %s
"""

LIST_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <hr>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""

LIST_SENTENCE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <hr>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""

LOAD_SENTENCES = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/loadsentences" method="post">
      <div><textarea name="sentences" rows="10" cols="40"></textarea></div>
      <div><input type="submit" value="Load sentences"></div>
   </form>
"""


VIEW_CHI_CHAR_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div>%s</div>
    <div>%s</div>
    <div>%s</div>
    <form action="/editchichar/%s" method="get">
       <div><input type="submit" value="Edit char"></div>
    </form>
    <form action="/deletechichar/%s" method="post">
      <div><input type="submit" value="Delete char"></div>
    </form>
    <form action="/addchichar" method="get">
      <div><input type="submit" value="Add char"></div>
    </form>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""

VIEW_CHI_CHAR_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div>%s</div>
    <div>%s</div>
    <div>%s</div>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""



EDIT_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/savechichar/%s" method="post">
       <div><textarea name="chichar"        rows="1" cols="40">%s</textarea></div>
       <div><textarea name="translation"    rows="1" cols="40">%s</textarea></div>
       <div><textarea name="pronunciation"  rows="1" cols="40">%s</textarea></div>
       <div><input type="submit" value="Save"></div>
    </form>
    <form action="/viewchichar/%s" method="get">
      <div><input type="submit" value="Cancel"></div>
    </form>
"""
