import telegram
import requests
from bs4 import BeautifulSoup
import base64

# Токен бота и username менеджера
TOKEN = '6140734425:AAE60R_-aNBJJrTrooEw6CC8v_pbaeHpTaE'
manager_username = 'timvista'

# Создание объекта бота
bot = telegram.Bot(token=TOKEN)

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введите артикул или название товара с сайта Nike.com")

# Обработчик сообщений
def echo(update, context):
    # Получение текста сообщения
    text = update.message.text

    # Поиск товара на сайте Nike.com
    url = 'https://www.nike.com/w?q=' + text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product = soup.find('div', {'class': 'product-card__body'})

    # Если товар не найден, ищем наиболее подходящую позицию
    if not product:
        product = soup.find('div', {'class': 'product-card__body'})
    
    # Получение изображения товара
    image_url = product.find('img')['src']

    # Декодирование изображения из base64
    image_data = base64.b64decode(image_url.split(',')[1])

    # Получение пути к файлу
    file_path = 'images/' + image_url.split('/')[-1]

    # Сохранение изображения на сервере
    with open(file_path, 'wb') as f:
        f.write(image_data)

    # Отправка фотографии
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(file_path, 'rb'))

    # Запрос размера, количества и адреса доставки
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите размер, количество и адрес доставки")

    # Формирование сообщения о заказе
    order_info = f"Пользователь @{update.message.from_user.username} заказал товар {text} в количестве {quantity} размера {size} по адресу {address}"

    # Отправка сообщения о заказе на аккаунт менеджера
    context.bot.send_message(chat_id=manager_username, text=order_info)

# Создание обработчиков команд и сообщений
from telegram.ext import CommandHandler, MessageHandler, Filters
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

# Добавление обработчиков в диспетчер
from telegram.ext import Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Запуск бота
updater.start_polling()
