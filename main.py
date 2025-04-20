from flask import Flask, request
import openai
import os

app = Flask(__name__)

# إعداد مفتاح OpenAI (خلي المفتاح مالتك كمتغير بيئي أو بشكل مباشر مؤقتًا)
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key-here")

@app.route("/", methods=["GET"])
def home():
    return "FetraBot is Alive - فطرة بوت شغّال 💡"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if message:
        # إرسال السؤال لـ OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أجب بشكل متوازن، منطقي، ويفهم الفطرة. كن محايدًا بين الأديان ولا تتعصب. كن مساعدًا ذكيًا يعين الباحثين عن الحقيقة."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content

        # إرسال الرد للتليجرام
        send_telegram_message(chat_id, reply)

    return "ok"

def send_telegram_message(chat_id, text):
    import requests
    telegram_token = os.getenv("TELEGRAM_TOKEN", "your-telegram-token-here")
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
