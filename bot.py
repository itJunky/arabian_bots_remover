import telebot
from config import token


bot = telebot.TeleBot(token)
#TODO удалять юзеров с никами из арабских символов


#TODO удалять юзера, приглашающего юзеров с арабскими никами
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def check_join_messages(msg):
    print(clr.Yellow + msg.chat.title + clr.END)
    # print('{} {} {}'.format(msg.new_chat_member.username, msg.new_chat_member.first_name))
    res = detect_and_ban_bots(msg)
    print(clr.Red + "Result: " + str(res) + clr.END)


#TODO дописать бан за форварды
@bot.message_handler(func=lambda msg: msg.forward_from_chat, content_types=["text", "photo", "video", "document"])
#@bot.message_handler(content_types=["text", "photo", "video", "document"])
def posts_from_channels(msg):
    print(clr.Yellow + msg.chat.title + clr.END)
    print(msg)
    res = detect_and_ban_bots(msg)
    print(clr.Red + "Result: " + str(res) + clr.END)
    print(clr.Blue + str(msg.forward_from_chat) + clr.END)


# удалять сообщения содержащие арабские символы
@bot.message_handler(func=lambda m: True)  # get all messages
def check_messages(msg):
    print(clr.Yellow + msg.chat.title + clr.END)
    print(msg.text)
    # print(msg)
    if check_symbols(msg.text):
        try_to_ban(msg)


###########################################
def try_to_ban(msg):
    try:
        print(msg.text)
        bot.delete_message(msg.chat.id, msg.message_id)
        print('Message {} deleted'.format(msg.message_id))
        bot.kick_chat_member(msg.chat.id, msg.from_user.id)
        print('Ban user id {} - {}'.format(msg.from_user.id, msg.from_user.first_name))
    except Exception as e:
        print(e)
        bot.send_message(msg.chat.id, 'Can\'t remove message because I\'m doesn\'t have administration privileges.')


def detect_and_ban_bots(msg):
    # Проверяем кто добавил, если админ, ничего не делать
    if bot.get_chat_member(msg.chat.id, msg.from_user.id).status in ['creator', 'administrator']:
        return False

    try:
        # Если добавил обычный юзер, проверять имя на арабские символы и бот или не бот
        if check_symbols(msg.new_chat_member.first_name) or \
           check_symbols(msg.new_chat_member.last_name) or \
           it_is_bot(msg) :
            print('ITS SPAMBOT')
            #TODO удалять бота и его сообщения
            remove_bots(msg)
            return True
    except Exception as e:
        print("Error")
        return False

    return False

def check_symbols(text):
    res = False
    dbg = []
    if text is not None:
        for char in text:
            dbg.append(ord(char))
            if ord(char) > 1500 and ord(char) < 1800:
                res = True
                # return True

    print(clr.Grey + str(dbg) + clr.END)
    return res
    # return False


def it_is_bot(msg):
    for user in msg.new_chat_members:
        print(user)


def remove_bots(msg):
    last_msg_id = 0
    # remove user
    try:
        bot.kick_chat_member(msg.chat.id, msg.from_user.id)
    except Exception as e:
        print(e)

    # remove bots
    for user in msg.new_chat_members:
        try:
            bot.kick_chat_member(msg.chat.id, user.id)
        except Exception as e:
            print(e)
            print(user)


class clr:

    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Magenta = '\033[95m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Grey = '\033[90m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


if __name__ == '__main__':
    print("ArabianRemover_bot Started")
    bot.polling(none_stop=True)
