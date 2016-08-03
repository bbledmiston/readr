from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import webapp2
import json

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Book(ndb.Model):
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class UserInfo(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    birthdate = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    my_collection = ndb.KeyProperty(repeated=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get function reads the file and puts it into the template
        profout_order_form = jinja_environment.get_template("templates/profout_order_form.html")
        prof_form = jinja_environment.get_template("templates/prof_form.html")
        main = jinja_environment.get_template("templates/main.html")
        user = users.get_current_user()
        if user:
            current_user = UserInfo.get_by_id(user.user_id())
            user_info = {
                "user_nickname": user.nickname(),
                "user_create_logout_url": users.create_logout_url("/")
            }
            if current_user:
                self.response.write(profout_order_form.render(user_info))
            else:
                self.response.write(prof_form.render(user_info))
        else:
            user_login = {
                "user_create_login_url": users.create_login_url("/")
            }
            self.response.write(main.render(user_login))
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
            id = user.user_id()
          )
        print prof_record
        prof_record.put()

        self.response.write(profout_order_form.render(prof_info))

class CollectionHandler(webapp2.RequestHandler):
    book_to_collection = []

    def get(self):
        user = users.get_current_user()
        main = jinja_environment.get_template("templates/main.html")
        my_collection_html = jinja_environment.get_template("templates/my_collection.html")
        # user_collection = {
        #     "user_nickname": user.nickname(),
        #     "user_create_login_url": users.create_logout_url("/"),
        #     "user_create_logout_url": users.create_logout_url("/")
        # }

        current_user = UserInfo.get_by_id(user.user_id())
        books = []
        for book_key in current_user.my_collection:
            new_book = {
                "book_name": book_key.get().title,
                "book_author": book_key.get().author,
                "book_description": book_key.get().description,
                "book_genre": book_key.get().genre,            "user_nickname": user.nickname(),
                "user_create_login_url": users.create_logout_url("/"), "user_create_logout_url": users.create_logout_url("/")
                }
            books.append(new_book)

        books_to_html = {
                "books": books,
                }

        self.response.write(my_collection_html.render(books_to_html))

    def post(self):
        user = users.get_current_user()
        my_collection_html = jinja_environment.get_template("templates/my_collection.html")
        temp_html = jinja_environment.get_template("templates/temp.html")
        title_value = self.request.get("title")
        author_value = self.request.get("author")
        genre_value = self.request.get("genre")
        description_value = self.request.get("description")

        book_details = {
            "title_answer": title_value,
            "author_answer": author_value,
            "genre_answer": genre_value,
            "description_answer": description_value,
        }
        book_to_collection = Book (
            title = title_value,
            author = author_value,
            genre = genre_value,
            description = description_value,
        )
        print book_to_collection
        book_key = book_to_collection.put()
        current_user = UserInfo.get_by_id(user.user_id())
        current_user.my_collection.append(book_key)
        current_user.put()

        # jsonstring = self.request.body
        # jsonobject = json.loads(jsonstring)
        # self.response.headers["Content-Type"] = "application/json"
        # self.response.write(json.dumps(book_details))

        books = []
        for book_key in current_user.my_collection:
            new_book = {
                "book_name": book_key.get().title,
                "book_author": book_key.get().author,
                "book_description": book_key.get().description,
                "book_genre": book_key.get().genre
                }
            books.append(new_book)

        books_to_html = {
                "books": books,
                }

        self.response.write(temp_html.render(books_to_html))



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
        user = users.get_current_user()
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
