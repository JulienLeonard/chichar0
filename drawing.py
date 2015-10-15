from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from mydicts     import *
from myschemas   import *
from myadmin     import *

from utils import *

DRAWING_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>SandboxDraw</h1>
    <div id="chicharcanvas">
    </div>
    <textarea id="charnstrokes" style="display:none;"></textarea>
    <textarea id="charstrokes" style="display:none;"></textarea>
     </div>
    <script type="text/javascript" src="javascript/others/webgl-utils.js"></script>
    <script type="text/javascript" src="javascript/others/sylvester.js"></script>
    <script type="text/javascript" src="javascript/jsvg/myquadtree.js"></script>
    <script type="text/javascript" src="javascript/jsvg/utils.js"></script>
    <script type="text/javascript" src="javascript/jsvg/color.js"></script>
    <script type="text/javascript" src="javascript/jsvg/geoutils.js"></script>
    <script type="text/javascript" src="javascript/jsvg/bside.js"></script>
    <script type="text/javascript" src="javascript/jsvg/mywebgl.js"></script>
    <script type="text/javascript" src="javascript/jsvg/bpatternbao.js"></script>
    <script type="text/javascript" src="javascript/drawing/chicharcanvas.js"></script>
"""


# [START ListSentences]
class SandboxDraw(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        self.response.write(DRAWING_TEMPLATE)

        self.response.write('</body></html>')
# [END ListSentences]

