import random
import string
import os.path
import json
from datetime import datetime

import cherrypy
import jinja2

"""Add in current dir"""
import jinja2plugin
import jinja2tool

class PasswordGenerator():
    def __init__(self):
        self.title = "Generate password"

    @cherrypy.expose
    def index(self):
        return {'title' : self.title}

    @cherrypy.expose
    def test(self):
        hello = "Hello world"
        return {'hello' : hello}

    @cherrypy.expose
    def generate(self, length=8):
        password = ''.join(random.sample(string.hexdigits, int(length)))
        """cherrypy.session['mystring'] = password"""
        self.saveJson(password)
        return {'word' : password , 'title' : self.title}

    @cherrypy.expose
    def log(self):
        dico = self.loadJson()
        if len(dico) == 0 :
            out = '<p>No link in the database.</p>'
        else:
            out = '<ol id="words">'
            for i in range(len(dico["logs"])):
                out += '''<li>{}</li>'''.format(dico["logs"][i]["password"])
            out += '</ol>'
        return {'words': out, 'title' : self.title}

    def loadJson(self):
        """Load passwords from json file."""
        try:
            with open('log.json', 'r') as file:
                content = json.loads(file.read())
                return content
        except:
            cherrypy.log('Loading database failed.')
            return []

    def saveJson(self, password):
        """Save passwords in json file."""
        try:
            with open('log.json', 'r') as file:
                data = json.load(file)
            with open('log.json', 'w') as file:
                today = datetime.now().strftime("%Y-%m-%d %H:%M")
                data["logs"] += [{"date": today, "password":password}]
                print(data)
                json.dump(data, file)
        except:
            cherrypy.log('Saving database failed.')

if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(PasswordGenerator(), config='server.conf')