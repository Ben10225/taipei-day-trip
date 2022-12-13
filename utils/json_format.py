
def attraction_details(item):
	images = item["urls"].split(",")
	details = {
		"id": item["id"],
		"name": item["name"],
		"category": item["category_name"],
		"description": item["description"],
		"address": item["address"].replace(" ",""),
		"transport": item["transport"],
		"mrt": item["mrt_name"],
		"lat": item["lat"],
		"lng": item["lng"],
		"images": images
	}
	return details

def booking_details(booking):
	details = {
		"attraction": {
			"id": booking["attraction_id"],
			"name": booking["name"],
			"address": booking["address"],
			"image": booking["url"]
		},
		"date": booking["date"],
		"time": booking["time"],
		"price": booking["price"],
		"bid": booking["bid"]
	}
	return details
