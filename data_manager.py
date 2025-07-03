import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
token = os.getenv("token")
url = os.getenv("url")

class DataManager:
    def __init__(self):
        self.url = url
        self.headers ={
            "Authorization": token
        }

    def get_data(self):
        response = requests.get(url = self.url,headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data

    def update_data(self,d_iata,o_iata,row_id):
        sheety_endpoint = f"{url}/{row_id}"
        update_data = {
            "formResponses1": {
                "destCode": d_iata,
                "originCode": o_iata
            }
        }
        response = requests.put(url=sheety_endpoint, json=update_data, headers=self.headers)
        print(response.text)

    def update_state(self,row_id):
        sheety_endpoint = f"{url}/{row_id}"
        update_data = {
            "formResponses1": {
                "mailsent": "Done"
            }
        }
        response = requests.put(url=sheety_endpoint, json=update_data, headers=self.headers)
        print(response.text)


