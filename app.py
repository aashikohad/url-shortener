from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500))
    short_code = db.Column(db.String(10), unique=True)

# Generate short code
def generate_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Home page
@app.route('/', methods=['GET','POST'])
def index():
    short_url = None
    
    if request.method == 'POST':
        long_url = request.form['url']
        
        code = generate_code()
        
        new_url = URL(long_url=long_url, short_code=code)
        db.session.add(new_url)
        db.session.commit()
        
        short_url = request.host_url + code
    
    return render_template('index.html', short_url=short_url)

# Redirect route
@app.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first()
    
    if url:
        return redirect(url.long_url)
    
    return "URL not found"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
   app.run(host="0.0.0.0", port=10000)
