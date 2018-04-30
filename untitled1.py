# coding: utf8
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import time
import requests

import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# просто команды
def time_1(bot, update):
    t = time.asctime().split()[-2]
    n = ''.join(t)
    update.message.reply_text(n)


def data(bot, update):
    t = time.asctime().split()[1:3]
    n = ' '.join(t)
    update.message.reply_text(n)


def address(bot, update):
    update.message.reply_text(" ул. Посадского, 246, Саратов")


def phone(bot, update):
    update.message.reply_text("Телефон: 8 (845) 227-50-65 ")


def site(bot, update):
    update.message.reply_text("Сайт: http://lmi-school.ru/")


def work_time(bot, update):
    update.message.reply_text("Время работы: пн-пт -- 9-00 - 19-00")


# опрос

def start(bot, update):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живете? (Можете не отвечать на данный вопрос, нажав команду /skip.")

    # Это то число, которое является ключем в словаре states — втором параметре ConversationHandler'а.
    return 1


def first_response(bot, update, user_data):
    # Сохраняем ответ в словаре.
    user_data['locality'] = update.message.text
    update.message.reply_text("Какая погода в городе {0}?".format(user_data['locality']))
    return 2


def skip(bot, update, user_data):
    update.message.reply_text("Какая погода у вас за окном?".
                              format(user_data['locality']))
    return 2


def second_response(bot, update, user_data):
    weather = update.message.text
    update.message.reply_text("Спасибо за участие в опросе! Привет, {0}!".
                              format(user_data['locality']))  # Используем user_data в ответе.
    return ConversationHandler.END


def stop(bot, update):
    update.message.reply_text(
        "Жаль. А было бы интерсно пообщаться. Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.


# help
def help(bot, update):
    update.message.reply_text(
        "Команды: /time, /data, /adress, /phone, /site, /work_time, /start, /start_translator,/geocoder, /picture . Если хотите узнать, как работает команда, вызовите её и получите нужную информацию.")
    return 1


def time_2(bot, update):
    update.message.reply_text("Данная команда выводит вреамя в данный момент времени.")
    return ConversationHandler.END


def data_1(bot, update):
    update.message.reply_text("Данная команда выводит дату в данный момент времени.")
    return ConversationHandler.END


def adress_1(bot, update):
    update.message.reply_text(
        "Эта команда выводит адрес Лицея Математики и Информатики в городе Саратове, на всякий случай!)")
    return ConversationHandler.END


def phone_1(bot, update):
    update.message.reply_text("Номер МАУО 'ЛМИ' ")
    return ConversationHandler.END


def site_1(bot, update):
    update.message.reply_text("Команда выводит ссылку на сайт МАУО 'ЛМИ')")
    return ConversationHandler.END


def work_time_1(bot, update):
    update.message.reply_text("Выводит время работы МАУО 'ЛМИ'")
    return ConversationHandler.END


def start_1(bot, update):
    update.message.reply_text("Можете пройти мини-опрос)")
    return ConversationHandler.END


def start_translator_1(bot, update):
    update.message.reply_text(
        "Команда, которая поможет переводить слова с русского на английский и наооборот!")
    return ConversationHandler.END


def stop_1(bot, update):
    update.message.reply_text(
        "Надеюсь, вам полезна наша информация!")
    return ConversationHandler.END

def geocoder_1(bot, update):
    update.message.reply_text(
        "Эта команда, который по запросу пользователя присылает ему карту с запрошенным объектом, чтобы была картинка, нужна вызвать /picrure  ")
    return ConversationHandler.END
# переводчик
def start_translator(bot, update):
    update.message.reply_text(
        "Добро пожаловать, здесь ты можешь воспользоваться переводчиком, который перводит с русского на английский: /translater_ru, и наооборот /translater_en.")
    return 1
def picture_1(bot, update):
    update.message.reply_text(
        "Вы водит картинку места, вызывается после команды /geocoder ")
    return 1


def translater_ru(bot, updater):
    accompanying_text = "Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/."
    translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    response = requests.get(
        translator_uri,
        params={
            "key":
                "{trnsl.1.1.20180430T071140Z.3cc311352ad543ba.3d4c24bc3e732bab8507bd5c884b783c229a7d9e}",
        # Ключ, который необходимо получить по ссылке в тексте.
            "lang": "ru-en",  # Направление перевода: с русскго на английский.
            "text": updater.message.text  # То, что нужно перевести.
        })
    updater.message.reply_text(
        "\n\n".join([response.json()["text"][0], accompanying_text]))
    return 2


def translater_en(bot, updater):
    accompanying_text = "Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/."
    translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    response = requests.get(
        translator_uri,
        params={
            "key":
                "{trnsl.1.1.20180430T071140Z.3cc311352ad543ba.3d4c24bc3e732bab8507bd5c884b783c229a7d9e}",
            "lang": "en-ru",
            "text": updater.message.text
        })
    updater.message.reply_text(
        "\n\n".join([response.json()["text"][0], accompanying_text]))
    return 2


def stop_2(bot, update):
    update.message.reply_text(
        "Надеюсь, вам полезна наша информация!")
    return ConversationHandler.END

def text_translator(bot,update):
    update.message.reply_text(
        "Можешь продолжить переводить, вызвав нужную функцию), или вызвать /stop, чтобы закончить. ")
    return 1




#геокодер
def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={address}&format=json".format(**locals())

    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None

def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return (None,None)

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l,b = envelope["lowerCorner"].split(" ")
    r,t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())

    return (ll, span)

def geocoder(bot, updater):
    ll, spn = get_ll_spn(updater.message.text)

    static_api_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map".format(**locals())
    print(static_api_request)
    bot.sendPhoto(
        updater.message.chat.id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API по сути является ссылкой на картинку.
        static_api_request#open('image.jpg', 'rb')
    )

def picture(bot, updater):
    updater.message.reply_text(updater.message.text)
    bot.sendPhoto(updater.message.chat.id, open('image.jpg', 'rb'))

def main():
    # Создаем объект updater. Вместо слова "TOKEN" надо разместить полученнй от @BotFather токен
    updater = Updater("564873346:AAEKyGZSN0xSFAQOui5Q38beysSphyJWEx4")

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("time", time_1))
    dp.add_handler(CommandHandler("data", data))

    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))

    dp.add_error_handler(error)

    dp.add_handler(CommandHandler('geocoder', geocoder))
    dp.add_handler(CommandHandler('picture', picture))

    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True),
                CommandHandler('skip', skip, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, second_response, pass_user_data=True)],

        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler_1 = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('help', help)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [CommandHandler('time', time_2), CommandHandler('data', data_1), CommandHandler('adress', adress_1),
                CommandHandler('phone', phone_1), CommandHandler('site', site_1),
                CommandHandler('work_time', work_time_1),
                CommandHandler('start', start_1), CommandHandler('start_translator', start_translator_1)],

        },
        fallbacks=[CommandHandler('stop', stop_1)]
    )
    conv_handler_translator = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start_translator', start_translator)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [CommandHandler('translater_ru', translater_ru), CommandHandler('translater_en', translater_en)],
            2: [MessageHandler(Filters.text,text_translator)],
        },
        fallbacks=[CommandHandler('stop', stop_2)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_1)
    dp.add_handler(conv_handler_translator)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждем завершения приложения. (например, получение сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
