from flask import Flask, render_template, redirect, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretki'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/prodzekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    name = db.Column(db.String(100))
    cards = db.relationship('Card', backref='board', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        boards = Board.query.filter_by(user_id=current_user.id).all() 
    else:
        boards = []
    return render_template('home.html', boards=boards)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                flash('Incorrect password.')
                return render_template('login.html')
        else:
            flash('Username does not exist.')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            return redirect('/')
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/create_board', methods=['POST'])
@login_required
def create_board():
    title = request.form.get('title') 

    if title: 
        new_board = Board(name=title, user_id=current_user.id) 
        db.session.add(new_board)
        db.session.commit() 

        flash('New board has been created.') 
        return redirect('/') 
    else:
        flash('Title cannot be empty.') 
        return redirect('/') 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
