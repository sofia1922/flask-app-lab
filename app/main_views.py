from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('main.resume'))

@main_bp.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    message = None
    if request.method == 'POST':
        name = request.form.get('name')
        message = f"Дякую, {name}! Я отримала твоє повідомлення 💌"
    return render_template('contacts.html', title='Контакти', message=message)
