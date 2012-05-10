import webapp2
import re
import template
import user
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Welcome(template.TemplateHandler):
    def get(self):
        username = self.request.cookies.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else: 
            self.redirect('/signup')

class SignUp(template.TemplateHandler):
    def get(self):
        self.render('signup-form.html')

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        params = dict(username = username, 
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True
        
        if have_error:
            self.render('signup-form.html', **params)
        else:
            username_in_db = db.GqlQuery("select * from User where username = :username", username)
            
            self.write(username)
#            if not username_in_db.get():
#                u = user.User(username = username, 
#                              password = password, 
#                              email = email)
#                u.put()
#                header_value = str('username=%s; Path=/' % username)
#                self.response.headers.add_header('Set-Cookie', header_value)
#                self.redirect('/welcome')
#            else:
#               params['error_username'] = "That user already exists."
#               self.render('signup-form.html', **params)

app = webapp2.WSGIApplication([('/signup', SignUp), 
                               ('/welcome', Welcome)
                               ], 
                              debug = True)

