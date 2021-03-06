

ADD_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/doaddchichar" method="post">
      <div><textarea name="chichar"        rows="1" cols="40"></textarea></div>
      <div><textarea name="pronunciation"  rows="1" cols="40"></textarea></div>
      <div><textarea name="translation"    rows="1" cols="40"></textarea></div>
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
    <div align="center">
    <h1>Char list</h1>
    <hr>
    %s
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </div>
"""


VIEW_CHI_CHAR_ADMIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="chichar">%s</div>
    <div class="pronunciation">%s</div>
    <div class="translation">%s</div>
    <div class="space"></div>
    <table>
    <tr>
    <td>
    <form action="/editchichar/%s" method="get">
       <div class="charaction"><input type="submit" value="Edit"></div>
    </form>
    </td>
    <td>
    <form action="/strokechichar/%s" method="get">
       <div class="charaction"><input type="submit" value="Stroke"></div>
    </form>
    </td>
    <td>
    <form action="/deletechichar/%s" method="post">
      <div class="charaction"><input type="submit" value="Delete"></div>
    </form>
    </td>
    <td>
    <form action="/addchichar" method="get">
      <div class="charaction"><input type="submit" value="New"></div>
    </form>
    </td>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/chicharsentences/%s" method="get">
      <div><input type="submit" value="Sentences"></div>
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

VIEW_CHI_CHAR_USER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="chichar">%s</div>
    <div class="pronunciation">%s</div>
    <div class="translation">%s</div>
    <div class="space"></div>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="Char List"></div>
    </form>
    </td>
    <td>
    <form action="/chicharsentences/%s" method="get">
      <div><input type="submit" value="Sentences"></div>
    </form>
    </td>
    </tr>
    </table>
   </div>
"""



EDIT_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <form action="/savechichar/%s" method="post">
       <div><textarea class="chichar" name="chichar"        rows="1" cols="2">%s</textarea></div>
       <div><textarea name="pronunciation"    rows="1" cols="10">%s</textarea></div>
       <div><textarea name="translation"  rows="1" cols="10">%s</textarea></div>
       <div class="space"></div>
       <div id="buttons">
           <table>
           <tr>
           <td>
           <div><input type="submit" name="save" value="Save"></div>
           </td>
           <td>
           <div><input type="submit" name="cancel" value="Cancel"></div>
           </td>
           </tr>
           </table>
           <div style="clear:both"></div>
       </div>
    </form>
    </div>
"""

STAT_CHI_CHAR_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Char stats</h1>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>  
    </tr>
    </table>
    <hr>
    <table> 
    <tr>
    <td>
    Chars number
    </td>
    <td>
    %s
    </td>
    </tr>
    </table>
    <hr>
    %s
    <hr>
    </div>
"""

CHI_CHAR_SENTENCES_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <h1>%s sentences</h1>
    <hr>
    %s
    <hr>
    <table>
    <tr>
    <td>
    <form action="/viewchichar/%s" method="get">
      <div><input type="submit" value="Back"></div>
    </form>
    </td>
    </tr>
   </table>
"""

LOAD_CHICHARS = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/loadchichars" method="post">
      <div><textarea name="chichars" rows="10" cols="40"></textarea></div>
      <div><input type="submit" value="Load chichars"></div>
   </form>
"""

CHICHAR_STROKE_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>%s Strokes</h1>
    <hr>
    <div id="chicharcanvas"></div>
    <script type="text/javascript" src="/javascript/others/webgl-utils.js"></script>
    <script type="text/javascript" src="/javascript/others/sylvester.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/myquadtree.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/utils.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/color.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/geoutils.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/bside.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/mywebgl.js"></script>
    <script type="text/javascript" src="/javascript/jsvg/bpatternbao.js"></script>
    <script type="text/javascript" src="/javascript/drawing/chicharutils.js"></script>
    <script type="text/javascript" src="/javascript/drawing/chicharcanvas.js"></script>
    <script type="text/javascript" src="/javascript/drawing/chicharstroke.js"></script>
    <hr>
    <table>
    <tr>
    <td>
    <form action="/clearstrokechichar/%s" method="post">
       <div><input type="submit" value="Clear"></div>
   </form>
   </td>
   <td>
    <form action="/savestrokechichar/%s" method="post">
       <textarea name="charnstrokes" style="display:none;">%s</textarea>
       <textarea name="charstrokes" style="display:none;">%s</textarea>
      <div><input type="submit" value="Save"></div>
   </form>
   </td>
   <td>
    <form action="/viewchichar/%s" method="get">
       <div><input type="submit" value="View"></div>
   </form>
   </td>
   </tr>
   </table>
   </div>
"""
