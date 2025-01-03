import telebot
import requests
import json

bot = telebot.TeleBot('7974007930:AAFyfHTvO1z0hAkIFQQy1DNH4zk0VSZFJIA')
API = '89dd9d2e62822a8be1c4180a29a6c95b'

@bot.message_handler(content_types=['text'])
def get_weather(message):
    print("начинаем")
    city = "Almaty"
    try:
        # Увеличиваем тайм-аут для requests
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&limit=5&appid={API}&lang=ru&units=metric",
            timeout=15  # Тайм-аут увеличен до 15 секунд
        )
        if res.status_code == 200:
            data = json.loads(res.text)
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            humidity = data["main"]["humidity"]

            response_message = (
                f"Температура: {temp}°C\n"
                f"Описание: {description}\n"
                f"Скорость ветра: {wind_speed} м/с\n"
                f"Влажность: {humidity}%"
            )
            bot.reply_to(message, response_message)

            image = 'sunny.png' if temp > 5.0 else 'sun.png'
            try:
                with open('./' + image, 'rb') as file:
                    bot.send_photo(message.chat.id, file)
            except FileNotFoundError:
                bot.reply_to(message, "Изображение не найдено.")
        else:
            bot.reply_to(message, f'Город указан неверно.')
    except requests.exceptions.ReadTimeout:
        bot.reply_to(message, "Сервер не отвечает. Попробуйте позже.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

bot.polling(none_stop=True, timeout=60, long_polling_timeout=30)
