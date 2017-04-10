from google.appengine.ext import ndb

class Message(ndb.Model):
    message_text = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.StringProperty()
    email = ndb.StringProperty()
    rating = ndb.StringProperty()
    ratings = ndb.FloatProperty()

