import json
from users import connectPool

insertAll = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng, imgs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
insertCat = "INSERT INTO categories (category_name) VALUES (%s)"
insertMrt = "INSERT INTO mrts (mrt_name) VALUES (%s)"
insertAttrs = "INSERT INTO attractions (id, name, category_id, description, address, transport, mrt_id, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
insertImages = "INSERT INTO images (iid, url) VALUES (%s, %s)"

with open("taipei-attractions.json") as f:
  data = json.load(f)

data = data["result"]["results"]

cat = []
cat_dict = {}
cct = 0
for i in range(len(data)):
  if data[i]["CAT"] not in cat:
    cct += 1
    cat_name = data[i]["CAT"]
    cat.append(cat_name)
    cat_dict[f"{cat_name}"] = cct

mrt = []
mrt_dict = {}
mct = 0
for i in range(len(data)):
  if data[i]["MRT"] not in mrt:
    station = data[i]["MRT"]
    mct += 1
    mrt.append(station)
    mrt_dict[f"{station}"] = mct



db = connectPool("setup")
mycursor = db.cursor()


# # insert table categories
# for i in cat:
#   mycursor.execute(insertCat, (i,))
#   db.commit()


# # insert table mrts
# for i in mrt:
#   mycursor.execute(insertMrt, (i,))
#   db.commit()
    

# # insert table attractions
# for i in range(len(data)):
#   cat_s = data[i]["CAT"]
#   mrt_s = data[i]["MRT"]
#   if not mrt_s:
#     mrt_id = 20
#   else:
#     mrt_id = mrt_dict[mrt_s]
#   val = ( data[i]["_id"], data[i]["name"], cat_dict[cat_s], data[i]["description"], data[i]["address"],
#           data[i]["direction"], mrt_id, data[i]["latitude"], data[i]["longitude"])
#   mycursor.execute(insertAttrs, val)
#   db.commit()


# insert table images
for i in range(len(data)):
  imgs = data[i]["file"].split("https")
  for j in range(len(imgs)):
    if j > 0:
      if(imgs[j][-3:].lower() == "png" or imgs[j][-3:].lower() == "jpg"):
        imgs[j] = "https" + imgs[j]
        val = (data[i]["_id"], imgs[j])
        mycursor.execute(insertImages, val)
        db.commit()


# 單一資料庫做法
# for i in range(len(data)):
#   imgs = data[i]["file"].split("https")
#   imgTxt = ""
#   for j in range(len(imgs)):
#     if j > 0:
#       if(imgs[j][-3:].lower() == "png" or imgs[j][-3:].lower() == "jpg"):
#         imgTxt += "https" + imgs[j] + " "
#   val = (data[i]["_id"], data[i]["name"], data[i]["CAT"], data[i]["description"], data[i]["address"], data[i]["direction"], data[i]["MRT"], data[i]["latitude"], data[i]["longitude"], imgTxt)
#   mycursor.execute(insertAll, val)
#   db.commit()

mycursor.close()
db.close()

# print("新增所有資料完成")

