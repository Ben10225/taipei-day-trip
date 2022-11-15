from flask import *
from data.users import db_attractions
from data.users import db_attraction_by_id
from data.users import db_categories

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


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
	page = request.args.get("page", "0")
	keyword = request.args.get("keyword", "")

	items = db_attractions(keyword)

	datas = []

	def attraction_details(range, page):
		dt = items[range * int(page) + i]
		images = dt["imgs"].split(" ")
		datas.append({
			"id": dt["id"],
			"name": dt["name"],
			"category": dt["category"],
			"description": dt["description"],
			"address": dt["address"],
			"transport": dt["transport"],
			"mrt": dt["mrt"],
			"lat": dt["lat"],
			"lng": dt["lng"],
			"images": images[:-1],
		})
		return datas

	if len(items) - 12 * (int(page)+1) >= 0:
		for i in range(12):
			datas = attraction_details(12, page)
			nextPage = int(page)+1

	elif 0 > len(items) - 12 * (int(page)+1) >= -11:
		lefts = abs(len(items) - 12 * int(page))
		for i in range(lefts):
			datas = attraction_details(lefts, page)
			nextPage = None

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
		images = item["imgs"].split(" ")
		result = {
			"data": {
				"id": item["id"],
				"name": item["name"],
				"category": item["category"],
				"description": item["description"],
				"address": item["address"],
				"transport": item["transport"],
				"mrt": item["mrt"],
				"lat": item["lat"],
				"lng": item["lng"],
				"images": images[:-1]
			}
		}
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