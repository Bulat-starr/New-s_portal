from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('main_page.html')