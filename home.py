import webapp2

main_page = """
<html>
<head>
    <title>Kan's Udacity</title>
</head>

<body>

    Hello, Udacity!
    <br>
    <div>
        <a href='rot13'>rot13</a>
    </div>
    <div>
        <a href='signup'>signup</a>
    </div>
    <div>
        <a href='blog'>blog</a>
    </div>

</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(main_page)

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)

