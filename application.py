from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QDialog, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
import requests
import sqlite3
import re


app = QApplication([])
window = QWidget()
window.resize(1300, 800)
window.setWindowTitle('Приложение Арины и Полины')

main_layout = QHBoxLayout()
v_layout1 = QVBoxLayout()
v_layout2 = QVBoxLayout()
v_layout3 = QVBoxLayout()

l_dish = QLabel('Список блюд:')
l_dish.setFont(QFont('Arial', 14))
list_dish = QListWidget()

v_layout1.addWidget(l_dish)
v_layout1.addWidget(list_dish)

l_image = QLabel('Картинка')
pixmap = QPixmap('default_photo.jpg')
image = pixmap.scaled(400, 300)
l_image.setPixmap(image)

l_products_delivery = QLabel('Продукты на доставку:')
l_products_delivery.setFont(QFont('Arial', 14))
list_products = QListWidget()
l_ingredients = QLabel('Введите недостающие ингредиенты:')
l_ingredients.setFont(QFont('Arial', 14))
product_input = QLineEdit()
product_input.setFont(QFont('Arial', 12))


v_layout2.addWidget(l_image)
v_layout2.addWidget(l_products_delivery)
v_layout2.addWidget(list_products)
v_layout2.addWidget(l_ingredients)
v_layout2.addWidget(product_input)

l_recipe = QLabel('Рецепт:')
l_recipe.setFont(QFont('Arial', 14))
list_recipe = QListWidget()
l_list_ingredients = QLabel('Ингредиенты:')
l_list_ingredients.setFont(QFont('Arial', 14))
list_ingredients = QListWidget()

h_layout4 = QHBoxLayout()

btn_add = QPushButton('Добавить')
btn_add.setFont(QFont('Arial', 9))
btn_delivery = QPushButton('Сформировать заказ')
btn_delivery.setFont(QFont('Arial', 9))

v_layout3.addWidget(l_recipe)
v_layout3.addWidget(list_recipe)
v_layout3.addWidget(l_list_ingredients)
v_layout3.addWidget(list_ingredients)
h_layout4.addWidget(btn_add, alignment=(Qt.AlignLeft| Qt.AlignBottom))
h_layout4.addWidget(btn_delivery, alignment=(Qt.AlignRight | Qt.AlignBottom))

v_layout3.addLayout(h_layout4)

main_layout.addLayout(v_layout1)
main_layout.addLayout(v_layout2)
main_layout.addLayout(v_layout3)

window.setLayout(main_layout)

conn = sqlite3.connect('eda.db')
cursor = conn.cursor()

cursor.execute('SELECT name_dish FROM recipes')
dishes = cursor.fetchall()

for dish in dishes:
    item = f'{dish[0]}'
    list_dish.addItem(item)


def get_ingredients_dish(dish_name: str):
    list_ingredients.clear()
    cursor.execute("SELECT id FROM recipes WHERE name_dish = ?", (dish_name,))
    result = cursor.fetchone()
    dish_id = result[0]
    cursor.execute("SELECT name_ingredients FROM ingredients WHERE recipe_id = ?", (dish_id,))
    ingredients = cursor.fetchall()
    ingredient_list = [ingredient[0] for ingredient in ingredients]
    for ingredient in ingredients:
        item = f'{ingredient[0]}'
        list_ingredients.addItem(item)

def get_image_dish(dish_name):
    cursor.execute(f"SELECT photo_dish FROM recipes WHERE name_dish = ?", (dish_name,))
    dishes = cursor.fetchall()
    for dish in dishes:
        url = f'{dish[0]}'
        response = requests.get(url)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        image = pixmap.scaled(400, 300)
        l_image.setPixmap(image)


def get_recipe_dish():
    list_recipe.clear()
    dish_name = list_dish.selectedItems()[0].text()
    cursor.execute(f"SELECT manual FROM recipes WHERE name_dish = ?", (dish_name,))
    resipes = cursor.fetchall()
    for recipe in resipes:
        item = f'{recipe[0]}'
        list_recipe.addItem(item)
    get_ingredients_dish(dish_name)
    get_image_dish(dish_name)

def get_product():
    product_name = list_products_delivery.selectedItems()[0].text()
    list_products.addItem(product_name)
    product_input.clear()
    win_delivery_products.close()


def get_products_delivery():
    global list_products_delivery
    global win_delivery_products
    win_delivery_products = QDialog()
    win_delivery_products.setWindowTitle("Выбор продукта")
    win_delivery_products.resize(400, 400)
    list_products_delivery = QListWidget()
    v_layout4 = QVBoxLayout()
    v_layout4.addWidget(list_products_delivery)
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM products')
    dirty_list_products = cursor.fetchall()
    products = [f'{product[0]}' for product in dirty_list_products]
    for prod in products:
        if list_ingredients.selectedItems()[0].text().title() in prod:
            list_products_delivery.addItem(prod)
    win_delivery_products.setLayout(v_layout4)
    win_delivery_products.show()
    list_products_delivery.itemClicked.connect(get_product)
    win_delivery_products.exec_()

def add_ingredient_for_delivery():
    global list_products_delivery
    global win_delivery_products
    win_delivery_products = QDialog()
    win_delivery_products.setWindowTitle("Выбор продукта")
    win_delivery_products.resize(400, 400)
    list_products_delivery = QListWidget()
    v_layout4 = QVBoxLayout()
    v_layout4.addWidget(list_products_delivery)
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM products')
    dirty_list_products = cursor.fetchall()
    products = [f'{product[0]}' for product in dirty_list_products]
    for prod in products:
        if product_input.text().title() in prod:
            list_products_delivery.addItem(prod)
    win_delivery_products.setLayout(v_layout4)
    win_delivery_products.show()
    list_products_delivery.itemClicked.connect(get_product)
    win_delivery_products.exec_()

def show_window_delivery():
    QMessageBox.information(None, "Состояние заказа", "Заказ оформлен!")

def create_list_product_delivery():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    win_delivery_products2 = QDialog()
    win_delivery_products2.setWindowTitle("Доставка продуктов")
    win_delivery_products2.resize(400, 400)
    list_products_delivery2 = QListWidget()
    l_price = QLabel('Сумма доставки:')
    btn_order = QPushButton('Заказать')
    v_layout5 = QVBoxLayout()
    v_layout5.addWidget(list_products_delivery2)
    v_layout5.addWidget(l_price)
    v_layout5.addWidget(btn_order, alignment=(Qt.AlignRight | Qt.AlignBottom))
    
    list_prices = []
    item_count = list_products.count()
    total_price = 0
    for i in range(item_count):
        product = list_products.item(i).text()
        cursor.execute(f"SELECT price FROM products WHERE name = ?", (product,))
        prices = cursor.fetchall()
        list_products_delivery2.addItem(product)
        list_prices.append(prices)
    for price in range(len(prices)):
        pattern = r'\d+'  
        match = re.search(pattern, list_prices[price][0][0])
        number = int(match.group())
        total_price += int(number)
    l_price.setText(f'Сумма доставки: {total_price} руб')
    l_price.setFont(QFont('Arial', 14))
    win_delivery_products2.setLayout(v_layout5)
    win_delivery_products2.show()
    btn_order.clicked.connect(show_window_delivery)
    win_delivery_products2.exec_()

    


list_dish.itemClicked.connect(get_recipe_dish)

list_ingredients.itemClicked.connect(get_products_delivery)

btn_add.clicked.connect(add_ingredient_for_delivery)

btn_delivery.clicked.connect(create_list_product_delivery)

window.show()
app.exec_()

