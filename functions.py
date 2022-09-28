import json
import random
from server import bot
import telebot
import csv
import time





# Словарь для хранения текущего пункта
active_function = {
    "game_cities" : False,  # Игра Города
    "game_secret": False,   # Загадки
    "game_words": False,    # Составить слова
    "movie_year": False,    # Фильм по году
    "movie_genre": False,   # Фильм по жанру
    "movie_name": False,   # Фильм по имени
    "rock_paper_scissors":False, #Камень , ножницы, бумага

}


# Массив для городов, которые ещё не выбирались
cities_list = []

# Массив для сыгранных городов
cities_list_played = []

# Последний названный город
city_last = ''

# Словарь загадок
secrets_dict = {}

# Текущая загадка с ответом
secret_active = {}

# Словарь слов с подсловами
word = {}

# Текущее загаданное слово
word_active = ''

# Текущее слово с подсловами
subwords_active = []

rounds = 0












# Меню для поиска фильмов
def movie_menu(message):
    active_function["movie_name"] = False
    active_function["movie_year"] = False
    active_function["movie_genre"] = False
    movie_list = [['Поиск по названию'],
                 ['Поиск по жанру', 'Поиск по году'],
                 ['Назад в главное меню']]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for game in movie_list:
        markup.add(*game)
    bot.send_message(chat_id=message.chat.id,
                     text='❓Какой поиск тебя интересует❓\n',
                     reply_markup=markup)





# Поиск фильма по году
def movie_year(message):
    if message.text == 'Закончить' or message.text == 'Назад в главное меню':
        movie_menu(message)
        return

    with open("movies.json", encoding='utf-8') as file:
        data = json.load(file) # Читаем весь файл с фильмами

    count_search = 0
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Закончить')
    for i in range(len(data)):
        genre_arr = ''
        # Если введенный год равен году в файле
        if message.text.lower() in data[i]["year"]:

            count_search += 1

            for j in range(len(data[i]["genre"])):
                genre_arr += data[i]["genre"][j] + '\t'
                time.sleep(1.21)
                answer = f'Рекомендую к просмотру🔽\n'\
                         f'Название фильма: {data[i]["name"]} \n' \
                         f'Жанры фильма: {genre_arr} \n'\
                f'Год фильма: {data[i]["year"]}\n' \

                bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)

        if count_search == 0:
            answer = f'🚫 Фильмов с таким годом нет в моей базе🚫 \n' \
                     f'Попробуйте позже, когда я обновлю базу.'
            bot.send_message(chat_id=message.chat.id,
                             text=answer + '\n',
                             reply_markup=markup)

# Поиск фильма по имени
def movie_name(message):
    if message.text == 'Закончить' or message.text == 'Назад в главное меню':
        movie_menu(message)
        return
    time.sleep(0.09)
    with open("movies.json", encoding='utf-8') as file:
        data = json.load(file)

    count_search = 0
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Закончить')
    for i in range(len(data)):
        genre_arr = ''
        if message.text.lower() in data[i]["name"].lower():
            count_search += 1



            for j in range(len(data[i]["genre"])):
                genre_arr += data[i]["genre"][j] + '\t'
                time.sleep(1.2)
            answer = f'Рекоменую к просмотру🔽\n' \
                     f'Название фильма: {data[i]["name"]} \n' \
                     f'Жанры фильма: {genre_arr} \n', \
                     f'Год фильма: {data[i]["year"]}\n'
            bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)





    if count_search == 0:
        answer = f'🚫Фильмов с таким названием нет в моей базе🚫 \n' \
                 f'Попробуйте позже, когда я обновлю базу.'
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

# Поиск фильма по жанру
def movie_genre(message):
    if message.text == 'Закончить' or message.text == 'Назад в главное меню':
        movie_menu(message)
        return

    with open("movies.json", encoding='utf-8') as file:
        data = json.load(file)

    count_search = 0
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Закончить')
    for i in range(len(data)+0):
        genre_arr = data[i]["genre"]
        for genre in genre_arr:
            if message.text.lower() in genre.lower():
                count_search += 1

                time.sleep(1.21)

                answer = f'Рекомендую к просмотру 🔽\n' \
                         f'Название фильма: {data[i]["name"]} \n' \
                         f'Год фильма: {data[i]["year"]}\n'
                f':Жанр фильма {data[i]["genre"]}\n'\

                bot.send_message(chat_id=message.chat.id, text=answer + '\t'
                                 , reply_markup=markup)


    if count_search == 0:
        answer = f'🚫 Фильмов с таким жанром нет в моей базе🚫  \n' \
                 f'Попробуйте позже, когда я обновлю базу '
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

# Меню для выбора игры
def game_menu(message):
    active_function["game_words"] = False
    active_function["game_secret"] = False
    active_function["game_cities"] = False
    game_list = [['Города'], ['Загадки'],
                 ['Найди слова'],['Камень,ножницы,бумага'],
                 ['Назад в главное меню']]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for game in game_list:
        markup.add(*game)
    bot.send_message(chat_id=message.chat.id,
                     text='Жду твоего решения😊\n',
                     reply_markup=markup)





# Заполнение массива с названием городов
def set_cities():
    with open("city.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        for row in file_reader:
            cities_list.append(row[3])



# Правила игры "Города"
def help_cities(message):
    global cities_list, cities_list_played
    cities_list.clear()
    cities_list_played.clear()
    set_cities()
    answer = f'🏙 Приветствую в игре "Города 🏙" \n' \
             f'Давай для начала вспомним правила игры: \n' \
             f'Нужно называть города на последнюю букву \n' \
             f'Если последняя буквы Ы или Й, то называем на предпоследнюю \n' \
             f'Например: Москва (последняя буква А), значит следующим может быть Астрахань \n' \
             f'Попробуем сыграть? 😊\n'
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    answer_yes = telebot.types.InlineKeyboardButton(text='Да ✔', callback_data='cities_yes')
    answer_no = telebot.types.InlineKeyboardButton(text='Нет ✖', callback_data='cities_no')
    markup.add(answer_yes, answer_no)
    bot.send_message(chat_id=message.chat.id,
                     text=answer,
                     reply_markup=markup)

# Процесс игры в города
def play_cities(message):
    global city_last, cities_list
    message.text = message.text.strip()
    if message.text.lower() in cities_list:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        game_end = telebot.types.InlineKeyboardButton(text='Закончить ❌', callback_data='cities_no')
        last_char = telebot.types.InlineKeyboardButton(text='На какую букву ❓', callback_data='last_char')
        markup.add(last_char, game_end)
        cities_list.remove(message.text)
        check_last_city = False  # Проверка на правильность введённого города
        check_played_city = False  # Проверка на ранее сыгранное слово

        if city_last == '':
            check_last_city = True
        elif message.text[0].lower() == city_last[-1]:# Поиск слова по псоледней букве ране ведённого слова игроком.
            check_last_city = True

        if message.text.lower() not in cities_list_played:
            check_played_city = True

        if message.text[-1] == 'ь' or message.text[-1] == 'ы' or message.text[-1] == 'й':
            message.text = message.text[:-1]

        if message.text.lower() not in cities_list_played and check_last_city and check_played_city:
            cities_list_played.append(message.text)  # Добавляем названный город в массив сыгранных городов
            for city in cities_list:
                if city[0].lower() == message.text[-1]: # Если первая буква найденного города равна последней введенного
                    answer = city # Ответ бота - найденный город
                    cities_list_played.append(city) # Добавляем названный город в массив сыгранных городов
                    cities_list.remove(city) # Удаляем из массива возможных городов
                    if city[-1] == 'ь' or city[-1] == 'ы' or city[-1] == 'й':
                        city_last = city[:-1] # Последний город равен ответу бота
                    else:
                        city_last = city
                    bot.send_message(chat_id=message.chat.id,
                                     text=answer,
                                     reply_markup=markup)
                    break
        else:
            answer = f'Такой город уже называли 🔇'
            bot.send_message(chat_id=message.chat.id,
                             text=answer,
                             reply_markup=markup)
    else:
        answer = f'🚫Такого города не существует🚫 \n' \
                 f'Попробуй ещё раз'
        bot.send_message(chat_id=message.chat.id,
                         text=answer)
        raise

# Наполняем словарь загадок
def set_secrets():
    with open("secret.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        for row in file_reader:
            row[0] = row[0].replace(r'\n', '\n')
            secrets_dict[row[0]] = row[1]

# Правила игры "Загадки"
def help_secret(message):
    global secrets_dict, secret_active
    secrets_dict.clear()
    secret_active.clear()
    set_secrets()
    answer = f'👋🏻 Приветствую в моей игре "Загадки 👋🏻" \n' \
             f'Правила очень простые \n' \
             f'Я задаю тебе загадку, а тебе нужно предлагать ответы \n' \
             f' Сыграем?😊'
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    secret_start = telebot.types.InlineKeyboardButton(text='Начать игру ✔', callback_data='secret_yes')
    secret_stop = telebot.types.InlineKeyboardButton(text='Закончить игру ✖', callback_data='secret_no')
    markup.add(secret_start, secret_stop)
    bot.send_message(chat_id=message.chat.id,
                     text=answer,
                     reply_markup=markup)

# Загадываем загадку пользователю
def send_secret(message):
    secret_active.clear() # Очищаем словарь текущей загадки
    if len(secrets_dict) != 0:
        secret_sends, answer_secret = random.choice(list(secrets_dict.items())) # Выбираем рандомную загадку
        secrets_dict.pop(secret_sends) # Удаляем загадку из словаря загадок
        secret_active[secret_sends] = answer_secret # Устанавливаем текущую загадку и ответ на неё
        bot.send_message(chat_id=message.chat.id,
                         text=f'<b>❓Вот моя загадка:</b> \n'
                              f'{secret_sends}',
                         parse_mode='html')
    else:# Вариант , если загадки закончились.(Редкость)
        answer = 'У меня закончились загадки \n' \
                 'Давай попробуем в следующий раз 😊'
        bot.send_message(chat_id=message.chat.id,
                         text=answer)
        game_menu(message)

# Процесс игры в Загадки
def play_secret(message):
    sec = secret_active.keys()
    answer_secret = ''
    for i in sec:
        answer_secret = secret_active.get(i)
        answer_secret = answer_secret.lower()
    if message.text.strip().lower() == answer_secret:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2.02)
        secret_next = telebot.types.InlineKeyboardButton(text='Продолжить✔', callback_data='secret_yes')
        secret_stop = telebot.types.InlineKeyboardButton(text='Закончить✖', callback_data='secret_no')
        markup.add(secret_next, secret_stop)
        bot.send_message(chat_id=message.chat.id,
                         text='Молодец!',
                         reply_markup=markup)
    else:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2.02)
        secret_answer = telebot.types.InlineKeyboardButton(text='Ответ✔', callback_data='secret_answer')
        secret_stop = telebot.types.InlineKeyboardButton(text='Закончить✖', callback_data='secret_no')
        markup.add(secret_answer, secret_stop)
        bot.send_message(chat_id=message.chat.id,
                         text='Неверный ответ!✖ \n'
                              'Подумай ещё',
                         reply_markup=markup)
# Наполняем массивы словами
def set_word():
    global word, word_active
    with open("words.json", encoding='utf-8') as file:
        data = json.load(file) # Читаем файл

    for i in range(len(data)):
        word[data[i]["word"]] = data[i]["subwords"] # Добавляем новые элементы в словарь

# Правила игры "Найди слова"
def help_words(message):
    global word, subwords_active
    word.clear() # Очищаем словарь всех слов
    subwords_active.clear() # Очищаем массив всех подслов загаданного слова
    set_word() # Читаем файл и заполняем словари
    answer = f'👋🏻 Приветствую в моей игре "Найди слова 👋🏻" \n' \
             f'Правила очень простые \n' \
             f'Я задаю тебе слово, \n' \
             f'А тебе нужно найти все слова, которые можно из него составить \n' \
             f'Удачи!'
    markup = telebot.types.InlineKeyboardMarkup(row_width=2.02)
    word_start = telebot.types.InlineKeyboardButton(text='Начать✔', callback_data='word_yes')
    word_stop = telebot.types.InlineKeyboardButton(text='Закончить✖', callback_data='word_no')
    markup.add(word_start, word_stop)
    bot.send_message(chat_id=message.chat.id,text=answer,reply_markup=markup)

# Загадываем слово
def send_word(message):
    global word_active, subwords_active
    word_active = '' # Очищаем загаданное слово
    subwords_active.clear()  # Очищаем словарь текущих подслов
    if len(word) != 0: # Если ещё не все слова были сыграны
        word_active, subwords_active = random.choice(list(word.items()))  # Выбираем рандомное слово
        word.pop(word_active)  # Удаляем слово из словаря
        bot.send_message(chat_id=message.chat.id,
                         text=f'<b>Я загадываю слово:</b> \n'
                              f'{word_active} \n'
                              f'Тебе нужно будет назвать: {len(subwords_active)} слов',
                         parse_mode='html')
    else:
        answer = 'У меня закончились слова \n' \
                 'Давай попробуем в следующий раз :)'

        bot.send_message(chat_id=message.chat.id+ '\a',
                         text=answer)
        game_menu(message) # Возвращаемся в игровое меню

# Процесс игры в "Найди слова"
def play_word(message):
    global subwords_active
    if message.text.strip().lower() in subwords_active and len(subwords_active) == 1:
        subwords_active.remove(message.text.strip().lower())
        markup = telebot.types.InlineKeyboardMarkup(row_width=2.02)
        word_cont = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='word_yes')
        word_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='word_no')
        markup.add(word_cont, word_stop)
        answer = f'Ты отгадал все слова, которые можно составить из слова {word_active} \n' \
                 f'Хочешь продолжить?'

        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

    elif message.text.strip().lower() in subwords_active and len(subwords_active) > 1:
        subwords_active.remove(message.text.strip().lower())
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        word_help_user = telebot.types.InlineKeyboardButton(text='Подсказка', callback_data='word_help')
        markup.add(word_help_user)
        answer = f'Такое слово присутствует \n' \
                 f'Осталось угадать: {int(len(subwords_active))} слов\n'
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

    elif message.text.strip().lower() not in str(subwords_active):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        word_help_user = telebot.types.InlineKeyboardButton(text='Подсказка', callback_data='word_help')
        markup.add(word_help_user)
        answer = f'Такого слова нет \n' \
                 f'Попробуй ещё раз'

        bot.send_message(
            chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Играем в города
    if call.data == 'cities_yes':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Жду от тебя название первого города!')


        active_function["game_cities"] = True

    # На какую букву называем город
    elif call.data == 'last_char':
        bot.send_message(chat_id=call.message.chat.id,text=f'{city_last[-1].upper().lower()}\n')

    # Отказываемся играть в города
    elif call.data == 'cities_no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Буду ждать следующей игры!')

        games(call.message)
        active_function["game_cities"] = False

    # Играем в загадки
    elif call.data == 'secret_yes':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        active_function["game_secret"] = True
        send_secret(call.message)

    # Получить ответ на загадку
    elif call.data == 'secret_answer':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        sec = secret_active.keys()
        answer = ''
        for i in sec:
            answer = secret_active.get(i)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'Ответ: {answer} \n'
                              f'Запомни ответ на загадку!')

        send_secret(call.message)

    # Заканчиваем играть в загадки
    elif call.data == 'secret_no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Буду ждать следующей игры!😌')

        games(call.message)
        active_function["game_secret"] = False

    # Играем в "Найди слова"
    elif call.data == 'word_yes':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        active_function["game_words"] = True
        send_word(call.message)

    # Помощь в "Найди слова"
    elif call.data == 'word_help':
        if len(subwords_active) != 1:
            random_index = random.randrange(len(subwords_active))
            answer = subwords_active[random_index]
            subwords_active.remove(answer)
            bot.send_message(chat_id=call.message.chat.id,
                             text=f'Есть такое слово: {answer} \n'
                                  f'✨Осталось слов: {len(subwords_active)} слов ✨')

        elif len(subwords_active) == 1:
            random_index = random.randrange(len(subwords_active))
            answer = subwords_active[random_index]
            subwords_active.remove(answer)
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            word_cont = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='word_yes')
            word_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='word_no')
            markup.add(word_cont, word_stop)
            bot.send_message(chat_id=call.message.chat.id,
                             text=f'✨Это последнее слово: {answer}\n',
                             reply_markup=markup)


    # Заканчиваем играть в "Найди слова"
    elif call.data == 'word_no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='✨ Буду ждать следующей игры! ✨')
        games(call.message)
        active_function["game_words"] = False

def description(message):
    answer = 'Приветствую вас в игре Камень ножницы бумага!' \
             'ВЫ загадываете камень,ножницы либо бумагу!' \
             'И робот тоже выбирает что-то одно!Кто кого побил,тот победил!' \
             'Попробуем сыграть?'
    bot.send_message(chat_id=message.chat.id,text=answer)
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button2 = telebot.types.InlineKeyboardButton(text='Начать',callback_data='yes')
    button1 = telebot.types.InlineKeyboardButton(text='Стоп', callback_data='no')

    markup.add(button2,button1)
@bot.message_handler(content_types=["text"])
def rock_paper_scissors(message):
    if message.text =='Начать':
        bot.send_message(chat_id=message.chat.id, text='Сколько раундов ты хочешь сыграть?')
        rounds.text = message.text.strip()
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        button6 = telebot.types.InlineKeyboardButton(text='КАМЕНЬ', callback_data='к')
        button5 = telebot.types.InlineKeyboardButton(text='НОЖНИЦЫ', callback_data='н')
        button4 = telebot.types.InlineKeyboardButton(text="БУМАГА", callback_data="б")
        markup.add(button6, button4, button5)
        while str(rounds) != '0':
            bot.send_message(chat_id=message.chat.id, text='Выбирай! камень,ножницы или бумага!', reply_markup=markup)

            bot_step = random.randint(0, 3)  # 1 камень 2 ножницы 3 бумага
            if message.text == "БУМАГА" and bot_step == 3:
                bot.send_message(chat_id=message.chat.id, text='Ничья!Бот тоже выбрал бумагу!')
            elif message.text == "БУМАГА" and bot_step == 2:
                bot.send_message(chat_id=message.chat.id, text='Ты проиграл!Бот походил бумагой!')
            elif message.text == "БУМАГА" and bot_step == 1:
                bot.send_message(chat_id=message.chat.id, text="Ты победил!Бот походил камнем!")
            elif message.text == 'КАМЕНЬ' and bot_step == 3:
                bot.send_message(chat_id=message.chat.id, text='Ты проиграл!Бот походил бумагой!')
            elif message.text == 'КАМЕНЬ' and bot_step == 1:
                bot.send_message(chat_id=message.chat.id, text="Ничья!Бот тоже выбрал камень!")
            elif message.text == 'КАМЕНЬ' and bot_step == 2:
                bot.send_message(chat_id=message.chat.id, text="Ты победил!Бот выбрал ножницы!")
            elif message.text == 'НОЖНИЦЫ' and bot_step == 3:
                bot.send_message(chat_id=message.chat.id, text='Ты победил!Бот походил бумагой!')
            elif message.text == 'НОЖНИЦЫ' and bot_step == 1:
                bot.send_message(chat_id=message.chat.id, text="ТЫ проиграл!Бот походил камень!")
            elif message.text == 'НОЖНИЦЫ' and bot_step == 2:
                bot.send_message(chat_id=message.chat.id, text="Ты проиграл!Бот выбрал ножницы!")
            telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button8 = telebot.types.InlineKeyboardButton(text='СТОП!', callback_data='н')
            button7 = telebot.types.InlineKeyboardButton(text="ПРОДОЛЖИТЬ ИГРУ!", callback_data="б")
            markup.add(button7, button8)
            if message.text == "ПРОДОЛЖИТЬ ИГРУ!":
                continue
            else:
                game_menu(message)

# Обработка команды /start
@bot.message_handler(commands=["start"])
def start(message):

    answer = f'{message.from_user.first_name}, привет! 👋🏻 \n' \
             f'✨ Давай начнём работу ✨ \n' \
             f'Для этого нажми сюда --> /menu'
    bot.send_message(chat_id=message.chat.id, text=answer)

# Обработка команды /menu
@bot.message_handler(commands=["menu"])
def menu(message):
    active_function["movie_genre"] = False
    active_function["movie_year"] = False
    active_function["movie_name"] = False
    active_function["game_cities"] = False
    active_function["game_secret"] = False
    active_function["game_words"] = False
    menu_list = [['Поиск фильма'], ['Игры']]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for command in menu_list:
        markup.add(*command)
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите интересующий вас пункт',
                     reply_markup=markup)



# Обработка команды /games
@bot.message_handler(commands=["games"])
def games(message):
    answer = '🔥Добро пожаловать в игровое меню! 🔥 \n' \
             'Игры, в которые мы можем сыграть: \n' \
             '1.Города✨ \n' \
             '2.Загадки✨\n' \
             '3.Составить слова из слова✨ \n' \
             '4.Камень,ножницы,бумага✨ \n' \
             'Для того, чтобы начать выберите игру из меню!' \

    bot.send_message(chat_id=message.chat.id,text=answer)
    game_menu(message)


# Обработка команды /movies
@bot.message_handler(commands=["movies"])
def movies(message):
    answer = f'🎥 Добро пожаловать в меню поиска фильма! 🎥\n' \
             f'✨Я умею искать фильм по параметрам: \n' \
             f'1. Название ✨\n' \
             f'2. Год ✨\n' \
             f'3. Жанр ✨\n' \
             f'Для того, чтобы начать выберите игру из меню!🔽\n'\
             f'В список фильмов входить подборка фильмов с сервиса "кинопоиск".Мы выбрали самые интересные фильмы для вас😌.\n'
    bot.send_message(chat_id=message.chat.id,text=answer)
    movie_menu(message)






# Обработка текста от пользователя (При нажатии на кнопку в клавиатуре всегда отправляется текст Боту)
@bot.message_handler(content_types=['text'])
def action(message):
    if message.text == 'Игры':
        games(message)

    elif message.text == 'Города':
        help_cities(message)

    elif message.text == 'Загадки':
        help_secret(message)

    elif message.text == 'Найди слова':
        help_words(message)

    elif active_function["game_cities"]:
        play_cities(message)

    elif active_function["game_secret"]:
        play_secret(message)

    elif active_function["game_words"]:
        play_word(message)

    elif message.text == 'Поиск фильма':
        movies(message)







    elif message.text == 'Поиск по названию':
        bot.send_message(chat_id=message.chat.id,
                         text='✨Введи название фильма, который ты хочешь найти \n'
                              'Например: Назад в будущее✨🔽\n')
        active_function["movie_genre"] = False
        active_function["movie_year"] = False
        active_function["movie_name"] = True

    elif message.text == 'Поиск по жанру':
        bot.send_message(chat_id=message.chat.id,
                         text='✨Введи жанр фильмов, которые ты хочешь найти \n'
                              'Например: Мультфильм✨🔽\n')
        active_function["movie_genre"] = True
        active_function["movie_year"] = False
        active_function["movie_name"] = False

    elif message.text == 'Поиск по году':
        bot.send_message(chat_id=message.chat.id,
                         text='✨Введи год фильмов, которые ты хочешь найти \n'
                              'Например: 2020✨🔽\n')
        active_function["movie_genre"] = False
        active_function["movie_year"] = True
        active_function["movie_name"] = False

    elif active_function["movie_name"]:
        movie_name(message)

    elif active_function["movie_year"]:
        movie_year(message)

    elif active_function["movie_genre"]:
        movie_genre(message)


    elif message.text == 'Назад в главное меню':
        menu(message)





