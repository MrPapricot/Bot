from search import Search
import telebot
from telebot.apihelper import ApiTelegramException
from telebot import types

bot = telebot.TeleBot(token='6195626191:AAHqSd1q5GQIJH_62zLUqTtBtJEkNeUNXzM')

ready = False

result = None

buttons = None


@bot.message_handler(commands=['start'])
def start(message):
    global ready
    ready = True
    bot.send_message(message.chat.id, 'Введите название фильма / сериала')


@bot.message_handler(commands=['stop'])
def stop(message):
    global ready
    global result
    ready = False
    result = None


@bot.message_handler(func=lambda message: ready)
def parse(message):
    global result
    global buttons
    kb = types.InlineKeyboardMarkup(row_width=1)
    result = Search(message.text)
    if len(result.names) == 0:
        bot.send_message(message.chat.id, 'По данному запросу ничего не найдено')
        result = None
        return
    try:
        bot.send_photo(message.chat.id, result.get_image(result.get_page_by_name(result.names[0])), result.names[0])
    except AttributeError:
        bot.send_message(message.chat.id, result.names[0])
    if len(result.names) > 1:
        for i in range(len(result.names) - 1):
            kb.add(types.InlineKeyboardButton(text=result.names[i + 1], callback_data=result.names[i + 1]))
        try:
            bot.send_message(message.chat.id, 'Другие варианты:', reply_markup=kb)
        except ApiTelegramException:
            pass


@bot.callback_query_handler(func=lambda callback: callback.data and result)
def callback_handler(callback):
    try:
        bot.send_photo(callback.message.chat.id, result.get_image(result.get_page_by_name(callback.data)),
                       callback.data)
    except AttributeError:
        bot.send_message(callback.message.chat.id, callback.data)


bot.polling()
