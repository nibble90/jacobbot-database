#! /home/ubuntu/python/jacobbot/bin/python3
import sys, os
sys.path.insert(0, os.path.dirname("/home/ubuntu/python/jacobbot/seasonal/"))
from christmas import Christmas
import logging, threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat
from invoke import task

logging.basicConfig(filename='log.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater('', use_context=True)
class Commands:
    """
    Class to call for the /help command
    Args:
    update: update from telegram
    context: context of the update from telegram
    """
    def __init__(self, update, context):
        self.update = update
        self.context = context
        self.is_gc = None

    @staticmethod
    def normal_commands():
        """
        Gets normal, user commands from file and returns them
        Returns:
        normal_commands: the commands in a text format
        """
        with open('normal_commands.txt', 'r') as file: commands = file.read().strip('\n')
        return commands

    @staticmethod
    def admin_commands():
        """
        Gets admin, commands from file and returns them, users must be stated in the authorised_user.txt file
        Returns:
        admin_commands: the commands in a text format
        """
        with open('admin_commands.txt', 'r') as file: commands = file.read().strip('\n')
        return commands

    def commands_help(self):
        """
        Returns the commands to the user in a message
        Args:
        self: all variables set out in __init__
        Returns:
        The output of the other commands in this class in a message format
        """
        with open('authorised_users.txt', 'r') as file: verified = list(map(int,file.read().strip('\n').split(',')))
        if(self.update.effective_user.id in verified):
            normal = self.normal_commands()
            admin = self.admin_commands()
            self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                text="COMMANDS:\n{}\n \nADMIN COMMANDS\n{}".format(normal, admin))
        else:
            self.normal_commands()
            self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                text="""
                COMMANDS:
                {}""".format(normal))

    def is_group_chat(self):
        """

        """
        type = self.update.effective_chat.type
        if(type == 'private'):
            self.is_gc = False
        elif(type == 'group'):
            self.is_gc = True
        elif(type == 'supergroup'):
            self.is_gc = False
        else:
            logger.warning("Cannot establish group type {}".format(type))
       # print(self.update.effective_chat.type)

    def main(self):
        self.is_group_chat()
        if(self.is_gc):
            self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                text="Sorry {}, this must be done in a private chat".format(self.update.message.from_user.first_name))
# send link as the text above, make the link in the format t.me/your_bot?start=XXXX
# use pass_args in command handler to pass args into start so that /help is ran
# grab args in callbackcontext, they're as a string
        else:
            self.commands_help()

def read_uuids(filename):
    final = []
    with open(filename, "r") as file:
        contents = file.read().split(',')
        for i in range(len(contents)):
            if(contents[i] == "\n" or contents[i] == ""):
                contents.pop(i)
            else:
                final.insert(i, contents[i].strip('\n'))
    return list(map(int, final))

def shutdown_bot():
    updater.stop()
    updater.is_idle = False

def start(update, context):
    """
    Function for the /start command
    Args:
    update: update from telegram
    context: context of the update from telegram
    Return:
    Returns a nice welcome message to the user
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!")

def hello(update, context):
    """
    Function for the /hello command
    Args:
    update: update from telegram
    context: context of the update from telegram
    Return:
    Returns a nice hello message to the user
    """
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))
#    Commands(update, context).is_group_chat()

def deactivate(update, context):
    """
    Function for the /deactivate command
    Args:
    update: update from telegram
    context: context of the update from telegram
    Return:
    Shuts down server providing the user is in the authorised_user.txt list
    """
    #user_information = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It's been fun, goodbye")
    logger.critical('Shutdown initiated by {}:{}:{}'.format(update.message.from_user.first_name, update.message.from_user.last_name, update.effective_user.id))
    threading.Thread(target=shutdown_bot).start()

def unknown(update, context):
    """
    Function for the unknown command handler
    Args:
    update: update from telegram
    context: context of the update from telegram
    Return:
    Returns a a sorry message
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.")

def error_handle(update, context):
    """
    Function for the error handler
    Args:
    update: update from telegram
    context: context of the update from telegram
    Return:
    Returns an error message in the log file
    """
    logger.warning('Update "{}" caused error "{}"'.format(update, context.error))
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, there was an error processing that command.")

def help(update, context):
    """
    Function for the /help command
    Args:
    update: update from telegram
    context: context of the update from telegram
    """
    Commands(update, context).main()

def christmas(update, context):
    """
lemons
    """
    chat_id = update.effective_chat.id
    codes = read_uuids('christmas_chats.txt')
    if(chat_id in codes):
        Christmas(chat_id, context).countdown()
    else:
        with open('christmas_chats.txt', 'a+') as file: file.write(f"{chat_id},")
        Christmas(chat_id, context).countdown()


verified = read_uuids('authorised_users.txt')
updater.dispatcher.add_error_handler(error_handle)
updater.dispatcher.add_handler(CommandHandler('start', start)) #add the /start command
updater.dispatcher.add_handler(CommandHandler('hello', hello)) #add the /hello command
updater.dispatcher.add_handler(CommandHandler('deactivate', deactivate, Filters.user(user_id=verified))) #add the deactivate command and restrict it to users in authorised_users.txt only
updater.dispatcher.add_handler(CommandHandler('help', help)) #add the /help command
updater.dispatcher.add_handler(CommandHandler('christmas', christmas)) #christmas command
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) #trigger the unknown function if a command is not recognised

updater.start_polling() #gets updates from telegram
updater.idle() #waits for a stop signal
