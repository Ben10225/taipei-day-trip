from flask import *
from api.model import *
from utils.jwt import jwt_verify
from utils.json_format import booking_details


router_page_booking = Blueprint("router_page_booking", __name__, template_folder="templates")

@router_page_booking.route("/api/booking")
def get_booking():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    uuid = payload["sub"]
    name = payload["name"]

    bookings = Booking.get_bookings(uuid)
    if len(bookings) > 0:
      return {"data": bookings, "name": name}, 200

  except:
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


@router_page_booking.route("/api/booking", methods=["post"])
def create_booking():
  try:
    payload = jwt_verify(request.cookies.get("token"))

    uuid = payload["sub"]
    attraction_Id = request.json["attractionId"]
    date = request.json["date"]
    time = request.json["time"]
    price = request.json["price"]

    if not attraction_Id or not date or not time or not price:
      return {"error": True, "message": "輸入不正確"}, 400

    status = Booking.create_booking(uuid, attraction_Id, date, time, price)
    if status == "exists":
      # 需要再去處理重複的行程
      return {"error": True, "message": "此行程已存在"}, 400
    elif status == "created":
      return {"ok": True}, 200
    else:
      return {"error": True, "message": "伺服器內部錯誤"}, 400

  except:
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp
