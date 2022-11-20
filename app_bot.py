import telebot
from extensions import CryptoConvertor, ConvertionException
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help', ])
def start(message: telebot.types.Message):
    text = "Вас приветствует бот - конвертер валют! \n " \
           "Чтобы начать работу введите команду боту в формате:\n " \
           "<имя валюты> <в какую валюту перевести> <количество переводимой валюты> \n" \
           "список доступных валют: /values"
    bot.send_message(message.chat.id, f" Здравтвуйте {message.chat.username},\n {text}")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')

        quote, base, amount = values
        total_base = CryptoConvertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()