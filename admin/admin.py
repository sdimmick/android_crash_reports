import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
from models import Config, AccessToken

class ConfigHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        config = Config.get_app_config()
        self.render_template(config)

    def post(self):
        user = users.get_current_user()

        if user:
            pivotal_project_id = self.request.get('pivotal_project_id')
            pivotal_auth_token = self.request.get('pivotal_auth_token')

            config = Config.get_app_config()
            config.pivotal_project_id = pivotal_project_id
            config.pivotal_auth_token = pivotal_auth_token
            config.put()
        
            self.render_template(config)
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def render_template(self, config):
        template_values = {
            'config': config,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/config.html')
        self.response.out.write(template.render(path, template_values))

class AccessTokenHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        tokens = AccessToken.get_all()
        self.render_template(tokens)

    def post(self):
        user = users.get_current_user()
        if user:
            AccessToken.generate_new_token()
            tokens = AccessToken.get_all()
            self.render_template(tokens)
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def delete(self):
        user = users.get_current_user()
        if user:
            token = AccessToken.delete_token(self.request.get('token'))
            tokens = AccessToken.get_all()
            self.render_template(tokens)
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
    def render_template(self, tokens):
        template_values = {
            'tokens': tokens,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/tokens.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/admin/config', ConfigHandler),
    ('/admin/tokens', AccessTokenHandler),
    ], debug=True)
