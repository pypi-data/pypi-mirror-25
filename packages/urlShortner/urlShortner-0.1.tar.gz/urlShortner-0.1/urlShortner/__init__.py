from flask import Flask, request
from se.urlShortner.routes import urls
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.debug = True

for url in urls:
	app.add_url_rule(url[0], methods=url[1], view_func=url[2])

if __name__ == '__main__':
	app.run(debug=True)
