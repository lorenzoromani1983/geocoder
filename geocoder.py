import os
import requests
from pycookiecheat import BrowserType, chrome_cookies

class Geocoder:
	def __init__(self, address, sessionId=None, lat=None, lon=None):
		self.google_maps_api_key = os.environ["GOOGLE_MAPS_API_KEY"]
		self.google_maps_url = "https://maps.googleapis.com/maps/api/geocode/json"
		self.lat = lat
		self.lon = lon
		self.address = address

	def geocode(self):
		params = {"address": self.address, "key": self.google_maps_api_key}
		try:
			response = requests.get(self.google_maps_url, params=params).json()
		except requests.exceptions.ConnectionError as e:
			print("Connection error:",e)
			return None
		if response["status"] == "OK":
			location = response["results"][0]["geometry"]["location"]
			self.lat = location["lat"]
			self.lon = location["lng"]
			return {"address":self.address, "lat": location["lat"], "lon": location["lng"]}
		else:
			return {"address":None, "error": response["status"], "message": response.get("error_message", "Geocoding failed")}

	def instagram_locations(self):
		if all((self.lat, self.lon)):
			instagram_geocode_url = f"https://www.instagram.com/location_search/?latitude={self.lat}+&longitude={self.lon}"
			cookies = chrome_cookies("https://instagram.com")
			try:
				response = requests.get(instagram_geocode_url, cookies=cookies).json()
			except requests.exceptions.ConnectionError as e:
				print("Connection error:",e)
				return None
			venues = response["venues"]
			locations = [{"miles_from_specified_address": float(venue["address"].split(' · ')[0].replace('mi','').replace('<','')), 
							"name": venue["name"], 
							"lat":venue["lat"], 
							"lon":venue["lng"],
							"facebook_page": "https://facebook.com/"+str(venue["external_id"])}
							if 'address' in venue 
							else None 
							for venue in venues]
			return locations 
		else:
			return {"Error": "you need to call the .geocode method first to set latitude and longitude parameters"}

address = Geocoder("Via del Corso, Rome, Italy")
coordinates = address.geocode()
locations = address.instagram_locations()

for location in locations:
	print(location)

