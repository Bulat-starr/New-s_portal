import random

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, make_response

bp = Blueprint('main', __name__)

heading = "Lorem ipsum dolor sit amet"

content = """
Loren ipsum dolor sit amet consectetur adipisicing elit.
Repellat inventore assumenda laboriosam,
obcaecati saepe pariatur atque est? Quam, molestias nisi.
"""

posts = 200
quantity = 10
db = list()

for x in range(posts):
    headingParts = heading.split(" ")
    random.shuffle(headingParts)

    contentParts = content.split(" ")
    random.shuffle(contentParts)

    db.append([x, " ".join(headingParts), " ".join(contentParts)])

@bp.route('/')
def index():
    """
        Обработчик главной страницы приложения.

        Returns:
            Response: HTML страница, отрендеренная из шаблона main_page.html

        Functionality:
            - Отображает главную страницу новостного агрегатора
            - В будущем здесь будет передаваться список новостей в шаблон
            - Подготавливается для добавления пагинации и фильтров

        Template: main_page.html
        Methods: GET only
        """

    return render_template('index.html')



@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/news')
def main_page():
    return render_template("main_page.html")

@bp.route('/news/load')
def load():

    res = make_response(jsonify([]), 400)

    if request.args:
        counter = int(request.args.get("c"))
        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            res = make_response(jsonify(db[0:quantity]), 200)
        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify([]), 200)
        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            res = make_response(jsonify(db[counter:counter + quantity]), 200)
    return res

