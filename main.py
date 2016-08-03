from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import webapp2
import json

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UserInfo(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    birthdate = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    my_collection = ndb.KeyProperty(MyCollection)

class MyCollection(ndb.Model):
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

# class RequestBooks(ndb.Model):


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get function reads the file and puts it into the template
        prof_form = jinja_environment.get_template("templates/prof_form.html")
        main = jinja_environment.get_template("templates/main.html")
        user = users.get_current_user()
        if user:
            user_info = {
                "user_nickname": user.nickname(),
                "user_create_logout_url": users.create_logout_url("/")
            }
            self.response.write(prof_form.render(user_info))
        else:
            user_login = {
                "user_create_login_url": users.create_login_url("/")
            }
            self.response.out.write(main.render(user_login))
        #sends it to the client


    def post(self):
        profout_order_form = jinja_environment.get_template("templates/profout_order_form.html")
        user = users.get_current_user()
        name_value = self.request.get("name")
        email_value = self.request.get("email")
        birthdate_value = self.request.get("birthdate")
        phone_value = self.request.get("phone")
        city_value = self.request.get("city")
        genre_value = self.request.get("genre")
        #prepares data for the template
        prof_info = {
          "name_answer": name_value,
          "email_answer": email_value,
          "birthdate_answer": birthdate_value,
          "phone_answer": phone_value,
          "city_answer": city_value,
          "genre_answer": genre_value,
          "user_nickname": user.nickname(),
          "user_create_login_url": users.create_logout_url("/"),
          "user_create_logout_url": users.create_logout_url("/")
          }
        prof_record = UserInfo  (
            name = name_value,
            email = email_value,
            birthdate = birthdate_value,
            phone = phone_value,
            city = city_value,
            genre = genre_value,
            my_collection = send
          )
        send_to_database = prof_record.put()

        #generates final html page
        # and sends the response
        self.response.write(profout_order_form.render(prof_info))

class CollectionHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        main = jinja_environment.get_template("templates/main.html")
        my_collection = jinja_environment.get_template("templates/my_collection.html")
        user_collection = {
            "user_nickname": user.nickname(),
            "user_create_login_url": users.create_logout_url("/"),
            "user_create_logout_url": users.create_logout_url("/")
        }
        self.response.write(my_collection.render(user_info))

    def post(self):
        my_collection = jinja_environment.get_template("templates/my_collection.html")
        title_value = self.request.get("title")
        author_value = self.request.get("email")
        genre_value = self.request.get("genre")
        description_value = self.request.get("description")
        book_details = {
            "title_answer": title_value,
            "author_answer": author_value,
            "genre_answer": genre_value,
            "description_answer": description_value,
        }
        book_to_collection = MyCollection (
            title = title_value,
            author = author_value,
            genre = genre_value,
            description = description_value,
            my_collection_key =
        )
        send_book_to_collection = book_to_collection.put()
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(json.dumps(book_details))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_for_book = jinja_environment.get_template("templates/search_for_book.html")
        user = users.get_current_user()
        user_info = {
            "user_nickname": user.nickname(),
            "user_create_login_url": users.create_logout_url("/"),
            "user_create_logout_url": users.create_logout_url("/")
        }
        self.response.write(search_for_book.render())

    def post(self):
        book_info = jinja_environment.get_template("templates/book_info.html")
        user_info = {
            "user_nickname": user.nickname(),
            "user_create_login_url": users.create_logout_url("/"),
            "user_create_logout_url": users.create_logout_url("/")
        }
        self.response.write(book_info.render(user_info))

app = webapp2.WSGIApplication([
  ("/", MainHandler),
  ("/my_collection", CollectionHandler),
  ("/search_for_book",SearchHandler),
], debug=True)
