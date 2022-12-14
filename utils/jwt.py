import jwt
import time

def jwt_encode(uuid, name):
  payload = {
    "iss": "ben.127",
    "exp": int(time.time() + 86400 * 7), # 設定 JWT 被視為無效的時間
    "aud": "www.ben.127", 
		"sub": uuid, 
    "name": name,
  }
  token = jwt.encode(payload, "secret", algorithm="HS256")
  return token

def jwt_verify(token):
  payload = jwt.decode(token, "secret", audience="www.ben.127", algorithms="HS256")
  if payload:
    return payload
  return None