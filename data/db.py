import json
from users import connectPool

insertAll = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng, imgs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

with open("taipei-attractions.json") as f:
  data = json.load(f)

data = data["result"]["results"]

db = connectPool("setup")
mycursor = db.cursor()

for i in range(len(data)):
  imgs = data[i]["file"].split("https")
  imgTxt = ""
  for j in range(len(imgs)):
    if j > 0:
      if(imgs[j][-3:].lower() == "png" or imgs[j][-3:].lower() == "jpg"):
        imgTxt += "https" + imgs[j] + " "
  val = (data[i]["_id"], data[i]["name"], data[i]["CAT"], data[i]["description"], data[i]["address"], data[i]["direction"], data[i]["MRT"], data[i]["latitude"], data[i]["longitude"], imgTxt)
  mycursor.execute(insertAll, val)
  db.commit()

mycursor.close()
db.close()

print("新增所有資料完成")

