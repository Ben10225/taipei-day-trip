from flask import *
from api import *

app = Flask(__name__, static_folder="public", static_url_path="/")
app.register_blueprint(router_page_attractions)
app.register_blueprint(router_page_auth)
app.register_blueprint(router_page_booking)
app.register_blueprint(router_page_order)
app.register_blueprint(router_page_member)


app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# 排序 json
app.config["JSON_SORT_KEYS"]=False


@app.after_request 
def after_request(response):
	header = response.headers
	header["Access-Control-Allow-Origin"] = "*"
	return response


# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")
	
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/member")
def member():
	return render_template("member.html")

if __name__ == "__main__":
	app.run(port=4000, host="0.0.0.0", debug=True)