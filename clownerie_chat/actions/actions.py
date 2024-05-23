from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime
import json
import os
import random
import string
import time

class ActionSaveBookingToJson(Action):
    def name(self) -> Text:
        return "action_save_booking_to_json"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        json_file = "reservation_data.json"

        dispatcher.utter_message(text="Checking if we have a table for you...")
        date = tracker.get_slot('slot_date')
        people = tracker.get_slot('slot_people')
        maxLimit = 10

        available = self.check_for_availability(date, int(people), maxLimit)

        if available:
            dispatcher.utter_message(text="Yes, we have a table available for you !")
        else:
            dispatcher.utter_message(text="Sorry, we don't have a table available for that date and time.")
            return []

        def generate_uid():
            return ''.join(random.choices(string.digits, k=6))

        if os.path.exists(json_file) and os.stat(json_file).st_size != 0:
            with open(json_file, 'r', encoding="utf-8") as booking_data:
                reservations = json.load(booking_data)
                if not isinstance(reservations, list):
                    reservations = []
        else:
            reservations = []

        name = tracker.get_slot("slot_name")
        phone = tracker.get_slot("slot_phone")

        new_reservation_data = {
            "id": generate_uid(),
            "sender_id": tracker.sender_id,
            "date": date,
            "name": name,
            "people": people,
            "phone": phone,
            "comment": "",
            "created_at": time.time()
        }

        print(new_reservation_data)

        reservations.append(new_reservation_data)

        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(reservations, file, indent=4)

        recap_time = datetime.datetime.fromtimestamp(new_reservation_data['created_at'])

        recap_message = (
            f"Here is your reservation recap :"
            f"- Reservation ID: {new_reservation_data['id']}"
            f"- Date: {new_reservation_data['date']}"
            f"- Name: {new_reservation_data['name']}"
            f"- Number of Guests: {new_reservation_data['people']}"
            f"- Phone: {new_reservation_data['phone']}"
            f"- Booked at: {recap_time.strftime('%d-%m-%Y %H:%M')}"
        )

        dispatcher.utter_message(text="Your reservation has been saved.")
        dispatcher.utter_message(text=recap_message)

        return []

    def check_for_availability(self, date: str, people: int, maxLimit: int) -> bool:
        json_file = "reservation_data.json"
        allPeople = 0
        with open(json_file, 'r', encoding="utf-8") as booking_data:
            reservations = json.load(booking_data)
            for booking in reservations:
                if booking['date'] == date:
                    allPeople += int(booking['people'])

        if allPeople + people > maxLimit:
            return False
        else:
            return True

class ActionAddComment(Action):
    def name(self) -> Text:
        return "action_add_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        json_file = "reservation_data.json"
        comment = tracker.get_slot('slot_comment')
        reservation_id = tracker.get_slot('slot_comment_reservation_id')
        booking_found = False
        with open(json_file, 'r', encoding="utf-8") as booking_data:
            reservations = json.load(booking_data)
            for booking in reservations:
                if booking['id'] == reservation_id:
                    booking['comment'] = comment
                    booking_found = True

        if booking_found:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=4)
                dispatcher.utter_message(text=f"Comment added to booking {reservation_id} : {comment}")
        else:
            dispatcher.utter_message(text="No booking found with this ID")
        return []

class ActionDeleteBooking(Action):
    def name(self) -> Text:
        return "action_delete_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        json_file = "reservation_data.json"
        reservation_id = tracker.get_slot('slot_cancel_reservation_id')
        booking_found = False
        with open(json_file, 'r', encoding="utf-8") as booking_data:
            reservations = json.load(booking_data)
            for booking in reservations:
                if booking['id'] == reservation_id:
                    reservations.remove(booking)
                    booking_found = True

        if booking_found:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=4)
                dispatcher.utter_message(text="Your reservation has been successfully cancelled.")
        else:
            dispatcher.utter_message(text="No booking found with this ID")
        return []

class ActionShowBookingInfos(Action):
    def name(self) -> Text:
        return "action_show_booking_infos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        json_file = "reservation_data.json"
        reservation_id = tracker.get_slot('slot_info_reservation_id')
        booking_found = False
        new_reservation_data = {}
        with open(json_file, 'r', encoding="utf-8") as booking_data:
            reservations = json.load(booking_data)
            for booking in reservations:
                if booking['id'] == reservation_id:
                    reservation_data = {
                        "id": booking['id'],
                        "sender_id": booking['sender_id'],
                        "date": booking['date'],
                        "name": booking['name'],
                        "people": booking['people'],
                        "phone": booking['phone'],
                        "comment": booking['comment'],
                        "created_at": booking['created_at']
                    }
                    booking_found = True

        if booking_found:
            recap_time = datetime.datetime.fromtimestamp(reservation_data['created_at'])
            recap_message = (
                f"Here is your reservation infos :"
                f"- Reservation ID: {reservation_data['id']}"
                f"- Date: {reservation_data['date']}"
                f"- Name: {reservation_data['name']}"
                f"- Number of Guests: {reservation_data['people']}"
                f"- Phone: {reservation_data['phone']}"
                f"- Booked at: {recap_time.strftime('%d-%m-%Y %H:%M')}"
            )
            dispatcher.utter_message(text=recap_message)
        else:
            dispatcher.utter_message(text="No booking found with this ID")
        return []