import sqlite3

def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    
    # Создаем таблицу товаров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image_url TEXT
        )
    ''')
    
    # Очищаем старое (для теста) и добавляем актуальные товары
    cursor.execute('DELETE FROM products')
    
    products = [
        (
            "Hatsan FlashPup-S Set (4.5мм)",
            "Комплект із насосом та прицілом 4x32. PCP-система, компонування Bullpup. Спортивно-розважальна стрільба (18+).",
            18500,
            "https://placehold.co"  # Заглушка для фото
        ),
        (
            "Crosman C11 (4.5мм)",
            "Компактний пневматичний пістолет на балонах CO2. Початкова швидкість 146 м/с. Місткість магазину: 18 кульок BB.",
            3200,
            "https://placehold.co"
        ),
        (
            "Beeman Longhorn (4.5мм)",
            "Пружинно-поршнева гвинтівка з оптичним прицілом 4х32 в комплекті. Ергономічний приклад із вирізом для великого пальця.",
            6900,
            "https://placehold.co"
        )
    ]
    
    cursor.executemany('INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)', products)
    conn.commit()
    conn.close()
    print("🚀 База данных shop.db успешно создана и наполнена 3 товарами!")

if __name__ == '__main__':
    init_db()
