import webapp2
import jinja2
import cgi
import os
from google.appengine.ext import db
import json
import tweepy
from private import consumer_key, consumer_secret
from urlparse import urlparse 


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Hashtag(db.Model):
    name=db.StringProperty()
    Location=db.StringProperty()
    
class Questions(db.Model):
    contact = db.ReferenceProperty(Hashtag, collection_name="questions")
    question = db.StringProperty()

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        
        info=db.GqlQuery("SELECT * FROM Hashtag").run()
        template_values = {}
        to_append = []
        for i in info:
            to_append.append(i.name)
        template_values['hashtags'] = to_append
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class AskQuestion(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("<html><body><form action='/add-q' method='post'>\n<br />Question for: <input type=text name='hashtag' />\n" + \
                            "<br />Your question (500 char max): <textarea rows=6 cols=40 maxlength=500 name='question'></textarea>1\n" + \
                            "<br /><input type='submit' /></form></body></html>")
        
class AddQ(webapp2.RequestHandler):
    
    def post(self):
        hashtag = Hashtag(name=self.request.get('hashtag').lower().replace("#",""), key_name=self.request.get('hashtag').lower().replace("#",""))
        hashtag.put()
        Questions(contact=hashtag, question=self.request.get('question')).put()
        self.response.write('Success. Maybe.')
        
class GetHashtag(webapp2.RequestHandler):
    """Sends json encoded information about a person"""
    def get(self):
        info = db.GqlQuery("SELECT * FROM Hashtag WHERE name=:1", self.request.get('hashtag'))
        results = True
        try:
            info = info.run().next()
        except:
            questions=[]
            results = False
        to_send = {}
        if results:
            to_send['name'] = info.name
            questions = []
            for q in info.questions:
                questions.append(q.question)
                print q.question
        to_send['result'] = results
        to_send['questions'] = questions
        json_to_send = str(json.dumps(to_send))
        string_to_send = self.request.get('callback') + "(" + json_to_send + ")"
        self.response.write(string_to_send)
        
class Callback(webapp2.RequestHandler):
    
    def get(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'https://citizen-journalist.appspot.com/callback')
        auth.set_request_token(consumer_key, consumer_secret)
        print self.request.get('oauth_verifier')
        print self.request.cookies.get('REQUEST_TOKEN')
       # print auth.get_access_token(self.request.get('oauth_verifier'))

    
class Login(webapp2.RequestHandler):
    
    def get(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'https://citizen-journalist.appspot.com/callback')
        
#        self.response.headers.add_header('Set-Cookie', 'OAUTH_TOKEN = %s' % (auth['oauth_token']))
#        self.response.headers.add_header('Set-Cookie', 'OAUTH_TOKEN_SECRET = %s' % (auth['oauth_token_secret']))
        self.response.headers['Content-Type'] = 'text/html'
        auth_url = auth.get_authorization_url()
        print auth.request_token
        print urlparse("http://foo.bar?" + str(auth.request_token))
        self.response.headers.add_header('Set-Cookie', 'REQUEST_TOKEN = %s' % auth.request_token)
        self.response.write("<html><body><meta HTTP-EQUIV='REFRESH' content='0; url=%s'></body></html>" % (auth_url))

class Test(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.headers.add_header('Set-Cookie', 'email3=foo@bar.baz')
        self.response.write("<html><body><meta HTTP-EQUIV='REFRESH' content='0; url=%s'></body></html>" % ("/test2"))
        
       # self.response.out.write(self.request.cookies.get('email')) 
        
class Test2(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(self.request.cookies.get('email3'))
        
app = webapp2.WSGIApplication([
                               ('/test2', Test2),
                               ('/test', Test),
                               ('/login', Login),
                               ('/callback', Callback),
                               ('/get-hashtag', GetHashtag),
                               ('/ask-question', AskQuestion),
                               ('/add-q', AddQ),
                               ('/index', MainPage),
                               ('/', MainPage)],
                              debug=True)