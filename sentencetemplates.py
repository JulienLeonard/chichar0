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

VIEW_SENTENCE_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="sentencechichar">%s</div>
    <div class="sentencetranslation">%s</div>
    <div class="sentencepronunciation">%s</div>
    <div class="space"></div>

    %s <!-- char list clickable -->

    <table>
    <tr>
    <td>
    <form action="/editsentence/%s" method="get">
       <div class="charaction"><input type="submit" value="Edit"></div>
    </form>
    </td>
    <td>
    <form action="/deletesentence/%s" method="post">
      <div class="charaction"><input type="submit" value="Delete"></div>
    </form>
    </td>
    <td>
    <form action="/addsentence" method="get">
      <div class="charaction"><input type="submit" value="New"></div>
    </form>
    </td>
    <td>
    <form action="/listsentences" method="get">
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

VIEW_SENTENCE_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="sentencechichar">%s</div>
    <div class="sentencetranslation">%s</div>
    <div class="sentencepronunciation">%s</div>
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
    <form action="/listsentences" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
  
    </tr>
    </table>
   </div>
"""
