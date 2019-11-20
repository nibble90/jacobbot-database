import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat

logging.basicConfig(filename='log.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater('', use_context=True)
class Commands:
    """

    """
    def __init__(self, update, context):
        self.update = update
        self.context = context
    @staticmethod
    def normal_commands():
        with open('normal_commands.txt', 'r') as file: commands = file.read().strip('\n')
        return commands
    @staticmethod
    def admin_commands():
        with open('admin_commands.txt', 'r') as file: commands = file.read().strip('\n')
        return commands
    def commands_help(self):
        with open('authorised_users.txt', 'r') as file: verified = list(map(int,file.read().strip('\n').split(',')))
        if(self.update.effective_user.id in verified):
            normal = self.normal_commands()
            admin = self.admin_commands()
            self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                text="COMMANDS:\n{}\n \nADMIN COMMANDS\n{}".format(normal, admin))
        else:
            normal_commands()
            self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                text="""
                COMMANDS:
                {}""".format(normal))


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")

def hello(update, context):
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))
def deactivate(update, context):
    #user_information = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It's been fun, goodbye")
    logger.critical('Shutdown initiated by {}:{}:{}'.format(update.message.from_user.first_name, update.message.from_user.last_name, update.effective_user.id))
   # context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry {}, you must be creator not {}".format( user_information['user']['first_name'], user_information['status']))
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.")
def error_handle(update, context):
    logger.warning('Update "{}" caused error "{}"'.format(update, context.error))
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, there was an error processing that command.")
def help(update, context):
    Commands(update, context).commands_help()



with open('authorised_users.txt', 'r') as file: verified = list(map(int,file.read().strip('\n').split(',')))
updater.dispatcher.add_error_handler(error_handle)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('deactivate', deactivate, Filters.user(user_id=verified)))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
