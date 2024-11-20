import telebot
from  config import Token
from logic import show
bot = telebot.TeleBot(Token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\Привет! Я бот который генерирует изображение просто пиши что хочешь увидеть.\
            """)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.chat.id
    prompt = message.text
    bot.reply_to(message, "Генерирую картинку, подожди 3 минуты")
    bot.send_chat_action(message.chat.id, 'generation')
    img = show(prompt)
    with open(img, 'rb') as photo:
        
        bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")
        


bot.infinity_polling()