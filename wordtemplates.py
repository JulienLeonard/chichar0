ADD_WORD_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/doaddword" method="post">
      <div><textarea name="wordchichar"        rows="2" cols="40"></textarea></div>
      <div><textarea name="wordpronunciation"  rows="2" cols="40"></textarea></div>
      <div><textarea name="wordtranslation"    rows="2" cols="40"></textarea></div>
      <div><input type="submit" value="Add word"></div>
    </form>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""


LIST_WORD_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Words list</h1>
    <hr>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </div>
"""

LOAD_WORDS = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/loadwords" method="post">
      <div><textarea name="words" rows="10" cols="40"></textarea></div>
      <div><input type="submit" value="Load words"></div>
   </form>
"""

VIEW_WORD_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="wordchichar">%s</div>
    <div class="wordtranslation">%s</div>
    <div class="wordpronunciation">%s</div>
    <div class="space"></div>

    %s <!-- char list clickable -->

    <table>
    <tr>
    <td>
    <form action="/editword/%s" method="get">
       <div class="charaction"><input type="submit" value="Edit"></div>
    </form>
    </td>
    <td>
    <form action="/deleteword/%s" method="post">
      <div class="charaction"><input type="submit" value="Delete"></div>
    </form>
    </td>
    <td>
    <form action="/addword" method="get">
      <div class="charaction"><input type="submit" value="New"></div>
    </form>
    </td>
    <td>
    <form action="/listwords" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/" method="get">
      <div class="home"><input type="submit" value="Home"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
"""

VIEW_WORD_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="wordchichar">%s</div>
    <div class="wordtranslation">%s</div>
    <div class="wordpronunciation">%s</div>
    <div class="space"></div>

    %s <!-- char list clickable -->

    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listwords" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
  
    </tr>
    </table>
   </div>
"""

STAT_WORD_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Words Stats</h1>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listwords" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>  
    </tr>
    </table>
    <hr>
    <table> 
    <tr>
    <td>
    Words number
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
    <form action="/listwords" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>  
    </tr>
    </table>
    </div>
"""
