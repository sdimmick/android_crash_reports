import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from models import Config, AccessToken

class ConfigHandler(webapp2.RequestHandler):
    def get(self):
        config = Config.get_app_config()
        self.render_template(config)

    def post(self):
        post_to_pivotal = self.request.get('post_to_pivotal')
        pivotal_project_id = self.request.get('pivotal_project_id')
        pivotal_auth_token = self.request.get('pivotal_auth_token')

        config = Config.get_app_config()
        config.post_to_pivotal = post_to_pivotal.lower() == "true"
        config.pivotal_project_id = pivotal_project_id
        config.pivotal_auth_token = pivotal_auth_token
        config.put()
        
        self.render_template(config)

    def render_template(self, config):
        template_values = {
            'config': config,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/config.html')
        self.response.out.write(template.render(path, template_values))

class AccessTokenHandler(webapp2.RequestHandler):
    def get(self):
        tokens = AccessToken.get_all()
        self.render_template(tokens)

    def post(self):
        AccessToken.generate_new_token()
        tokens = AccessToken.get_all()
        self.render_template(tokens)

    def delete(self):
        token = AccessToken.delete_token(self.request.get('token'))
        tokens = AccessToken.get_all()
        self.render_template(tokens)
        
    def render_template(self, tokens):
        template_values = {
            'tokens': tokens,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/tokens.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/admin/tokens', AccessTokenHandler),
    ('/admin/config', ConfigHandler),
    ], debug=True)
