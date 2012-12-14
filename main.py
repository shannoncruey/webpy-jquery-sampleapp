#!/usr/bin/env python

import web
import os
import json
from datetime import datetime

# to avoid any path issues, "cd" to the web root.
web_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(web_root)
        
urls = (
    '/', 'index',
    '/ajaxdropdowns', 'ajaxdropdowns',
    '/getanythingyouwant', 'getanythingyouwant',
    '/getregionsashtml', 'getregionsashtml',
    '/getregionsasjson', 'getregionsasjson'
)
app = web.application(urls, globals())
render = web.template.render('templates', base='base')

class index:        
    def GET(self):
        return render.index()

class ajaxdropdowns:        
    def GET(self):
        return render.ajaxdropdowns()

class getregionsasjson:        
    def POST(self):
        try:
            country = getAjaxArg("country")

            #something here would populate this as needed
            if country == "USA":
                return json.dumps(["Alabama", "Georgia", "Michigan", "Texas"])       
            if country == "Canada":
                return json.dumps(["Newfoundland", "Manitoba", "Alberta", "France (quebec) :-)"])

        except Exception, ex:
            print ex.__str__()    

class getregionsashtml:        
    def POST(self):
        try:
            country = getAjaxArg("country")

            #something here would populate this as needed
            if country == "USA":
                return """
                <option value='Virginia'>Virginia</option>
                <option value='Tennessee'>Tennessee</option>
                """
            if country == "Canada":
                return """
                <option value='Nunavit'>Nunavit</option>
                <option value='Sascatchewan'>Sascatchewan</option>
                """
        except Exception, ex:
            print ex.__str__()    

class getanythingyouwant:        
    def POST(self):
        try:
            out = []
            out.append("Current Time is: %s<br />" % datetime.now())
            out.append("""You could do anything you wanted in here.  Full html, go get content from another
            site using urllib, parse an rss feed and format it for your site, etc.
            """)
            
            return "".join(out)
        except Exception, ex:
            print ex.__str__()    


def getAjaxArg(sArg, sDefault=""):
    """Picks out and returns a single value, regardless of GET or POST."""
    try:
        data = web.data()
        dic = None
        if data:
            dic = json.loads(data)
        else:
            # maybe it was a GET?  check web.input()
            dic = dict(web.input())

        if dic:
            if dic.has_key(sArg):
                if dic[sArg]:
                    return dic[sArg]
                else:
                    return sDefault
            else:
                return sDefault
        else:
            return sDefault
    except ValueError:
        raise Exception("getAjaxArg - no JSON arguments to decode. This method required a POST with JSON arguments.")



if __name__ == "__main__":
    app.run()