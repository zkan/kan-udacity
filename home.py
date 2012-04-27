import webapp2
import rot13
import signup

main_page = """
<html>
<head>
    <title>Kan's Udacity</title>
</head>

<body>

    Hello, Udacity!
    <br>
    <div>
        <a href='unit2/rot13'>rot13</a>
    </div>
    <div>
        <a href='unit2/signup'>signup</a>
    </div>

</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(main_page)

#class Unit2Rot13Handler(webapp2.RequestHandler):
#    def get(self):
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write('rot13')

#class Unit2SignUpHandler(webapp2.RequestHandler):
#    def get(self):
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write('signup')

app = webapp2.WSGIApplication([('/', MainPage), 
                               ('/unit2/rot13', rot13.Rot13Handler),
                               ('/unit2/signup', signup.SignUpHandler)], 
                               debug = True)


