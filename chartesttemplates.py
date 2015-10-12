CHAR2PINYIN_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <form action="/checkchar2pinyintest" method="post">
      <div><textarea name="chartestchichar" rows="1" cols="2" disabled>%s</textarea></div>
      <div><textarea name="chartestpinyin"  rows="1" cols="6"></textarea></div>
      <div><input type="submit" value="Check"></div>
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
      <div><input type="submit" value="Next"></div>
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
      <div><textarea name="chartestchichar"        rows="1" cols="2"></textarea></div>
      <div><input type="submit" value="Check"></div>
    </form>
    </div>
"""

DEF2CHAR_CHECK_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    %s
    <hr>
    <form action="/def2chartest" method="get">
      <div><input type="submit" value="Next"></div>
    </form>
    </div>
"""
