class Registry:

    def __init__(self):
        self.registry = {}

    def register_bot(self, bot):
        self.registry[bot.get_id()] = bot

    def get_bot(self, bot_id):
        return self.registry[bot_id]
