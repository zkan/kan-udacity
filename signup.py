import webapp2
import re

signup_page = """
<!DOCTYPE html>

<html>
<head>
<title>Sign Up</title>
    <style type="text/css">
        .label {text-align: right}
        .error {color: red}
    </style>
</head>

<body>
    <h2>Signup</h2>
    <form method="post">
        <table>
            <tr>
                <td class="label">
                    Username
                </td>
                <td>
                    <input type="text" name="username" value="%(username)s">
                </td>
                <td class="error">
                    %(username_error)s
                </td>
            </tr>

            <tr>
                <td class="label">
                    Password
                </td>
                <td>
                    <input type="password" name="password" value="">
                </td>
                <td class="error">
                    %(password_error)s
                </td>
            </tr>

            <tr>
                <td class="label">
                    Verify Password
                </td>
                <td>
                    <input type="password" name="verify" value="">
                </td>
                <td class="error">
                    %(verify_password_error)s
                </td>
            </tr>

            <tr>
                <td class="label">
                    Email (optional)
                </td>
                <td>
                    <input type="text" name="email" value="%(email)s">
                </td>
                <td class="error">
                    %(email_error)s
                </td>
            </tr>
        </table>

        <input type="submit">
    </form>
    <br>
    <a href = "/">Back</a>
</body>

</html>
"""

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write('Welcome, %s!' % username)

class SignUpHandler(webapp2.RequestHandler):
    def is_valid_username(self, username):
        self.USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
        if not self.USER_RE.match(username):
            return 'That\'s not a valid username.'
        else:
            return ''
            
    def is_valid_password(self, password):
        self.PASS_RE = re.compile(r'^.{3,20}$')
        if not self.PASS_RE.match(password):
            return 'That wasn\'t a valid password.'
        else:
            return ''

    def is_match_password(self, password, verify):
        if password != verify:
            return 'Your passwords didn\'t match.'
        else:
            return ''

    def is_valid_email(self, email):
        if email == '':
            return ''
        self.EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        if not self.EMAIL_RE.match(email):
            return 'That\'s not a valid email.'
        else:
            return ''

    def write_form(self, username = '', email = '', username_error = '', 
                   password_error = '', verify_password_error = '', 
                   email_error = ''):
        self.response.out.write(signup_page % {'username': username, 
                                               'email': email, 
                                               'username_error': username_error, 
                                               'password_error': password_error,
                                               'verify_password_error': verify_password_error, 
                                               'email_error': email_error}) 

    def get(self):
        self.write_form()

    def post(self): 
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        username_error = self.is_valid_username(username)

        password_error = self.is_valid_password(password)
        verify_password_error = ''
        if password_error == '':
            verify_password_error = self.is_match_password(password, verify)

        email_error = self.is_valid_email(email)

        if username_error == '' and password_error == '' and verify_password_error == '' and email_error == '':
            self.redirect('/unit2/welcome?username=%s' % username)
        else:
            self.write_form(username, email, username_error, password_error, 
                            verify_password_error, email_error)

app = webapp2.WSGIApplication([('/unit2/signup', SignUpHandler), 
                               ('/unit2/welcome', WelcomeHandler)], 
                               debug = True)

