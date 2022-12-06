import re

def validated(email, password):
  validated_email = bool(re.fullmatch(r"^\S+@\S+$", email))
  validated_pwd = bool(re.fullmatch(r"^(?=.*\d)(?=.*[a-z])[0-9a-zA-Z]{2,}$", password))

  return validated_email and validated_pwd