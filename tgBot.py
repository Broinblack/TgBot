import requests as rq

def get_weather(city):
    try:
        API_KEY = "2b6c16d35cfbe2c3eb3e82254737f4a3"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}&lang=ru"
        answer = rq.get(url).json()
        weather_data_def = {
            "погода" : answer["weather"][0]["main"],
            "Описание" : answer["weather"][0]["description"],
            "Температура" : answer["main"]["temp"],
            "мин" : answer["main"]["temp_min"],
            "макс" : answer["main"]["temp_max"],
            "ощущается" : answer["main"]["feels_like"]
        }
        return weather_data_def
    except:
        print(f"Ошибка при запросе погоды {Exception}")
        return None


weather_data_main = {}
city = input("Введите город в котором хотите узнать погоду: ")
weather_data_main = get_weather(city)

print(f"""Город: {city}\nПогода: {weather_data_main['погода']}, {weather_data_main['Описание']}\nТемпература: \
      {weather_data_main['Температура']}°C\nОщущается как: {weather_data_main['ощущается']}°C""")
