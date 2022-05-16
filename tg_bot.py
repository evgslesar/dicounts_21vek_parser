import json
import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from shop_parser import get_articles, write_to_json, write_to_csv
from bot_config import TOKEN


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Список товаров", "Скачать CSV"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Товары со скидкой", reply_markup=keyboard)
    
    
@dp.message_handler(Text(equals="Список товаров"))
async def get_discounts(message: types.Message):
    await message.answer("Подождите...")
    
    data = get_articles()
    
    with open("sales_articles.json") as file:
        try:
            old_data = json.load(file)
        except:
            old_data = {"":""}
        cards = []
        for key, value in data.items():
            if not key in old_data.keys():
                card = f"🔥{hbold('НОВЫЙ УЦЕНЕННЫЙ ТОВАР')}🔥\n" \
                    f"{hlink(value.get('name'), value.get('item_url'))}\n" \
                    f"{hbold('Бренд: ')} {value.get('brand')}\n" \
                    f"{hbold('Описание: ')} {value.get('description')}\n" \
                    f"{hbold('Полная цена: ')} {value.get('full_price')}\n" \
                    f"{hbold('Цена со скидкой: ')} -{value.get('discount')}%: {value.get('sale_price')}"
                cards.append(card)
                if not len(cards)%20:
                    time.sleep(5)
                await message.answer(card)

            elif value["sale_price"] < old_data[key]["sale_price"]:
                card = f"⚡️{hbold('УЦЕНЕННЫЙ ТОВАР СТАЛ ЕЩЕ ДЕШЕВЛЕ')}⚡️\n" \
                    f"{hlink(value.get('name'), value.get('item_url'))}\n" \
                    f"{hbold('Бренд: ')} {value.get('brand')}\n" \
                    f"{hbold('Описание: ')} {value.get('description')}\n" \
                    f"{hbold('Полная цена: ')} {value.get('full_price')}\n" \
                    f"{hbold('Новая цена со скидкой: ')} -{value.get('discount')}%: {value.get('sale_price')}\n" \
                    f"{hbold('Старая цена со скидкой: ')} -{old_data[key].get('discount')}%: {old_data[key].get('sale_price')}"                
                cards.append(card)
                if not len(cards)%20:
                    time.sleep(5)
                await message.answer(card)

            elif value["sale_price"] > old_data[key]["sale_price"]:
                card = f"⚡️{hbold('УЦЕНЕННЫЙ ТОВАР СТАЛ НЕМНОГО ДОРОЖЕ')}⚡️\n" \
                    f"{hlink(value.get('name'), value.get('item_url'))}\n" \
                    f"{hbold('Бренд: ')} {value.get('brand')}\n" \
                    f"{hbold('Описание: ')} {value.get('description')}\n" \
                    f"{hbold('Полная цена: ')} {value.get('full_price')}\n" \
                    f"{hbold('Новая цена со скидкой: ')} -{value.get('discount')}%: {value.get('sale_price')}\n" \
                    f"{hbold('Старая цена со скидкой: ')} -{old_data[key].get('discount')}%: {old_data[key].get('sale_price')}"
                cards.append(card)
                if not len(cards)%20:
                    time.sleep(5)
                await message.answer(card)
            
    if len(cards) < 1:
        await message.answer("Новых скидок нет😔")    
        
    write_to_json(data)
    write_to_csv(data)


@dp.message_handler(Text(equals="Скачать CSV"))
async def process_file_command(message: types.Message):
    await message.answer_document(open("sales_articles.csv", "rb"))
    
    
if __name__ == "__main__":
    executor.start_polling(dp)
