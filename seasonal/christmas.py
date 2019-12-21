import datetime
class Christmas:
    def __init__(self, user_id, context):
        self.uuid = user_id
        self.context = context
    def countdown(self):
        cntdwn = datetime.datetime(2019, 12, 25) - datetime.datetime.now()
        christmas_countdown = "In the GMT timezone there are {} day(s) until christmas!".format(cntdwn.days)
        self.context.bot.send_message(chat_id=self.uuid,
                                      text=christmas_countdown)
