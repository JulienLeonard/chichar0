MAIN_PAGE_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">

    <h1>General</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/mainsearch" method="post">
      <div><input type="submit" value="Search"></div>
    </form>
    </td>
    <td>
    <form action="/mainload" method="get">
      <div><input type="submit" value="Load"></div>
    </form>
    </td>
    <td>
    <form action="/mainclear" method="post">
      <div><input type="submit" value="Clear"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>

    <h1>Chars</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/addchichar" method="get">
      <div><input type="submit" value="Add"></div>
    </form>
    </td>
    <td>
    <form action="/loadchicharfile" method="get">
      <div><input type="submit" value="Load"></div>
    </form>
    </td>
    <td>
    <form action="/clearchichars" method="post">
      <div><input type="submit" value="Clear"></div>
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

    <h1>Words</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/listwords" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/addword" method="get">
      <div><input type="submit" value="Add"></div>
    </form>
    </td>
    <td>
    <form action="/loadwordfile" method="get">
      <div><input type="submit" value="Load"></div>
    </form>
    </td>
    <td>
    <form action="/clearwords" method="post">
      <div><input type="submit" value="Clear"></div>
    </form>
    </td>
    <td>
    <form action="/statwords" method="get">
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
    <form action="/addsentence" method="get">
      <div><input type="submit" value="Add"></div>
    </form>
    </td>
    <td>
    <form action="/loadsentencefile" method="get">
      <div><input type="submit" value="Load"></div>
    </form>
    </td>
    <td>
    <form action="/clearsentences" method="post">
      <div><input type="submit" value="Clear"></div>
    </form>
    </td>
    <td>
    <form action="/statsentences" method="get">
      <div><input type="submit" value="Stats"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>

    <h1>Training</h1> 
    <div align="center">
    <table>
    <tr>
    <td>
    <form action="/char2pinyintest" method="get">
      <div><input type="submit" value="Char2Pinyin"></div>
    </form>
    </td>
    <td>
    <form action="/def2chartest" method="get">
      <div><input type="submit" value="Def2Char"></div>
    </form>
    </td>
    <td>
    <form action="/charteststats" method="get">
      <div><input type="submit" value="CharTestStats"></div>
    </form>
    </td>
    </tr>
    </table>
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

LOAD_GENERAL = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/domainload" method="post">
      <div><textarea name="dataentry" rows="10" cols="40"></textarea></div>
      <div><input type="submit" value="Load"></div>
   </form>
"""

SEARCH_GENERAL = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>Search</h1>
    <hr>
    <form action="/mainsearch" method="post">
      <div><textarea name="searchquery" rows="1" cols="10">%s</textarea></div>
      <div><input type="submit" value="Search"></div>
   </form>
   <hr>
   <h1>Chars</h1>
   %s
   <h1>Words</h1>
   %s
   <h1>Sentences</h1>
   %s
   <hr>
    <form action="/" method="post">
      <div><input type="submit" value="Home"></div>
   </form>
"""
