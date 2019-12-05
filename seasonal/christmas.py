class Christmas:
    def __init__(self, user_id, context):
        self.uuid = user_id
        self.context = context
    def countdown(self):
        self.context.bot.send_message(chat_id=self.uuid,
                                      text="Return countdown here")
