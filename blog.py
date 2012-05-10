import webapp2
import template
from google.appengine.ext import db

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class NewPostHandler(template.TemplateHandler):
    def render_new_post(self, subject = '', content = '', error = ''):
        self.render('newpost.html', subject = subject,
                                    content = content,
                                    error = error)

    def get(self):
        self.render_new_post()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blog(subject = subject, content = content)
            b.put()

#            self.write(b.key().id())
#            t = Blog.get_by_id(b.key().id())
#            self.write(t.subject)

            self.redirect('/blog/' + str(b.key().id()))
        else:
            error = 'subject and content, please!'
            self.render_new_post(subject, content, error)

class MainPage(template.TemplateHandler):
    def render_front(self, blog_id = ''):
        if blog_id:
            blogs = []
            blog = Blog.get_by_id(int(blog_id))
            blogs.append(blog)
        else:
            blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')

        self.render('front.html', blogs = blogs) 

    def get(self, blog_id = ''):
        self.render_front(blog_id)

app = webapp2.WSGIApplication([('/blog/?', MainPage),
                               ('/blog/(\d+)', MainPage),
                               ('/blog/newpost', NewPostHandler)], 
                               debug = True)

