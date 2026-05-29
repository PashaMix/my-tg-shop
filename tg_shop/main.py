import asyncio
import json
import logging
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = "8779445142:AAHBA31vdbdQUJgNrOHZJ6pTXYnn-sF-5q4"
WEBAPP_URL = "https://pashamix.github.io/my-tg-shop/index.html" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КОРС НАСТРОЙКИ ДЛЯ БРАУЗЕРА ---
async def handle_get_products(request):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price, image_url FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    products = [{"name": r[0], "description": r[1], "price": r[2], "image": r[3]} for r in rows]
    return web.json_response(products, headers={"Access-Control-Allow-Origin": "*"})

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Відкрити магазин", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("👋 Ласкаво просимо! Натисніть кнопку нижче для входу в магазин.", reply_markup=markup)

@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        cart = data.get("cart", [])
        total = data.get("total", 0)
        
        order_text = "🎉 **Нове замовлення прийнято!**\n\n"
        for item in cart:
            order_text += f"• {item['name']} x{item['quantity']} — {item['price'] * item['quantity']} грн\n"
        order_text += f"\n💰 **Разом: {total} грн**"
        
        await message.answer(order_text, parse_mode="Markdown")
    except Exception:
        await message.answer("Помилка оформлення.")

# --- ЗАПУСК БОТА И API ПАРАЛЛЕЛЬНО ---
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Запускаем локальный веб-сервер на порту 8080 для отдачи товаров
    app = web.Application()
    app.router.add_get('/api/products', handle_get_products)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    asyncio.create_task(site.start())
    print("🔗 API товаров запущено на http://localhost:8080/api/products")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())