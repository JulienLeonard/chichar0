from utils import *

def tableclickchichars(chichars):
    result = "<table>"
    for chichar10 in lsplit(chichars,10):
        result += "<tr>"
        for chichar in chichar10:
            result += "<td>"
            result += "<form action=\"/viewchichar/" + chichar.key.urlsafe() + "\" method=\"get\"><div><input type=\"submit\" value=\"" + chichar.chichar + "\"></div></form>"
            result += "</td>"
        result += "</tr>"
    result += "<table>"
    return result
