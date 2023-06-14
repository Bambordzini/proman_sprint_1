from flask import Flask, render_template, url_for, request, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mimetypes
import queries

mimetypes.add_type('application/javascript', '.js')
app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # replace with your database URI
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return 'Invalid username or password'
        login_user(user)
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# The rest of your routes...
def main():
    with app.app_context():
        db.create_all()  # Creates the database tables
    app.run(debug=True)

if __name__ == '__main__':
    main()
