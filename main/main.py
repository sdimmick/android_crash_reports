import os
import webapp2
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/reports/all')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ], debug=True)
