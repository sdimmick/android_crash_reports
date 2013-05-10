from google.appengine.ext import webapp
register = webapp.template.create_template_register()

def get_id(value):
    return value.key.id()

register.filter(get_id)
