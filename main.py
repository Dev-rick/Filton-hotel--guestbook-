# -*- coding: utf-8 -*-
import webapp2
import os
import jinja2
from models import Message
import counter


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainPage(BaseHandler):
    def get(self):
        average_rating = counter.get_average_rating()
        params = {"average_rating": average_rating}
        return self.render_template("home.html", params)


class ResultHandler(BaseHandler):
    def post(self):
        bad = self.request.get("bad")
        if bad:
            text = "bad"
            ratings = 1.0
        not_special = self.request.get("not_special")
        if not_special:
            text = "not special"
            ratings = 2.0
        good = self.request.get("good")
        if good:
            text = "good"
            ratings = 3.0
        very_good = self.request.get("very_good")
        if very_good:
            text = "very good"
            ratings = 4.0
        excellent = self.request.get("excellent")
        if excellent:
            text = "excellent"
            ratings = 5.0
        message = self.request.get("some_text")
        if "<script>" in message:
            message="Sorry you can't hack me!"
        elif not message:
            message = "None"
        author = self.request.get("author")
        if not author:
            author = "Anonymous"
        email = self.request.get("email")
        if not email:
            email = "None"
        try:
            msg_object = Message(author=author, email=email,
                             message_text=message.replace("<script>", ""),
                             rating=text, ratings=ratings)  # another way to fight JS injection
            msg_object.put()
        except UnboundLocalError:
            return self.render_template("error1.html")
        average_rating = counter.get_average_rating()
        params = {"average_rating": average_rating}
        return self.render_template("home.html", params)


class MessageListHandler(BaseHandler):
    def get(self):
        ratings = counter.get_average_rating()
        messages = Message.query().fetch()
        params = {"messages": messages,"ratings": ratings}
        return self.render_template("message_list.html", params=params)


class MessageDetailsHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        date_created = str(message.created)[0:10]
        time_created = str(message.created)[11:19]
        params = {"message": message,"date_created": date_created, "time_created": time_created}
        return self.render_template("message_details.html", params=params)


class DeleteMessageHandler(BaseHandler):
    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.key.delete()
        messages = Message.query().fetch()
        params = {"messages": messages}
        return self.render_template("message_list.html", params=params)


class SearchMessageHandler(BaseHandler):
    def post(self):
        messages = Message.query().fetch()
        search = self.request.get("search")
        search = search.lower()
        result_list = []
        text = self.request.get("text")
        if text:
            for message in messages:
                index_position = message.message_text.lower().find(search)
                if index_position > -1:
                    result_list.append(message)
        date = self.request.get("date")
        if date:
            for message in messages:
                date = str(message.created)[0:10]
                index_position = date.find(search)
                if index_position > -1:
                    result_list.append(message)
        rating = self.request.get("ratings")
        if rating:
            for message in messages:
                rating = str(message.rating)
                index_position = rating.find(search)
                if index_position > -1:
                    result_list.append(message)
        else:
            for message in messages:
                index_position = message.message_text.lower().find(search)
                if index_position > -1:
                    result_list.append(message)
        params = {"result_list": result_list}
        return self.render_template("message_list.html", params=params)



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/message-list', MessageListHandler, name="msg-list"),
    webapp2.Route('/message/search', SearchMessageHandler),
    webapp2.Route('/message/<message_id:\d+>', MessageDetailsHandler),
    webapp2.Route('/message/<message_id:\d+>/delete', DeleteMessageHandler),
], debug=True)