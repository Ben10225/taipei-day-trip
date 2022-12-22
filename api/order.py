import base64
import requests
from flask import *
from api.model import *
from utils.jwt import jwt_verify
from utils.create_payment import create_orders


router_page_order = Blueprint("router_page_order", __name__, template_folder="templates")

@router_page_order.route("/api/orders", methods=["post"])
def create_order():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    uuid = payload["sub"]
    prime = request.json['prime']
    order = request.json['order']

    if not prime or not order or len(order["trips"])==0:
      return {"error": True, "message": "資料輸入錯誤"}, 400

    try:
      url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
      partner_key = "partner_xx7qA40I1lNDglRMGRM6KcfFGFhE4xR3JKExEZwiuA4p18TCBBadXC4m"
      headers = {
        'Content-Type': 'application/json',
        "x-api-key": partner_key
      }
      data = {
        "prime": prime,
        "partner_key": partner_key,
        "merchant_id": "bbnn669999_ESUN",
        "details":"TapPay Taipei-day-trip orders",
        "amount": order["totalPrice"],
        "cardholder": {
          "phone_number": order["contact"]["phone"],
          "name": base64.b64encode(order["contact"]["name"].encode("utf-8")).decode("ascii"),
          "email": order["contact"]["email"]
        },
        "remember": True
      }

      r = requests.post(url, headers=headers, data=json.dumps(data))
      status = json.loads(r.text)["status"]

      if status != 0:
        number, payment_id = create_orders(order, uuid, False)
        result = {
          "number": number + "-" + str(payment_id),
          "payment": {
            "status": status,
            "message": "付款失敗"
          }
        }
        return {"data": result}, 200

      number, payment_id = create_orders(order, uuid, True)
      result = {
        "number": number + "-" + str(payment_id),
        "payment": {
          "status": 0,
          "message": "付款成功"
        }
      }
      return {"data": result}, 200  

    except Exception as e:
      print(e)
      return {"error": True, "message": "伺服器錯誤"}, 500

  except Exception as e:
    print(e)
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


@router_page_order.route("/api/order/<order_number>")
def get_order_details(order_number):
  try:
    jwt_verify(request.cookies.get("token"))

    payment_id = order_number.split("-")[1]
    number = order_number.split("-")[0]

    if not payment_id or not number:
      return {"error": True, "message": "載入錯誤"}, 400

    payment, trips = Order.get_order_details(payment_id, number)

    trips_details = []
    for trip in trips:
      detail = {
        "attraction": {
          "id": trip["attraction_id"],
          "name": trip["attraction_name"],
          "address": trip["attraction_address"],
          "image": trip["attraction_image"],
        },
        "price": trip["attraction_price"],
        "date": trip["attraction_date"],
        "time": trip["attraction_time"]
      }
      trips_details.append(detail)

    result = {
      "number": order_number,
      "price": payment["total_price"],
      "trips": trips_details,
      "contact": {
        "name": payment["contact_name"],
        "email": payment["contact_email"],
        "phone": payment["contact_phone"]
      }
    }

    return {"data": result}, 200 

  except Exception as e:
    print(e)
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp