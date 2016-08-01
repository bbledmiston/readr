from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class prof_form(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    birthdate = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get function reads the file and puts it into the template
        template = jinja_environment.get_template('templates/prof_form.html')
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
        self.response.out.write('%s' % greeting)
        #sends it to the client
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/profout_order_form.html')
        name_value = self.request.get('name')
        email_value = self.request.get('email')
        birthdate_value = self.request.get('birthdate')
        phone_value = self.request.get('phone')
        city_value = self.request.get('city')
        genre_value = self.request.get('genre')
        #prepares data for the template
        prof_form = {
          'name_answer': name_value,
          'email_answer': email_value,
          'birthdate_answer': birthdate_value,
          'phone_answer': phone_value,
          'city_answer': city_value,
          'genre_answer': genre_value,
          }
        prof_record = Form(
            name = name_value,
            email = email_value,
            birthdate = birthdate_value,
            phone = phone_value,
            city = city_value,
            genre = genre_value,
          )
        key = prof_record.put()
        #generates final html page
        html_page = template.render(prof_form)
        # and sends the response
        self.response.write(html_page)



app = webapp2.WSGIApplication([
  ('/', MainHandler),
], debug=True)
