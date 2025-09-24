from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

bp = Blueprint('main', __name__)

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

    return render_template('main_page.html')