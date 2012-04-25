import webapp2

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
                    <input type="text" name="username" value="">
                </td>
                <td class="error">

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

                </td>
            </tr>

            <tr>
                <td class="label">
                    Email (optional)
                </td>
                <td>
                    <input type="text" name="email" value="">
                </td>
                <td class="error">

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

class SignUpHandler(webapp2.RequestHandler):
    def write_form(self, text = ''):
        self.response.out.write(signup_page % {'text': text})

    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')

        self.write_form(text)

app = webapp2.WSGIApplication([('/unit2/signup', SignUpHandler)], debug = True)

