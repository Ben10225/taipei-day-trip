from flask import *
from components.router_attractions import router_page_attractions
from components.router_member import router_page_member

app = Flask(__name__, static_folder="public", static_url_path="/")
app.register_blueprint(router_page_attractions)
app.register_blueprint(router_page_member)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# 排序 json
app.config["JSON_SORT_KEYS"]=False


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


app.run(port=3000, host="0.0.0.0", debug=True)