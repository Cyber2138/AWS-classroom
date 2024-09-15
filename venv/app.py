from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import boto3
from config import Config
from Automation_scripts.automation import upload_to_s3
from logs.cloudwatch_logger import log_to_cloudwatch

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database model for users (already exists)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = username
            log_to_cloudwatch('virtual_classroom_logs', 'login_stream', f"{username} logged in")
            return redirect(url_for('course'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/course')
def course():
    if 'user' in session:
        return render_template('courses.html')
    else:
        flash('You must be logged in to view this page', 'warning')
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'user' in session:
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('course'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('course'))

        # Upload file to S3
        message = upload_to_s3(file.filename, app.config['S3_BUCKET'])
        flash(message, 'info')
        return redirect(url_for('course'))
    else:
        flash('You must be logged in to upload files', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
