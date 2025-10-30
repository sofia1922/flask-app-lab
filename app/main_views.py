from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import logging
from .forms import ContactForm

main_bp = Blueprint('main', __name__)

logging.basicConfig(filename='contacts.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@main_bp.route('/')
def home():
    return redirect(url_for('main.resume'))

@main_bp.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "subject": form.subject.data,
            "message": form.message.data
        }

        logging.info(f"{data['name']} ({data['email']}, {data['phone']}) → {data['subject']}: {data['message']}")
        session['last_contact'] = data
        flash(f"Дякую, {data['name']}! Повідомлення успішно відправлено 💌", "success")
        return redirect(url_for('.contacts'))

    if request.method == 'POST' and not form.validate():
        flash("Будь ласка, перевірте правильність заповнення полів.", "danger")

    return render_template('contacts.html', form=form, title='Контакти')