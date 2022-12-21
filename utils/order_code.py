import time

def generate_order_code():
  code = str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))+str(time.time()).replace(".", "")[-7:])
  return code
