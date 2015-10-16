CHAR2PINYIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <form action="/checkchar2pinyintest" method="post">
      <div><textarea name="chartestchichar" rows="1" cols="2" disabled>%s</textarea></div>
      <!-- <div><textarea name="chartestpinyin"  rows="1" cols="6"></textarea></div> -->
           <input name="chartestpinyin" type="text" autocomplete="off" autofocus/>
      <div><input type="submit" value="Check"/></div>
    </form>
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>    
    </div>
"""

CHAR2PINYIN_CHECK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    %s
    <hr>
    <form action="/char2pinyintest" method="get">
      <div><input type="submit" value="Next" autofocus></div>
    </form>
    </div>
"""


DEF2CHAR_TEMPLATE = """\
  <head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
  </head>
  <div align="center">
  <form action="/checkdef2chartest" method="post">
      <div><textarea name="chartesttranslation"    rows="1" cols="10" disabled>%s</textarea></div>
      <div><textarea name="chartestpronunciation"  rows="1" cols="6" disabled>%s</textarea></div>
      <!-- <div><textarea name="chartestchichar"        rows="1" cols="2"></textarea></div> -->
      <!-- <input name="chartestchichar" type="text" autocomplete="off" autofocus/> -->
    </form>
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
<!--
    <td>
    <form action="/cleardef2chartest/" method="post">
       <div><input type="submit" value="Clear"></div>
   </form>
   </td>
-->
   <td>
    <form action="/checkdef2chartest" method="post">
       <textarea name="charnstrokes" style="display:none;"></textarea>
       <textarea name="charstrokes"  style="display:none;"></textarea>
      <div><input type="submit" value="Check"></div>
   </form>
   </td>
   </tr>
   </table>
    </div>
"""

DEF2CHAR_CHECK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    %s
    <hr>
    <table>
    <tr>
    <td>
    <div id="chicharcanvasdef"></div>
    <textarea name="chicharstrokedef" style="display:none;">%s</textarea>
    </td>
    <td>
    <div>%s</div>
    </td>
    <td>
    <div id="chicharcanvasanswer"></div>  
    <textarea name="chicharstrokeanswer" style="display:none;">%s</textarea>
    </td>
    </tr>
    </table>
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
    <script type="text/javascript" src="/javascript/drawing/chichartest.js"></script>
<table>
<tr>
<td>
    <form action="/answerdef2chartest/KO" method="get">
      <div><input type="submit" value="KO" autofocus></div>
    </form>
</td>
<td>
    <form action="/answerdef2chartest/OK" method="get">
      <div><input type="submit" value="OK"></div>
    </form>
</td>
</tr>
</table>
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>    
    </div>
"""

DEF2CHAR_ANSWER_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    %s
    <hr>
    <form action="/def2chartest" method="get">
      <div><input type="submit" value="Next" autofocus></div>
    </form>
    </div>
"""
