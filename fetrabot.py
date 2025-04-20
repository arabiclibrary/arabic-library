import json
import random
import os

# تحميل المبادئ الفطرية من ملف principles.json
def load_principles():
    with open('principles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# تحميل المحادثات السابقة من ملف memory.json
def load_memory():
    if os.path.exists('memory.json'):
        with open('memory.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

# حفظ المحادثات في ملف memory.json
def save_memory(memory):
    with open('memory.json', 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

# تحسين الردود بناءً على المحادثات السابقة
def improve_response(user_input, memory):
    response = "أفهم ما تقول، سأتعلم وأحسن إجابتي في المستقبل."
    
    if user_input.lower() in memory:
        response = random.choice(memory[user_input.lower()])
    
    return response

# إضافة المحادثة إلى الذاكرة
def add_to_memory(user_input, bot_response, memory):
    if user_input.lower() not in memory:
        memory[user_input.lower()] = []
    memory[user_input.lower()].append(bot_response)

def run_bot():
    principles = load_principles()
    memory = load_memory()
    
    print("مرحبًا! أنا بوت فطري. كيف يمكنني مساعدتك اليوم؟")
    
    while True:
        user_input = input("أنت: ")
        if user_input.lower() == 'خروج':
            print("إلى اللقاء!")
            break
        
        bot_response = improve_response(user_input, memory)
        print(f"البوت: {bot_response}")
        
        add_to_memory(user_input, bot_response, memory)
        save_memory(memory)

if __name__ == "__main__":
    run_bot()
