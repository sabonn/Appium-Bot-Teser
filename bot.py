import hashlib
from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os

TOKEN: Final = "7293743920:AAEunrKnQkQD141iPVZBKBabtBtms7kN8dc"
BOT_NAME: Final = "@NnnSssOoobot"


# start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pls send .jpg/.jpeg files")
    pass


# handeling messages from user
async def got_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive(photo.file_id + ".jpg")
    hash = get_hash(photo.file_id + ".jpg")
    await update.message.reply_text(hash)


async def handeling_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.document.file_name
    type = os.path.splitext(name)[1]
    if type != ".jpeg" and type != ".jpg":
        print("ERROR: WRONG FILE! SEND JPG!")
        await update.message.reply_text("ERROR: WRONG FILE! SEND JPG!")
        return

    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive(name)

    hash = get_hash(name)
    await update.message.reply_text(hash)


# getting hash
def get_hash(path: str, hash="sha256") -> str:
    file_hash: str = ""
    with open(path, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
        file_hash = hash
    os.remove(path)
    return file_hash


# Errors
async def error_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("ERROR: SENT TEXT! SEND JPG!")
    await update.message.reply_text("ERROR: SENT TEXT! SEND JPG!")


if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.PHOTO, got_picture))
    app.add_handler(MessageHandler(filters.TEXT, error_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handeling_files))

    print("Bot Is Up&Ready!!!")

    app.run_polling(poll_interval=3)
