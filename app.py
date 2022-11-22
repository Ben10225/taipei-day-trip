from flask import *
from data.users import db_attractions
from data.users import db_attraction_by_id
from data.users import db_categories

app = Flask(__name__, static_folder="public", static_url_path="/")

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# 排序 json
app.config["JSON_SORT_KEYS"]=False


def attraction_details(item):
	images = item["imgs"].split(" ")
	details = {
		"id": item["id"],
		"name": item["name"],
		"category": item["category"],
		"description": item["description"],
		"address": item["address"].replace(" ",""),
		"transport": item["transport"],
		"mrt": item["mrt"],
		"lat": item["lat"],
		"lng": item["lng"],
		"images": images[:-1],
	}
	return details


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


# attractions api
@app.route("/api/attractions")
def attractions():
	page = request.args.get("page", "")
	keyword = request.args.get("keyword", "")

	if not page or not page.isdigit():
		return {
			"error": True,
			"message": "資料輸入錯誤"
		}, 400

	items, next = db_attractions(page, keyword)

	if next:
		nextPage = int(page)+1
	else:
		nextPage = None

	datas = []

	if items:
		for i in range(len(items)):
			item_detail = attraction_details(items[i])
			datas.append(item_detail)
	else:
		return {
			"error": True,
			"message": "已無足夠資訊"
		}, 500

	result = {
		"nextPage": nextPage,
		"data" : datas 
	}
	return result, 200


# attraction/<id> api
@app.route("/api/attraction/<id>")
def attractionitem(id):
	if id.isdigit():
		id = int(id)
	else:
		return {
			"error": True,
			"message": "無法辨識"
		}, 500
	
	item = db_attraction_by_id(id)

	if item:
		result = attraction_details(item)
		status_code = 200
	else:
		result = {
			"error": True,
			"message": "查無此資料"
		}
		status_code = 400
	return result, status_code


# categories api
@app.route("/api/categories")
def categories():

	items = db_categories()

	if items:
		cates = []
		for i in items:
			if i[0] not in cates:
				cates.append(i[0])
		return {
			"data": cates
		}, 200
	else:
		return {
			"error": True,
			"message": "無任何類別"
		}, 500


@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(port=3000, host="0.0.0.0", debug=True)