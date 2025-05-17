import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import uuid

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="")

async def download_pdf(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    file_path = f'./files/{chat_id}_{uuid.uuid4()}.pdf'
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive(file_path)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7536106227:AAGMAq0FYlrN7Wna25ogl9UM4KrsDxbXRXo').build()

    start_handler = CommandHandler('start', start)
    file_handler = MessageHandler(filters.Document.PDF, download_pdf)
    application.add_handler(start_handler)
    application.add_handler(file_handler)
    application.run_polling()
