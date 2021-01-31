import datetime
import json
import requests
from urllib.parse import quote
from ..helpers import CollectionAppointment


DESCRIPTION = "Source for PGH.ST services for the city of Pittsburgh, PA, USA."
URL = "http://www.pgh.st"
TEST_CASES = {}


class Source:
    def __init__(self, house_number, street_name, zipcode):
        self._house_number = house_number
        self._street_name = quote(street_name)
        self._zipcode = zipcode

    def fetch(self):
        # get json file
        r = requests.get(
            f"http://pgh.st/locate/{self._house_number}/{self._street_name}/{self._zipcode}"
        )

        # extract data from json
        data = json.loads(r.text)

        # create entries for trash, recycling, and yard waste
        entries = [
            CollectionAppointment(
                date=datetime.datetime.strptime(data[0]['next_pickup_date'], '%m-%d-%Y').date(),
                t="Trash",
                icon="mdi:trash-can"),
            CollectionAppointment(
                date=datetime.datetime.strptime(data[0]['next_recycling_date'], '%m-%d-%Y').date(),
                t="Recycling",
                icon="mdi:recycle"),
            CollectionAppointment(
                date=datetime.datetime.strptime(data[0]['next_yard_date'], '%m-%d-%Y').date(),
                t="Yard Waste",
                icon="mdi:leaf"),
        ]

        return entries
