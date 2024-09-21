from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return  render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/segmentation')
def  segmentation():
    return render_template('segmentation.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__=='__main__':
    app.run(debug=True)