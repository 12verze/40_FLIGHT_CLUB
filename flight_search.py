import os
from dotenv import load_dotenv
import requests
import datetime
from pprint import pprint

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET= os.getenv("API_SECRET")

class FlightSearch:
    def __init__(self):
        self.data = None
        self.apikey = API_KEY
        self.secret = API_SECRET
        self.token = self.get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

        self.url = "https://test.api.amadeus.com/v1/reference-data/locations"

    def get_iata(self,city):
        params = {
            "keyword": city,
            "subType": "CITY"
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        error = response.status_code
        if error != 200:
            print(response.status_code)
            print("Check error")
        else:
            try:
                self.data = response.json()
                return self.data["data"][0]["iataCode"]
            except IndexError:
                return print("Please give a valid city name")

    def get_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": API_SECRET
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def cheapest_flight(self,destination_code,origin_code,price,name,date):
        cheap_price = float(price)
        message = None
        for i in range(7):  # Check for next 7 days
            tomorrow = (datetime.datetime.strptime(date, "%d/%m/%Y") + datetime.timedelta(days=i + 1)).date()
            url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
            params = {
                "originLocationCode": origin_code,
                "destinationLocationCode": destination_code,
                "departureDate": str(tomorrow),
                "adults": 1,
                "currencyCode": "INR"
            }
            response = requests.get(url, headers=self.headers, params=params)

            try:
                response.raise_for_status()
                flight_data = response.json().get("data", [])

                if not flight_data:
                    continue

                flight = flight_data[0]
                total_price = float(flight["price"]["total"])

                if total_price < cheap_price:
                    cheap_price = total_price
                    segment = flight["itineraries"][0]["segments"][0]

                    departure_iata = segment["departure"]["iataCode"]
                    arrival_iata = segment["arrival"]["iataCode"]
                    carrier = segment["carrierCode"]
                    departure_date = segment["departure"]["at"].split("T")[0]
                    departure_time = segment["departure"]["at"].split("T")[1]

                    return_date = (
                        flight["itineraries"][1]["segments"][0]["arrival"]["at"].split("T")[0]
                        if len(flight["itineraries"]) > 1 else "N/A"
                    )

                    message = (
                        f"Hey {name}, thank you for reaching out to Flight Club. We hope for a safe (*terrible) journey ;p\n\n"
                        f"🛫 Cheapest flight in the next few days:\n"
                        f"✈️ {departure_iata} to {arrival_iata} by {carrier}\n"
                        f"📅 From: {departure_date} - {return_date}\n"
                        f"🕒 Departure: {departure_time}\n"
                        f"💰 Price: ₹{total_price}\n\n"
                        f"May god keep you broke ass forever ❤️, so you won't hesitate to reach out to us again. - Visu🪽 (Founder - Flight Club)"
                    )

            except requests.exceptions.HTTPError as e:
                print(f"Error for date {tomorrow}: {e}")
                continue

        return message
