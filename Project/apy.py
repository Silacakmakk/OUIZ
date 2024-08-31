from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Güvenlik için rastgele bir anahtar belirleyin

# Veritabanı ayarları
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Veritabanı modelini tanımla
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

# Ana sayfa rotası
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('quiz'))
    return render_template('index.html')

# Quiz rotası
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        score = 0
        if request.form.get('question1') == 'correct':
            score += 25
        if request.form.get('question2') == 'correct':
            score += 25
        if request.form.get('question3') == 'correct':
            score += 25
        if request.form.get('question4') == 'correct':
            score += 25

        user = User.query.get(session['user_id'])
        user.score = score
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('quiz.html')

# Uygulamayı çalıştır
if __name__ == '__main__':
    # Veritabanı tablolarını oluştur
    with app.app_context():
        db.create_all()
    app.run(debug=True)
