import telebot
import requests
import os
import logging
import sys

# Token embedded directly into the code
TOKEN = "7164714428:AAGLz5l7LhYzaddLXmb4DhGrulbpvQ-3HsE"
fixed_url = "https://www.palringo.com/avatar.php?id=##&size=214"

logging.basicConfig(filename='errors.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    if TOKEN:
        print("تم التسجيل بنجاح")
        bot = telebot.TeleBot(TOKEN)
        chat_data = {}

        if not os.path.exists('Room'):
            os.makedirs('Room')

        if not os.path.exists('Account'):
            os.makedirs('Account')

        def send_images(chat_id, image_urls):
            for url in image_urls:
                bot.send_photo(chat_id, url)

        @bot.message_handler(commands=['start'])
        def handle_start(message):
            bot.send_message(message.chat.id, "ارسل العضوية 🥃:")
            chat_data[message.chat.id] = {'waiting_for_membership': True}

        @bot.message_handler(func=lambda message: chat_data.get(message.chat.id, {}).get('waiting_for_membership', False) or chat_data.get(message.chat.id, {}).get('waiting_for_room', False))
        def handle_membership(message):
            try:
                if 'waiting_for_membership' in chat_data.get(message.chat.id, {}):
                    membership_numbers = message.text.split(',')
                    for membership_number in membership_numbers:
                        membership_number = int(membership_number.strip())
                        file_url = fixed_url.replace('##', str(membership_number))

                        bot.send_message(message.chat.id, "ِ        خذلك جغمة ☻...🥃‌‏ ᴝgԸɹɹɹ")

                        response = requests.get(file_url)
                        file_name = f"Account/{membership_number}.gif"

                        with open(file_name, 'wb') as file:
                            file.write(response.content)

                        bot.send_document(message.chat.id, open(file_name, 'rb'), caption="🥃‏‏┊‏‏ ᴝgԸɹɹɹ GIF")

                        # Delete image after sending
                        os.remove(file_name)

                    chat_data[message.chat.id] = {}
                    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(telebot.types.KeyboardButton('🆔 إدخال عضوية أخرى'))
                    keyboard.add(telebot.types.KeyboardButton('🆔 الغرف ROom'))
                    keyboard.add(telebot.types.KeyboardButton('انهاء 🔴'))
                    bot.send_message(message.chat.id, "/start:", reply_markup=keyboard)

                elif 'waiting_for_room' in chat_data.get(message.chat.id, {}):
                    room_number = int(message.text)
                    room_url = "https://www.palringo.com/avatar.php?id={}&type=g&size=large".format(room_number)

                    bot.send_message(message.chat.id, "خذلك جغمة ☻...🥃‌‏ ᴝgԸɹɹɹ")
                    chat_data[message.chat.id] = {'waiting_for_room': True}

                    response = requests.get(room_url)
                    file_name = f"Room/{room_number}.gif"

                    with open(file_name, 'wb') as file:
                        file.write(response.content)

                    bot.send_document(message.chat.id, open(file_name, 'rb'), caption="🥃‏‏┊‏‏ ᴝgԸɹɹɹ GIF")

                    # Delete image after sending
                    os.remove(file_name)

                    chat_data[message.chat.id] = {}
                    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(telebot.types.KeyboardButton('🆔 إدخال عضوية أخرى'))
                    keyboard.add(telebot.types.KeyboardButton('🆔 الغرف ROom'))
                    keyboard.add(telebot.types.KeyboardButton('انهاء 🔴'))
                    bot.send_message(message.chat.id, "/start:", reply_markup=keyboard)

            except ValueError:
                bot.send_message(message.chat.id, "يرجى إدخال رقم صحيح.")
                logging.error("Invalid number entered.")

            except Exception as e:
                bot.send_message(message.chat.id, "حدث خطأ أثناء معالجة الطلب. يرجى المحاولة مرة أخرى لاحقًا.")
                logging.error(f"Error: {str(e)}")

        @bot.message_handler(func=lambda message: message.text == '🆔 إدخال عضوية أخرى')
        def handle_another_membership(message):
            bot.send_message(message.chat.id, "ارسل 🥃 عضوية جديدة:")
            chat_data[message.chat.id] = {'waiting_for_membership': True}

        @bot.message_handler(func=lambda message: message.text == '🆔 الغرف ROom')
        def handle_room(message):
            bot.send_message(message.chat.id, "ارسل 🏠 رقم الغرفة:")
            chat_data[message.chat.id] = {'waiting_for_room': True}

        @bot.message_handler(func=lambda message: message.text == 'انهاء 🔴')
        def handle_end(message):
            bot.send_message(message.chat.id, "تم انهاء العملية.")
            chat_data[message.chat.id] = {}

        bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()
