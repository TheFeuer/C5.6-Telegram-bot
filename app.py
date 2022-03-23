import telebot
from config import keys, TOKEN
from extensions import convertException, ValuesConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите комманду в следующем формате:\n|Название валюты| \
|В какую валюту перевести| \
|Количество|\nУвидить список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise convertException('Лишние параметры.')

        quote, base, amount = values

        total_base = ValuesConverter.get_price(quote, base, amount)

    except convertException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')

    except Exception:
         bot.reply_to(message, f'Не удалось оброботать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()