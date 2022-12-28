from flask import *
from api.model import *
from utils.jwt import *
import boto3

from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client('s3',
  aws_access_key_id = os.getenv("aws_access_key_id"),
  aws_secret_access_key = os.getenv("aws_secret_access_key"),
  region_name = os.getenv("region_name")
)

router_page_member = Blueprint("router_page_member", __name__, template_folder="templates")


@router_page_member.route("/api/member")
def get_history():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    uuid = payload["sub"]

    orders = History.get_user_orders(uuid)

    if not orders:
      return {"data": None}, 200

    history = []

    for order in orders:
      attractions_info = History.get_user_orders_attractions(order["payment_id"], order["order_number"])

      item = {
        "orderNumber": order["order_number"]+ "-" + str(order["payment_id"]),
        "totalPrice": order["total_price"],
        "contactName": order["contact_name"],
        "contactEmail": order["contact_email"],
        "contactPhone": order["contact_phone"],
        "trips": attractions_info,
        "time": str(order["time"])
      }
      history.append(item)

    return {"data": history}, 200


  except Exception as e:
    print(e)
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


@router_page_member.route("/api/member/name", methods=["post"])
def change_user_name():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    uuid = payload["sub"]
    name = request.json['name']

    if not name:
      return {"error": True, "message": "資料輸入錯誤"}, 400
    
    History.update_user_name(uuid, name)
    token = jwt_encode(uuid, name)

    resp = make_response({"ok": True}, 200)
    resp.set_cookie('token', '', 0)
    resp.set_cookie("token", token)
    return resp

  except Exception as e:
    print(e)
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


@router_page_member.route("/api/member/getimg")
def getimg():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    uuid = payload["sub"]

    get_url = s3.generate_presigned_url(
      "get_object",
      Params = {
        "Bucket": os.getenv("bucket_name"),
        "Key": uuid,
      },                                  
      ExpiresIn=3600)

    return {"data": get_url}, 200

  except Exception as e:
    print(e)
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


