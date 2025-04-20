from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# إضافة التوكن الذي حصلت عليه من بوت فاثر على تلغرام
TOKEN = 'YOUR_BOT_TOKEN'

# وظيفة الرد على أمر /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا بك في بوت الفطرة!')

# وظيفة الرد على أمر /help
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('اكتب /start للبدء أو أي استفسار وسيتم الرد عليك.')

def main():
    # إنشاء المحدث (updater) مع التوكن الخاص بك
    updater = Updater(TOKEN)

    # الحصول على الموزع (dispatcher) لربط الأوامر
    dispatcher = updater.dispatcher

    # إضافة الأوامر إلى الموزع
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # بدء البوت
    updater.start_polling()

    # إبقاء البوت يعمل
    updater.idle()

if __name__ == '__main__':
    main()
