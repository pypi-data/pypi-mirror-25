import json as json_handler

from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error

from balebot.models.constants.message_type import MessageType


class JsonMessage(BaseMessage):
    def __init__(self, raw_json):

        self.raw_json = str(raw_json)

    def get_json_object(self):

        data = {
            "$type": MessageType.json_message,
            "rawJson": self.raw_json

        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        raw_json = json_dict.get('rawJson', None)

        if raw_json is None:
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(raw_json=raw_json)
