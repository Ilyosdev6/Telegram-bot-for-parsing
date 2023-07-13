import telebot

bot = telebot.TeleBot('6028621901:AAGwqot-IAR42iJQkwXHhq4ZeXfNjzybAUA')

processed_users = []

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для обработки целевой аудитории.")

@bot.message_handler(commands=['parse'])
def handle_parse_request(message):
    bot.reply_to(message, "Загрузите файл со списком новых пользователей (каждый пользователь на новой строке).")
    bot.register_next_step_handler(message, handle_parse)

def handle_parse(message):
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        new_users_input = downloaded_file.decode('utf-8')
        new_users = new_users_input.split('\n')
        unique_users, _ = remove_duplicates(new_users, processed_users)
        unique_users = remove_links(unique_users, processed_users)
        if unique_users:
            response = "Новые пользователи без рассылки:\n" + "\n".join(unique_users)
        else:
            response = "Новых пользователей без рассылки не найдено."

        filename = 'response.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response)

        with open(filename, 'rb') as file:
            bot.send_document(message.chat.id, file)
        processed_users.extend(unique_users)
        count_message = "Итоговое количество новых пользователей без рассылки: {}".format(len(unique_users))
        bot.send_message(message.chat.id, count_message)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке запроса.")

def remove_duplicates(list1, list2):
    duplicates = set(list1) & set(list2) 
    list1 = [item for item in list1 if item not in duplicates]
    list2 = [item for item in list2 if item not in duplicates]
    return list1, list2

def remove_links(list1, links_to_remove):
    list1 = [item for item in list1 if item not in links_to_remove]
    return list1

bot.polling()