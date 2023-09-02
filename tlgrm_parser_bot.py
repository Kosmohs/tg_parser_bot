from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# import os

# os.environ['DISPLAY'] = ':0'

bot = Bot(token='6556202120:AAFQS_uvUkT1mMgZZmzvS7g8XMVzSXPFmk4')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Aloha")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = 'https://ru.wikipedia.org/w/index.php?go=Перейти&search=' + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    links = soup.find_all('div', class_='mw-search-result-heading')

    if len(links) > 0:
        url = 'https://ru.wikipedia.org' + links[0].find('a')['href']

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    driver.execute_script('window.scrollTo(0, 200)')
    driver.save_screenshot('img.png')
    driver.close()
   
    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options = Options()
    # chrome_options.add_argument("headless")
    # driver = webdriver.Chrome(options=chrome_options)
    # # driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=chrome_options)
    # # driver = webdriver.Chrome()
    # driver.get(url)
    # driver.save_screenshot('img.png')
    # driver.close()
    
    with open('img.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo=photo, caption=f'Article link: <a href="{url}">click</a>', parse_mode='HTML')

    # photo = open('img.png', 'rb')
    # await bot.send_photo(message.chat.id, photo=photo, caption=f'Article link: <a href="{url}">click</a>', parse_mode='HTML')

executor.start_polling(dp)