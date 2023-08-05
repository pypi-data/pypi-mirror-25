import json
import boto3

lambda_client = boto3.client('lambda')

class Bot:

    def __init__(self, bot_id):
        self.bot_id = bot_id

    def get_id(self):
        return self.bot_id

    def handle_get(self, event):
        pass

    def handle_post(self, event, processor):
        pass

    def send_for_processing(self, message, processor):
        lambda_client.invoke(
            FunctionName=processor,
            InvocationType='Event',
            Payload=json.dumps(
                {
                    'bot': self.to_json(),
                    'message': message.to_json()
                }
            )
        )

    def handle_process(self, event):
        self.process(event['message'])

    def process(self, message_json):
        pass

    def send_reply(self, message):
        pass

    def to_json(self):
        return {
            'bot_id': self.bot_id
        }

class Message:

    def __init__(self, source, target, content):
        self.source = source
        self.target = target
        self.content = content

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_content(self):
        return self.content

    @staticmethod
    def from_json(message_json):
        return Message(message_json['source'], message_json['target'], message_json['content'])

    def to_json(self):
        return {
            'source': self.source,
            'target': self.target,
            'content': self.content
        }