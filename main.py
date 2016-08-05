from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
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
    book_owner_id = ndb.StringProperty()

class Requests(ndb.Model):
    book_id = ndb.StringProperty(required=True)
    user_from = ndb.StringProperty(required=True)
    user_to = ndb.StringProperty(required=True)

class UserInfo(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    birthdate = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    my_collection = ndb.KeyProperty(repeated=True)
    user_id = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #get function reads the file and puts it into the template
        main_html = jinja_environment.get_template("templates/main.html")
        create_profile = jinja_environment.get_template("templates/create_profile.html")
        main = jinja_environment.get_template("templates/home.html")
        user = users.get_current_user()

        if user:

            current_user = UserInfo.query().filter(UserInfo.user_id==user.user_id()).get()

            user_info = {
                "user_nickname": user.nickname(),
                "user_create_logout_url": users.create_logout_url("/")
                }

            if current_user:

                request_query = Requests.query().filter(Requests.user_to==user.user_id()).fetch()

                list_of_requests = []
                for request in request_query:
                    every_request = {
                        "this_book_id": request.book_id,
                        "this_owner_id": request.user_from
                    }
                    list_of_requests.append(every_request)

                # self.response.write(list_of_requests)

                user_info["user_requests"] = list_of_requests

                user_details = {
                          "user_name": current_user.name,
                          "user_email": current_user.email,
                          "user_birthdate": current_user.birthdate,
                          "user_number": current_user.phone,
                          "user_city": current_user.city,
                          "user_fav_genre": current_user.genre,
                          }
                user_info["user_details"] = user_details
                self.response.write(main_html.render(user_info))
            else:
                self.response.write(create_profile.render(user_info))
        else:
            user_login = {
                "user_create_login_url": users.create_login_url("/")
            }
            self.response.write(main.render(user_login))
        #sends it to the client


    def post(self):
        main_html = jinja_environment.get_template("templates/main.html")
        user = users.get_current_user()
        name_value = self.request.get("name")
        email_value = self.request.get("email")
        birthdate_value = self.request.get("birthdate")
        phone_value = self.request.get("phone")
        city_value = self.request.get("city")
        genre_value = self.request.get("genre")
        #prepares data for the template
        user_details = {
                "user_name": name_value,
                "user_email": email_value,
                "user_birthdate": birthdate_value,
                "user_number": phone_value,
                "user_city": city_value,
                "user_fav_genre": genre_value,
            }

        prof_info = {"user_details": user_details,
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
            user_id = user.user_id(),
          )
        print prof_record
        prof_record.put()
        self.response.write(main_html.render(prof_info))

class CollectionHandler(webapp2.RequestHandler):
    book_to_collection = []

    def get(self):
        user = users.get_current_user()
        main = jinja_environment.get_template("templates/home.html")
        my_collection_html = jinja_environment.get_template("templates/my_collection.html")
        current_user = UserInfo.query().filter(UserInfo.user_id==user.user_id()).get()
        data_sent = self.request.body

        books = []
        for book_key in current_user.my_collection:
            new_book = {
                "book_name": book_key.get().title,
                "book_author": book_key.get().author,
                "book_description": book_key.get().description,
                "book_genre": book_key.get().genre,
                "book_owner_id": book_key.get().book_owner_id,
                "user_nickname": user.nickname(),
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

        current_user = UserInfo.query().filter(UserInfo.user_id==user.user_id()).get()

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
            book_owner_id = user.user_id()
        )
        print book_to_collection
        book_key = book_to_collection.put()
        current_user.my_collection.append(book_key)
        current_user.put()

        books = []
        for book_key in current_user.my_collection:
            new_book = {
                "book_name": book_key.get().title,
                "book_author": book_key.get().author,
                "book_description": book_key.get().description,
                "book_genre": book_key.get().genre,
                "book_owner_id": book_key.get().book_owner_id,
                # "book_id": book_key.key.id()
                }
            books.append(new_book)

        books_to_html = {
                "books": books,
                }

        self.response.write(my_collection_html.render(books_to_html))



class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_feed = jinja_environment.get_template("templates/search_feed.html")
        user = users.get_current_user()
        user_info = {
            "user_nickname": user.nickname(),
            "user_create_logdin_url": users.create_logout_url("/"),
            "user_create_logout_url": users.create_logout_url("/")
        }

        list_of_books = []
        book_query = Book.query().fetch()
        print book_query
        for book in book_query:
            every_book= {
                "book_name": book.title,
                "book_author": book.author,
                "book_description": book.description,
                "book_genre": book.genre,
                "book_id": book.key.id(),
                "book_owner_id": book.book_owner_id
            }
            print book
            list_of_books.append(every_book)


        list_of_books_to_html = {
            "list_of_books": list_of_books
        }

        self.response.write(search_feed.render(list_of_books_to_html))

    def post(self):
        user = users.get_current_user()
        search_feed = jinja_environment.get_template("templates/search_feed.html")
        user_info = {
            "user_nickname": user.nickname(),
            "user_create_login_url": users.create_logout_url("/"),
            "user_create_logout_url": users.create_logout_url("/")
        }
        text_to_search = self.request.get("text_to_search")
        book_query = Book.query()
        book_query0 = book_query.filter(Book.title==text_to_search).fetch()
        book_query1 = book_query.filter(Book.author==text_to_search).fetch()
        book_query2 = book_query.filter(Book.genre==text_to_search).fetch()
        books_found = []

        for book0 in book_query0:
            # for book in book_query1:
            #     for book in book_query2:
            every_book0 = {
                "book_name": book0.title,
                "book_author": book0.author,
                "book_description": book0.description,
                "book_genre": book0.genre
            }
            books_found.append(every_book0)

        for book1 in book_query1:
            every_book1 = {
                "book_name": book1.title,
                "book_author": book1.author,
                "book_description": book1.description,
                "book_genre": book1.genre
            }
            books_found.append(every_book1)

        for book2 in book_query2:
            every_book2= {
                "book_name": book2.title,
                "book_author": book2.author,
                "book_description": book2.description,
                "book_genre": book2.genre
            }
            books_found.append(every_book2)

        books_found_html = {
            "books_found": books_found
        }

        info = self.request.body

        books_found_html["data"] = info
        self.response.write(search_feed.render(books_found_html))

        #Now do requests

class SaveRequest(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        book_id_value = self.request.get("book_id")
        book_owner_id_value = self.request.get("book_owner_id")

        request_details = {
            "this_book_id": book_id_value,
            "this_book_owner_id": book_owner_id_value,
            "current_user": user.user_id()
        }

        book_request = Requests (
            book_id = book_id_value,
            user_from = user.user_id(),
            user_to = book_owner_id_value
        )

        print book_request
        book_request_key = book_request.put()

        self.response.write("It worked!")

class Approve(webapp2.RequestHandler):

    def post(self):

        user = users.get_current_user()
        current_user = UserInfo.query().filter(UserInfo.user_id==user.user_id()).get()


        book_value = self.request.get("book_id")
        book_owner_id_value = self.request.get("owner_id")

        book_owner = UserInfo.query().filter(UserInfo.user_id==book_owner_id_value).get()



        approval = mail.EmailMessage (
            sender=current_user.email,
            subject="Your request has been approved."
            )
        approval.to = "Mamadou Diallo <" + book_owner.email   + ">"
        approval.body = "Dear Mamadou Outlook: Thanks for requesting the book _book on _date. Where and when would you like to meet up so we can exchange books. I'd like your book _book in exchange. See you soon!"

        approval.send()

        self.response.write("Email Sent!")



class Reject(webapp2.RequestHandler):
    def get(self):

        # request_query =  Requests.query().filter(Requests.user_to==user.user_id()).fetch()

        self.response.write("Email Rejected!")









app = webapp2.WSGIApplication([
  ("/", MainHandler),
  ("/my_collection", CollectionHandler),
  ("/search_feed",SearchHandler),
  ("/save_request", SaveRequest),
  ("/approve", Approve),
  ("/reject", Reject)
], debug=True)
