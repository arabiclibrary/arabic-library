import json
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# تفعيل API Key الخاصة بـ OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"

# تفعيل توكن تليجرام
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
updater = Updater(TELEGRAM_TOKEN, use_context=True)

# تحميل المبادئ الفطرية من ملف JSON
def load_principles():
    with open('principles.json', 'r', encoding='utf-8') as file:
        return json.load(file)['principles']

# إرسال الردود بناءً على المبادئ
def get_fetrabot_response(user_message, principles):
    # دمج المبادئ الفطرية مع الرسالة
    prompt = "\n".join(principles) + "\nUser Message: " + user_message + "\nFetrabot's response:"
    
    # إرسال الـ prompt إلى OpenAI ليكون فطريًا
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# دالة للرد على الرسائل في التليجرام
def handle_message(update, context):
    user_message = update.message.text
    principles = load_principles()
    
    # الحصول على الرد الفطري من Fetrabot
    response = get_fetrabot_response(user_message, principles)
    
    # إرسال الرد إلى المستخدم
    update.message.reply_text(response)

# إضافة معالج للرسائل النصية
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# بدء البوت
updater.start_polling()
updater.idle()
