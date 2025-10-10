from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('resume'))

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    message = None
    if request.method == 'POST':
        name = request.form.get('name')
        message = f"Дякую, {name}! Я отримала твоє повідомлення 💌"
    return render_template('contacts.html', title='Контакти', message=message)

if __name__ == '__main__':
    app.run(debug=True)
