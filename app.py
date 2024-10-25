from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database
db = SQLAlchemy(app)

# Root route (index page)
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists! Please log in.', 'danger')
            return redirect(url_for('login'))

        # Create new user and hash the password
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user in (set session)
        session['username'] = username
        flash('Sign-up successful! Welcome!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email or not password:
            flash('Both email and password are required!', 'danger')
            return redirect(url_for('login'))

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'  # Replace with a strong secret key in production
    app.run(debug=True)
