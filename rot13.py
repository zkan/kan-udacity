import webapp2
import cgi

rot13_page = """
<!DOCTYPE html>

<html>
    <head>
        <title>Unit 2 Rot 13</title>
    </head>

<body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
        <textarea name="text"
                  style="height: 100px; width: 400px;">%(text)s</textarea>
        <br>
        <input type="submit">
    </form>
    <br>
    <a href = "/">Back</a>
</body>

</html>
"""

def rot13(s):
    s = s.encode('rot13')
    s = cgi.escape(s, quote = True)
    return s

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self, text = ''):
        self.response.out.write(rot13_page % {'text': text})

    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')
        text = rot13(text)

        self.write_form(text)

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13Handler)], debug = True)

