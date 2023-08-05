from ..lib.bots.messenger_bot import MessengerBot

class EchoBot(MessengerBot):

    def handle_text(self, text):
        return 'You sent text'

    def handle_media(self, attachments):
        return 'You sent media'

    def handle_link(self, links):
        return 'You sent a link'
