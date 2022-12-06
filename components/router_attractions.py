from flask import *
from components.model import *
from data.DBconnection import *

router_page_attractions = Blueprint("router_page_attractions", __name__, template_folder="templates")

sql_conn = Users()

# attractions api
@router_page_attractions.route("/api/attractions")
def attractions():
	try:
		page = request.args.get("page", "")
		keyword = request.args.get("keyword", "")

		if not page or not page.isdigit():
			return {
				"error": True,
				"message": "資料輸入錯誤"
			}, 400

		# sql_conn.set_page_keyword(page, keyword)
		items, next = sql_conn.attractions(page, keyword)

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
			}, 400

		result = {
			"nextPage": nextPage,
			"data" : datas 
		}
		return result, 200

	except Exception as e:
		print(f"{e}:伺服器錯誤")
		return {
			"error": True,
			"message": "伺服器發生錯誤"
		}, 500


# attraction api
@router_page_attractions.route("/api/attraction/<id>")
def attractionitem(id):
	try:
		if id.isdigit():
			id = int(id)
		else:
			return {
				"error": True,
				"message": "無法辨識"
			}, 500
		
		item = sql_conn.attraction(id)

		if item:
			result = {
				"data": attraction_details(item)
			}
			status_code = 200
		else:
			result = {
				"error": True,
				"message": "查無此資料"
			}
			status_code = 400
		return result, status_code

	except Exception as e:
		print(f"{e}:伺服器錯誤")
		return {
			"error": True,
			"message": "伺服器發生錯誤"
		}, 500


# categories api
@router_page_attractions.route("/api/categories")
def categories():
	try:
		items = sql_conn.categories()
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
			
	except Exception as e:
		print(f"{e}:伺服器錯誤")
		return {
			"error": True,
			"message": "伺服器發生錯誤"
		}, 500