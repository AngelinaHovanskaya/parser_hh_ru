from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from aiogram.filters.command import Command
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import F
from settings import TOKEN
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

options = Options()
options.add_argument('--headless')


def parser_hh(vacancy):
    browser = webdriver.Firefox(options=options)
    browser.get('https://spb.hh.ru/?hhtmFrom=vacancy')

    search_input = browser.find_element(By.ID, 'a11y-search-input')
    search_input.send_keys(vacancy)

    search_input.submit()
    # search_button = browser.find_element(By.CSS_SELECTOR, 'button[data-qa="search-button"]')
    # search_button.click()

    try:
        search_close = browser.find_element(By.CLASS_NAME, 'bloko-modal-close-button')
        search_close.click()
    finally:
        try:
            vacancies_count = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"]').text
        except:
            text = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-catalog-header"]')
            count = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-total-found"]')
            vacancies_count = text.text + count.text

    browser.close()
    return vacancies_count

# print(parser_hh('python developer'))


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Введите название вакансии, чтобы узнать количество объявлений на hh.ru')


@dp.message(F.text)
async def get_count_vacancies(message: types.Message):
    msg = await message.answer(f"Загрузка данных ⏳")

    vacancy = message.text
    count_vacancies = parser_hh(vacancy)
    await msg.delete()
    await message.answer(count_vacancies)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
