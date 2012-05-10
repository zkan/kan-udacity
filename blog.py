import webapp2
import template
import re
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

COOKIE_RE = re.compile(r'.+=; Path=/')
def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return template.render_str("post.html", p = self)

class BlogFront(template.TemplateHandler):
    def get(self):
#        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        posts = Post.all().order('-created')
        self.render('front.html', posts = posts)

class PostPage(template.TemplateHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(template.TemplateHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), 
                     subject = subject, 
                     content = content)
            p.put()

#            self.write(p.key().id())
#            t = Post.get_by_id(p.key().id())
#            self.write(t.subject)

            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content, please!'
            self.render("newpost.html", subject = subject, 
                                        content = content, 
                                        error = error)

class LogOut(template.TemplateHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie", "username=kan; Path=/")
        cookie = self.request.cookies.get('username')
#        if valid_cookie(cookie):
#            self.write('yes, valid')
#        self.redirect('/signup')

app = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/(\d+)', PostPage),
                               ('/blog/newpost', NewPost), 
                               ('/blog/logout', LogOut)
                               ], 
                              debug = True)

