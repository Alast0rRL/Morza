import telebot
from telebot import types

# Словари с азбукой Морзе для русских букв и цифр
morse_russian = {
    '.-': 'А', '-...': 'Б', '.--': 'В', '--.': 'Г', '-..': 'Д', '.': 'Е', '.-..-': 'Ё', '...-': 'Ж', '--..': 'З',
    '..': 'И', '.---': 'Й', '-.-': 'К', '.-..': 'Л', '--': 'М', '-.': 'Н', '---': 'О', '.--.': 'П', '.-.': 'Р',
    '...': 'С', '-': 'Т', '..-': 'У', '..-.': 'Ф', '....': 'Х', '-.-.': 'Ц', '---.': 'Ч', '----': 'Ш', '--.-': 'Щ',
    '-..-': 'Ъ', '-.--': 'Ы', '-..-': 'Ь', '..-..': 'Э', '..--': 'Ю', '.-.-': 'Я',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
    '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

morse_code = {
    'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ё': '.-..-', 'Ж': '...-', 'З': '--..',
    'И': '..', 'Й': '.---', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.',
    'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----', 'Щ': '--.-',
    'Ъ': '-..-', 'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

bot = telebot.TeleBot("7068375778:AAGocQ_QHeTPTN3QnaHAPgQdPEYi9_--fnA")

user_steps = {}


def morse_to_text(morse_text, morse_dict):
    words = morse_text.split('   ')  # Разделение слов в тексте Морзе
    decoded_text = ''
    for word in words:
        letters = word.split()  # Разделение букв в слове
        for letter in letters:
            if letter in morse_dict:
                decoded_text += morse_dict[letter]
            else:
                decoded_text += ' '
        decoded_text += ' '
    return decoded_text.strip()

def text_to_morse(text, morse_dict):
    morse_result = []
    for char in text.upper():
        if char in morse_dict:
            morse_result.append(morse_dict[char])
        else:
            morse_result.append(' ')
    return ' '.join(morse_result)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Морза-Русский')
    itembtn2 = types.KeyboardButton('Русский-Морза')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Привет! Я бот, который может преобразовывать текст в азбуку Морзе и обратно. Выберите один из вариантов:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def convert_text(message):
    chat_id = message.chat.id
    msg = message.text

    if msg in ['Морза-Русский', 'Русский-Морза']:
        user_steps[chat_id] = msg
        bot.send_message(chat_id, "Пожалуйста, введите текст.")
    elif chat_id in user_steps:
        choice = user_steps[chat_id]
        text = msg

        if choice == 'Морза-Русский':
            morse_dict = morse_russian
            decoded_text = morse_to_text(text, morse_dict)
            bot.send_message(chat_id, f"Результат:\n{decoded_text}")
        elif choice == 'Русский-Морза':
            morse_dict = morse_code
            encoded_text = text_to_morse(text, morse_dict)
            bot.send_message(chat_id, f"Результат:\n{encoded_text}")
    else:
        bot.send_message(chat_id, "Некорректный выбор. Пожалуйста, выберите один из вариантов: 'Морза-Русский' или 'Русский-Морза'.")


bot.polling()
