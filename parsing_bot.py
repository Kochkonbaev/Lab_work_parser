from parsing_2 import KinavoBot
import telebot
import parsing
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
kbot = KinavoBot()

@bot.message_handler(commands=['start', 'help'])
def start_and_help(message):
    bot.send_message(message.chat.id, kbot.help_text)


@bot.message_handler(commands=['categories'])
def categories(message):
    bot.send_message(message.chat.id, str(kbot.categoriesset))

@bot.message_handler(commands=['categories_name'])
def categories_from_kino_1(message):
    msg = bot.send_message(message.chat.id, 'Введите название категории:')
    bot.register_next_step_handler(msg, categories_from_kino_2)

def categories_from_kino_2(message):
    r = str(kbot.category_from_kinavo(message.text))
    if len(r) > 4096:
        for x in range(0, len(r), 4096):
            bot.send_message(message.chat.id, '{}'.format(r[x:x + 4096]))         
    else:
        bot.send_message(message.chat.id, '{}'.format(r))


@bot.message_handler(commands=['product'])
def product_1(message):
    msg = bot.send_message(message.chat.id, 'Введите название товара:')
    bot.register_next_step_handler(msg, product_2)

def product_2(message):
    r = str(kbot.product_from_kinavo(message.text))
    if len(r) > 4096:
        for x in range(0, len(r), 4096):
            bot.send_message(message.chat.id, '{}'.format(r[x:x + 4096]))    
    else:
        bot.send_message(message.chat.id, '{}'.format(r))


if __name__ == '__main__':
    bot.polling(none_stop=True)