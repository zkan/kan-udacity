import webapp2
import template
import cgi

def rot13(s):
    s = s.encode('rot13')
    s = cgi.escape(s, quote = True)
    return s

class Rot13(template.TemplateHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13_text = ''
        text = self.request.get('text')
        if text:
            rot13_text = rot13(text)

        self.render('rot13-form.html', text = rot13_text)

app = webapp2.WSGIApplication([('/rot13', Rot13)
                               ], 
                              debug = True)

