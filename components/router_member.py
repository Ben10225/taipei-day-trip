
from flask import *
from flask_bcrypt import Bcrypt
from data.DBconnection import *
from components.validate import *
from components.jwt import *

bcrypt = Bcrypt()
router_page_member = Blueprint("router_page_member", __name__, template_folder="templates")


# sign_up api
@router_page_member.route("/api/user", methods=["post"])
def sign_up():
  name = request.json['name']
  email = request.json['email']
  password = request.json['password']

  hacked = not validated(email, password)

  if not name or hacked:
    return {"error": True, "message": "遭受駭客攻擊"}, 400
  
  hashed_password = bcrypt.generate_password_hash(password=password)

  status = Users.createUser(name, email, hashed_password)

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

  hacked = not validated(email, password)

  if hacked:
    return {"error": True, "message": "遭受駭客攻擊"}, 400

  user_info = Users.getUser(email)
  if not user_info:
    return {"error":True, "message": "查無此帳號"}, 400

  check_password = bcrypt.check_password_hash(user_info["password"], password)
  if not check_password:
    return {"error":True, "message": "密碼錯誤"}, 400

  token = jwt_encode(user_info["uid"], user_info["name"])
  resp = make_response({"data": "OK"}, 200)
  resp.set_cookie("token", token)
  return resp


# auth api
@router_page_member.route("/api/user/auth")
def check_auth():
  try:
    payload = jwt_verify(request.cookies.get("token"))
    return {"ok": True}, 200

  except:
    resp = make_response({"error": True, "message": "未登入狀態"})
    resp.set_cookie('token', '', 0)
    return resp


# sign_out api
@router_page_member.route("/api/user/auth", methods=["delete"])
def sign_out():
  resp = make_response({"ok": True}, 200)
  resp.set_cookie('token', '', 0)
  return resp