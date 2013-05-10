import uuid
from google.appengine.ext import ndb

class Config(ndb.Model):
    pivotal_project_id      = ndb.StringProperty()
    pivotal_auth_token      = ndb.StringProperty()
    
    @classmethod
    def get_app_config(cls):
        return Config.get_or_insert('config')

class AccessToken(ndb.Model):
    token = ndb.StringProperty()

    @classmethod
    def is_authorized(cls, token):
        query = AccessToken.query(AccessToken.token == token)
        access_token = query.get()
        return access_token != None

    @classmethod
    def get_all(cls):
        query = AccessToken.query()
        return query.fetch()

    @classmethod
    def generate_new_token(cls):
        token = AccessToken()
        token.token = uuid.uuid4().hex
        token.put()
        return token

    @classmethod
    def delete_token(cls, token_value):
        query = AccessToken.query()
        query.filter(AccessToken.token == token_value)
        token = query.get()
        if token:
            token.key.delete()
