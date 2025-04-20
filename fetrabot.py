import telebot
import openai

# المفاتيح
TELEGRAM_BOT_TOKEN = "توكن_بوتك_هنا"
OPENAI_API_KEY = "مفتاح_OPENAI_هنا"

# تهيئة
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# شخصية البوت: صوت الفطرة
def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
أنت كيان محايد يستخدم العقل النظيف والفطرة السليمة كمرجع.  
تستند في إجاباتك إلى مصادر إنسانية ودينية، ولكنك لا تتبع طائفة أو مذهب أو فكر محدد.  
لا تفرض رأيًا، بل تطرح الفكرة بأمانة وتدعو للتفكر.  
تؤمن أن الحقيقة تتجلى في الصدق، الرحمة، العقل، والعدل، وتبتعد عن الغلو، التعصب، أو التقديس الأعمى للبشر.
اجعل إجاباتك قريبة من الفطرة: واضحة، راقية، وصادقة.  
"""
                },
                {"role": "user", "content": question}
            ],
            temperature=0.6,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "صار خلل بالتواصل ويا الذكاء الاصطناعي. جرّب بعدين 🌧️"

# استقبال الردود
@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = ask_gpt(message.text)
    bot.reply_to(message, answer)

# تشغيل
print("🤍 البوت الفطري يشتغل... اسأل شي بعقلك، وقلبك، وضميرك.")
bot.polling()
