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
    counter = int(request.args.get("c", 0))
    print(f"запрос новостей с counter: {counter}")

    if counter >= len(db):
        return make_response(jsonify([]), 200)

    end_index = min(counter + quantity, len(db))
    posts_chunk = db[counter:end_index]
    return make_response(jsonify(posts_chunk), 200)

