
import uuid
from flask import *
from flask_bcrypt import Bcrypt
from utils.validate import *
from utils.jwt import *
from api.model import *

bcrypt = Bcrypt()
router_page_member = Blueprint("router_page_member", __name__, template_folder="templates")


# sign_up api
@router_page_member.route("/api/user", methods=["post"])
def sign_up():
  name = request.json['name']
  email = request.json['email']
  password = request.json['password']

  checked = validated(email, password)

  if not name or not checked:
    return {"error": True, "message": "輸入格式錯誤"}, 400
  
  hashed_password = bcrypt.generate_password_hash(password=password)
  
  my_uuid = str(uuid.uuid4())

  status = User.create_user(my_uuid, name, email, hashed_password)


  if status == "exists":
    return {"error":True, "message": "此信箱已被使用"}, 400

  elif status == "created":
    return {"data": "OK"}, 200

  return {"error": True, "message": "伺服器錯誤"}, 500


# sign_in api
@router_page_member.route("/api/user/auth", methods=["put"])
def sign_in():
  email = request.json['email']
  password = request.json['password']
  reserve = request.json['reserve']

  checked = validated(email, password)

  if not checked:
    return {"error": True, "message": "輸入格式錯誤"}, 400

  user_info = User.get_user(email)
  if not user_info:
    return {"error":True, "message": "查無此帳號"}, 400

  check_password = bcrypt.check_password_hash(user_info["password"], password)
  if not check_password:
    return {"error":True, "message": "密碼錯誤"}, 400

  token = jwt_encode(user_info["uuid"], user_info["name"])
  resp = make_response({"data": "OK"}, 200)
  resp.set_cookie("token", token)

  if reserve:
    date = request.json['date']
    radio = request.json['radio']
    reserve_data = date + " " + radio
    resp.set_cookie("reserve", reserve_data)

  return resp


# auth api
@router_page_member.route("/api/user/auth")
def check_auth():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    return {"ok": True}, 200

  except:
    resp = make_response({"error": True, "message": "未登入狀態"}, 200)
    resp.set_cookie('token', '', 0)
    return resp


# sign_out api
@router_page_member.route("/api/user/auth", methods=["delete"])
def sign_out():
  resp = make_response({"ok": True}, 200)
  resp.set_cookie('token', '', 0)
  return resp



@router_page_member.route("/api/user/auth/cookie")
def get_ReserveData():
  reserve_data = request.cookies.get("reserve")
  if reserve_data:
    date = reserve_data.split(" ")[0]
    radio = reserve_data.split(" ")[1]

    resp = make_response({
      "ok": True,
      "date": date,
      "radio": radio
    }, 200)
    resp.set_cookie('reserve', '', 0)
    return resp
  return {"data": None}
