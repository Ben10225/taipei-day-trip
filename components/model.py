
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

