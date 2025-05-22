from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TOKEN = "7527447127:AAE7HFPQvJqfPe8w_FpHUtjDVbRAT0ex4ZU"
OWM_API_KEY = "2b6c16d35cfbe2c3eb3e82254737f4a3"

def start(update: Update, context: CallbackContext):
    # Кнопки для быстрого доступа
    buttons = [['Погода в Москве'], ['Погода в СПб']]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
    update.message.reply_text(
        'Привет! Я бот погоды. Напиши название города или нажми кнопку:',
        reply_markup=reply_markup
    )

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OWM_API_KEY}&lang=ru"
    response = requests.get(url).json()
    
    if response.get('cod') != 200:
        return None
    
    weather_data = {
        'city': response['name'],
        'temp': response['main']['temp'],
        'feels_like': response['main']['feels_like'],
        'description': response['weather'][0]['description'],
        'humidity': response['main']['humidity']
    }
    return weather_data

def weather(update: Update, context: CallbackContext):
    city = update.message.text
    
    # Обработка кнопок
    if city == 'Погода в Москве':
        city = 'Moscow,ru'
    elif city == 'Погода в СПб':
        city = 'Saint Petersburg,ru'
    
    weather_info = get_weather(city)
    
    if not weather_info:
        update.message.reply_text("Город не найден. Попробуйте ещё раз!")
        return
    
    message = (
        f"Погода в {weather_info['city']}:\n"
        f"🌡 {weather_info['temp']}°C (ощущается как {weather_info['feels_like']}°C)\n"
        f"☁ {weather_info['description'].capitalize()}\n"
        f"💧 Влажность: {weather_info['humidity']}%"
    )
    
    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, weather))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()