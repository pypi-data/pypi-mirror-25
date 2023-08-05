import json

import requests
from .bot import Bot, Message


class MessengerBot(Bot):

    def handle_get(self, event):
        if 'hub.mode' in event and event['hub.mode'] == 'subscribe' and 'hub.challenge' in event:
            if not event['hub.verify_token'] == self.params['fb_verify']:
                return 'Wrong verification token!', 401
            return event['hub.challenge'], 200
        return 'Hello!', 200

    def handle_post(self, event, processor):
        messages = MessengerBot.__read_event(event)
        sent_typing = False
        for message in messages:
            if not sent_typing:
                self.__send_typing_action(message)
                sent_typing = True
            self.send_for_processing(message, processor)
        return 'OK', 200

    @staticmethod
    def __read_event(event):
        messages = []
        for entry in event['entry']:
            for event in entry['messaging']:
                if 'message' in event and 'text' in event['message']:
                    messages.append(MessengerMessage(event['sender']['id'], event['recipient']['id'],
                                                     event['message']['text'], 'text'))
        return messages

    def __send_typing_action(self, message):
        self.__do_send(json.dumps({
            'recipient': {
                'id': message.source
            },
            'sender_action': 'typing_on'
        }))

    def process(self, message_json):
        message = MessengerMessage.from_json(message_json)
        reply = self.handle_text(message.content)
        reply_message = MessengerMessage(message.get_target(), message.get_source(), reply, message.get_content_type())
        self.send_reply(reply_message)

    def handle_text(self, text):
        pass

    def send_reply(self, message):
        self.__do_send(json.dumps({
            'recipient': {
                'id': message.target
            },
            'message': {
                'text': message.content
            }
        }))

    def __do_send(self, data):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'access_token': self.params['access_token']
        }
        r = requests.post('https://graph.facebook.com/v2.6/me/messages', params=params, headers=headers, data=data)
        if r.status_code != 200:
            raise Exception(r.text)

class MessengerMessage(Message):

    def __init__(self, source, target, content, content_type):
        super().__init__(source, target, content)
        self.content_type = content_type

    def get_content_type(self):
        return self.content_type

    @staticmethod
    def from_json(message_json):
        return MessengerMessage(message_json['source'], message_json['target'], message_json['content'],
                                message_json['content_type'])

    def to_json(self):
        message_json = Message.to_json(self)
        message_json['content_type'] = self.content_type
        return message_json
