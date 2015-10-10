MAIN_PAGE_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Chars</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/addchichar" method="get">
      <div><input type="submit" value="Add"></div>
    </form>
    </td>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/clearchichars" method="post">
      <div><input type="submit" value="Clear all"></div>
    </form>
    </td>
    <td>
    <form action="/statchichars" method="get">
      <div><input type="submit" value="Stats"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
    <h1>Sentences</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/listsentences" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/loadsentencefile" method="get">
      <div><input type="submit" value="Load"></div>
    </form>
    </td>
    <td>
    <form action="/clearsentences" method="post">
      <div><input type="submit" value="Clear all"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
    <h1>Training</h1> 
    <div align="center">
    TODO
    </div>
    <h1>My Stats</h1>
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/listviewstats" method="get">
      <div><input type="submit" value="View"></div>
    </form>
    </td>
    <td>
    <form action="/clearviewstats" method="post">
      <div><input type="submit" value="Clear"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
    </div>
    <hr>
    <a href="%s">%s</a>
"""

MAIN_PAGE_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Chars</h1>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    <h1>Sentences</h1>
    <form action="/listsentences" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    <h1>Training</h1>
    <div>TODO</div>
    <h1>My Stats</h1>
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/listviewstats" method="get">
      <div><input type="submit" value="View"></div>
    </form>
    </td>
    <td>
    <form action="/clearviewstats" method="post">
      <div><input type="submit" value="Clear"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
    </div>
    <hr>
    <a href="%s">%s</a>
"""
