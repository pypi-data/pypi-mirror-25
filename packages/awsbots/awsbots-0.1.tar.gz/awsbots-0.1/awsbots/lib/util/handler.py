import json

class Handler:

    def __init__(self, registry):
        self.registry = registry

    @staticmethod
    def __build_response(body, code):
        return {
            'statusCode': code,
            'headers': {'Content-Type': 'application/json; charset=utf-8'},
            'body': body
        }

    def __handle_api(self, event, context):
        bot_id = event['pathParameters']['bot_id']
        processor = context.invoked_function_arn
        bot = self.registry.get_bot(bot_id)

        if event['httpMethod'] == 'GET':
            params = event['queryStringParameters']
            resp, code = bot.handle_get(params)
            return resp, code
        elif event['httpMethod'] == 'POST':
            params = json.loads(event['body'])
            resp, code = bot.handle_post(params, processor)
            return json.dumps(resp), code
        else:
            return 'Wrong method', 400

    def __handle_process(self, event):
        bot_id = event['bot']['bot_id']
        bot = self.registry.get_bot(bot_id)
        bot.handle_process(event)
        return 'OK', 200

    def handle(self, event, context):
        if 'bot' in event:
            body, code = self.__handle_process(event)
        else:
            body, code = self.__handle_api(event, context)
        return Handler.__build_response(body, code)
