import webapp2
import jinja2
import cgi
import os
from google.appengine.ext import db
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Person(db.Model):
    name=db.StringProperty()
    Location=db.StringProperty()
    
class Questions(db.Model):
    contact = db.ReferenceProperty(Person, collection_name="questions")
    question = db.StringProperty()

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Hello, webapp World!')
        
class AskQuestion(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("<html><body><form action='/add-q' method='post'>\n<br />Question for: <input type=text name='person' />\n" + \
                            "<br />Your question (500 char max): <textarea rows=6 cols=40 maxlength=500 name='question'></textarea>1\n" + \
                            "<br /><input type='submit' /></form></body></html>")
        
class AddQ(webapp2.RequestHandler):
    
    def post(self):
        person = Person(name=self.request.get('person').lower(), key_name=self.request.get('person').lower())
        person.put()
        Questions(contact=person, question=self.request.get('question')).put()
        self.response.write('Success. Maybe.')
        
class GetPerson(webapp2.RequestHandler):
    """Sends json encoded information about a person"""
    def get(self):
        info = db.GqlQuery("SELECT * FROM Person WHERE name=:1", self.request.get('person'))
        info = info.run().next()
        to_send = {}
        to_send['name'] = info.name.title()
        questions = []
        for q in info.questions:
            questions.append(q.question)
        to_send['questions'] = questions
        self.response.write(json.dumps(to_send))
        
app = webapp2.WSGIApplication([
                               ('/get-person', GetPerson),
                               ('/ask-question', AskQuestion),
                               ('/add-q', AddQ),
                               ('/index', MainPage),
                               ('/', MainPage)],
                              debug=True)