from balebot.models.messages.text_message import TextMessage
import re
from balebot.filters.filter import Filter


class TextFilter(Filter):
    def __init__(self, keywords=None, pattern=None):
        self.keywords = []
        if isinstance(keywords, list):
            self.keywords += keywords
        elif isinstance(keywords, str):
            self.keywords.append(keywords)

        self.pattern = pattern

    def match(self, message):
        if isinstance(message, TextMessage):

            if not self.pattern and not self.keywords:
                return True

            text = message.text
            if self.find_keywords(text):
                return True
            elif self.find_pattern(text):
                return True
        else:
            return False

    def find_keywords(self, text):
        for keyword in self.keywords:
            if text.find(keyword) != -1:
                return True
        return False

    def find_pattern(self, text):
        return re.search(self.pattern, text)
