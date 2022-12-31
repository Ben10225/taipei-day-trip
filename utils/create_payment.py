from api.model import *
from utils.order_code import generate_order_code

def create_orders(order, uuid, bool):
  number = generate_order_code()
  create_p_value = [number, uuid, int(order["totalPrice"]), order["contact"]["name"], order["contact"]["email"], order["contact"]["phone"], bool]
  payment_id = Order.create_payment(create_p_value[0], create_p_value[1], create_p_value[2], create_p_value[3], create_p_value[4], create_p_value[5], bool)

  for i in range(len(order["trips"])):
    create_t_value = [payment_id, number, order["trips"][i]["attraction"]["id"], order["trips"][i]["attraction"]["name"], order["trips"][i]["attraction"]["address"], order["trips"][i]["attraction"]["image"], int(order["trips"][i]["attraction"]["price"]), order["trips"][i]["date"], order["trips"][i]["time"]]
    Order.create_trips(create_t_value[0], create_t_value[1],create_t_value[2], create_t_value[3], create_t_value[4], create_t_value[5], create_t_value[6], create_t_value[7], create_t_value[8])

  return number, payment_id