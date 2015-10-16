LIST_BOOK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Books list</h1>
    <hr>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </div>
"""

VIEW_BOOK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div>
    <h1>Book</h1>
    <hr>
    <table>
    <tr>
    <td>Name</td>
    <td> %s</td>
    </tr>
    <tr>
    <td>Description</td>
    <td>%s</td>
    </tr>
    </table>
    <hr>
    <form action="/exportbook/%s" method="get">
      <div><input type="submit" value="Export"></div>
    </form> 
    <hr>
    <h2>Content</h2>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </div>
"""


LOAD_BOOK = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/loadbook" method="post">
      <div><textarea name="bookcontent" rows="10" cols="40"></textarea></div>
      <div><input type="submit" value="Load book"></div>
   </form>
"""

STAT_BOOK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Book Stats</h1>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listbooks" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>  
    </tr>
    </table>
    <hr>
    <table> 
    <tr>
    <td>
    Books number
    </td>
    <td>
    %s
    </td>
    </tr>
    </table>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listbooks" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>  
    </tr>
    </table>
    </div>
"""


