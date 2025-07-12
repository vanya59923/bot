import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка конфигурации
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
ADMIN_CHAT_ID = os.environ['ADMIN_CHAT_ID']

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"👋 Привет, {user.first_name}! Я буду пересылать твои сообщения.")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Пересылаем сообщение админу
        await update.message.forward(chat_id=ADMIN_CHAT_ID)
        
        # Отправляем информацию об отправителе
        user = update.message.from_user
        user_info = (
            f"🚀 Новое сообщение:\n"
            f"👤 Имя: {user.first_name or '-'}\n"
            f"📌 Юзернейм: @{user.username or '-'}\n"
            f"🆔 ID: {user.id}"
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=user_info
        )
    except Exception as e:
        logger.error(f"Ошибка пересылки: {e}")

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    
    # Запуск бота
    logger.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()