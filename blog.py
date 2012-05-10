import webapp2
import template
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return template.render_str("post.html", p = self)

class NewPost(template.TemplateHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()

#            self.write(p.key().id())
#            t = Post.get_by_id(p.key().id())
#            self.write(t.subject)

            self.redirect('/blog/' + str(p.key().id()))
        else:
            error = 'subject and content, please!'
            self.render("newpost.html", subject = subject, 
                                        content = content, 
                                        error = error)

class BlogFront(template.TemplateHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('front.html', posts = posts)

class PostPage(template.TemplateHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/(\d+)', PostPage),
                               ('/blog/newpost', NewPost)
                               ], 
                              debug = True)

