import tkinter
import re
import configparser
import requests
import webbrowser
import subprocess
import socket
import getpass
import distro
import psutil
import platform
import keyboard
import time

from bs4 import BeautifulSoup

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

CHOOSING, CREATE_PROJECT, LOG_WORK, CREATE_PLANNER, CREATE_VACATION = range(5)

reply_keyboard = [
    ["Create Project", "Log Time"],
    ["Submit Vacation", "Create Planner Task"],
    ["Done"],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def command_info():
    text = "Command list:\n/pma or /bb to start talking with BB\n"
    text += "/project Project_Name to create project with name is: Project"


def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! My name is BB. I will help you working with PMA",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    update.message.reply_text(
        f"Your {text.lower()}? Yes, I would love to hear about that!"
    )

    return TYPING_REPLY


def custom_choice(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me: You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    update.message.reply_text(
        f"Bye Bye!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def startSession():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # ['Create Project', 'Log Time'],
            # ['Submit Vacation', 'Create Planner Task'],
            # ['Done'],
            CHOOSING: [
                MessageHandler(Filters.regex("^Create Project$"), createProject),
                MessageHandler(Filters.regex("^Log Time$"), logWork),
                MessageHandler(Filters.regex("^Create Planner Task$"), newTask),
                MessageHandler(Filters.regex("^Submit Vacation$"), custom_choice),
            ],
            # TYPING_CHOICE: [
            #     MessageHandler(
            #         Filters.text & ~(Filters.command | Filters.regex('^Done$')),
            #         regular_choice
            #     )
            # ],
            # TYPING_REPLY: [
            #     MessageHandler(
            #         Filters.text & ~(Filters.command | Filters.regex('^Done$')),
            #         received_information,
            #     )
            # ],
            CREATE_PROJECT: [MessageHandler(Filters.text, processingCreateProject)],
        },
        fallbacks=[MessageHandler(Filters.regex("^Done$"), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    # stop the conversation if timeout 10mins
    time.sleep(600)
    ConversationHandler.END


# def inputUserId(update: Update, context: CallbackContext)
#     text = update.message.text
#     context.user_data['user-id'] = text


def createProject(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please input projects name. Project Name must not contains * \n"
        "You can insert multiple project by enter the Project Name in a new line"
    )
    return CREATE_PROJECT


def processingCreateProject(update: Update, context: CallbackContext):
    global pmarUrl, pmaRequestVerificationToken
    replied = "Processing Creating Project..."
    requests.get(
        url1 + "sendMessage",
        params=dict(chat_id=update["message"]["chat"]["id"], text=replied),
    )

    projects = update.message.text

    createProjectsHelper(projects)

    # done process
    update.message.reply_text(
        "Creating Project successfully",
        reply_markup=markup,
    )
    return CHOOSING


def createProjectsHelper(projects):
    if "*" in projects:
        update.message.reply_text("The input text contains *. Please input again!")
        return CREATE_PROJECT

    projectsArr = projects.splitlines()

    projectsArr = [p for p in projectsArr if p]

    # generate request text, refer to examples.js file
    webbrowser.open(f"{pmaUrl}/project/submitportal")
    time.sleep(7)
    keyboard.send("ctrl+shift+j")

    projectsText = ""
    for project in projectsArr[:-1]:
        projectsText += f"'{project}',"
    projectsText += f"'{project}'"

    requestText = f"let arrayOfProjects = [{projectsText}];"
    requestText += "for (const project of arrayOfProjects) {"
    requestText += "await $.post("
    requestText += f"'{pmaUrl}/project/submitportal'," + "{"
    requestText += "__RequestVerificationToken: " + f"'{pmaRequestVerificationToken}',"
    requestText += "IsAutoGenerateProjectNo: true,"
    requestText += "IsShowListPrefix: true,"
    requestText += "PrefixName: 'PMA',"
    requestText += "ProjectName: project,"
    requestText += "ScopeId: 12,"
    requestText += "ServiceTypeId: 'b4d8200c-5566-498b-8d03-a8a70097cd67',"
    requestText += "BranchId: '3d4e34b9-6ace-49dc-a96e-a7eb0071e9f5',"
    requestText += "PriorityId: 'ff688692-5ded-4ca9-83cc-779ebef210b9',"
    requestText += "IsRequestor: true,"
    requestText += "RequestedBy: 862,"
    requestText += "Coordinator: 862,"
    requestText += "TaskDescription: '<div><br></div>'"
    requestText += "});"
    requestText += "}"

    time.sleep(3)
    keyboard.write(requestText)
    time.sleep(1)
    keyboard.send("enter")


def logWork(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please input project No, date, hours on one line. separate by space. (not supported yet: multiple value can be input by multi line) \n"
        "For example:\n"
        "PMA-1 Dec/20/2021 4.5"
    )
    return LOG_WORK


def processingLogWork(update: Update, context: CallbackContext):
    replied = "Processing Log Work..."
    requests.get(
        url1 + "sendMessage",
        params=dict(chat_id=update["message"]["chat"]["id"], text=replied),
    )


def newVacation(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please input date, type of vacation ,hours on one line. separate by space. multiple value can be input by multi line\n "
        "For example:\n"
        "Dec/20/2021 annual 4.5\n"
        "Dec/21/2021 annual 0.5"
    )
    return CREATE_VACATION


def processingNewVacation(update: Update, context: CallbackContext):
    replied = "Processing New Vacation..."
    requests.get(
        url1 + "sendMessage",
        params=dict(chat_id=update["message"]["chat"]["id"], text=replied),
    )


def newTask(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please input project No, date, hours on one line. separate by space. (not supported yet: multiple value can be input by multi line) \n"
        "For example:\n"
        "PMA-1 Dec/20/2021 4.5"
    )
    return CREATE_PLANNER


def main():
    global url1, url, last_update, token, lang, owner
    req = requests.get(url).json()

    for update in req["result"]:
        if last_update < update["update_id"]:
            last_update = update["update_id"]
            if update["message"]["from"]["username"] == owner:
                if update["message"]["text"].startswith("/project"):
                    projectName = update["message"]["text"].replace("/project ", "")
                    if len(projectName) > 1:
                        createProjectsHelper(projectName)
                    else:
                        requests.get(
                            url1 + "sendMessage",
                            params=dict(
                                chat_id=update["message"]["chat"]["id"],
                                text="Please input Project Name!!\n\n" + command_info(),
                            ),
                        )
                elif (
                    update["message"]["text"] == "hi"
                    or "halo"
                    or "Halo"
                    or "Hi"
                    or "/start"
                    or "/pma"
                ):
                    startSession()
                else:
                    requests.get(
                        url1 + "sendMessage",
                        params=dict(
                            chat_id=update["message"]["chat"]["id"], text=command_info()
                        ),
                    )
                    pass

    root.after(2, main)


config = configparser.ConfigParser()
config.sections()
config.read("config.ini")
pmaUrl = config["SETTINGS"]["pma_url"]
pmaRequestVerificationToken = config["SETTINGS"]["verify_token"]
token = config["SETTINGS"]["tele_token"]
lang = config["SETTINGS"]["language"]
owner = config["SETTINGS"]["owner_username"]
last_update = 0
root = tkinter.Tk()
root.title("Running")
root.geometry("500x100")

teks = """
Bot is Running
You can type "/start" or "hi" to the Bot to get your command list

note: Don't close this window if you want to use your bot!
"""

label = tkinter.Label(root, text=teks)
label.pack()
url1 = "https://api.telegram.org/bot" + token + "/"
url = url1 + "getUpdates"
reqlast = requests.get(url).json()
try:
    last_update = reqlast["result"][-1]["update_id"]
except:
    pass
root.after(2, main)
root.mainloop()
