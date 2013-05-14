import os
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/reports/all')

class AdminRedirectHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/admin/config')

app = webapp2.WSGIApplication([
    ('/admin',  AdminRedirectHandler),
    ('/',       MainHandler),
    ], debug=True)
