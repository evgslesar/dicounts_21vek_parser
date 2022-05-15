import json
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from shop_parser import get_articles, write_to_json
from bot_config import TOKEN


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Список товаров"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Товары со скидкой", reply_markup=keyboard)
    
    
@dp.message_handler(Text(equals="Список товаров"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")
    
    data = get_articles()
    
    with open("sales_articles.json") as file:
        old_data = json.load(file)
        cards = []
        for key, value in data.items():
            if key not in old_data.keys() or value["sale_price"] != old_data[key]["sale_price"]:
                card = f"{hlink(value.get('name'), value.get('item_url'))}\n" \
                    f"{hbold('Бренд: ')} {value.get('brand')}\n" \
                    f"{hbold('Описание: ')} {value.get('description')}\n" \
                    f"{hbold('Цена: ')} {value.get('full_price')}\n" \
                    f"{hbold('Цена со скидкой: ')} - {value.get('discount')}%: {value.get('sale_price')}🔥"
                cards.append(card)
                if not len(cards)%20:
                    time.sleep(5)
                await message.answer(card)
    if len(cards) < 1:
        await message.answer("Новых скидок нет😔")    
        
    write_to_json(data)


def main():
    executor.start_polling(dp)
    
    
if __name__ == "__main__":
    main()
