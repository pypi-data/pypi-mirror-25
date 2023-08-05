from ..lib.bots.messenger_bot import MessengerBot

class EchoBot(MessengerBot):

    def handle_text(self, text):
        return 'Echo: ' + text
