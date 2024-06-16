# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)

# This is temporary database for CCCD
CCCD_db = {
    '123456789',
    '123456789123'
}

class ActionReplyForReceivingDifferentCertificate(Action):
    def name(self) -> Text:
        return "action_reply_for_receiving_different_certificate"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get("entities", [])
        certificate_levels = [e["value"] for e in entities if e["entity"] == "certificate_level"]

        if certificate_levels[0] > certificate_levels[1]:
            message = f"Bạn đã đề cập đến các chứng chỉ: {', '.join(certificate_levels)}"
        else:
            message = "Tôi không tìm thấy thông tin về chứng chỉ nào trong tin nhắn của bạn."

        dispatcher.utter_message(text=message)
        return []

class ActionShowExamRoom(Action):

    def name(self) -> Text:
        return "action_show_exam_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_CCCD = next(tracker.get_latest_entity_values("CCCD_number"), None)

        if not current_CCCD:
            dispatcher.utter_message(text="Xin lỗi, tôi không nhận diện được số CCCD của bạn. Bạn có thể gửi lại được không?")
            return []

        # check the current CCCD in the database
        if current_CCCD in CCCD_db:
            dispatcher.utter_message(text="Phòng thi của bạn là phòng 101")
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy thông tin của bạn trong hệ thống. Bạn có thể gửi lại được không?")

        return [SlotSet("CCCD_number", current_CCCD)]

class ActionShowExamScore(Action):

    def name(self) -> Text:
        return "action_show_exam_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_CCCD = next(tracker.get_latest_entity_values("CCCD_number"), None)

        if not current_CCCD:
            current_CCCD = tracker.get_slot("CCCD_number")
            if not current_CCCD:
                dispatcher.utter_message(text="Xin lỗi, tôi không nhận diện được số CCCD của bạn. Bạn có thể gửi lại được không?")
                return []

        # check the current CCCD in the database
        if current_CCCD in CCCD_db:
            dispatcher.utter_message(text="Điểm thi của bạn là 9.5")
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy thông tin của bạn trong hệ thống. Bạn có thể gửi lại được không?")

        return [SlotSet("CCCD_number", current_CCCD)]

class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Xin lỗi, hiện tại tôi chưa hiểu ý bạn. Bạn có thể nói lại được không?")

        return []

