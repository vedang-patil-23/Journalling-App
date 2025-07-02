from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    entries = db.relationship('JournalEntry', backref='user', lazy=True)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    mood = db.Column(db.String(50))  # e.g., Happy, Sad, Neutral, Excited, Anxious
    tags = db.Column(db.String(255))  # Comma-separated tags
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def index():
    search_query = request.args.get('search', '')
    filter_mood = request.args.get('mood', 'all')
    filter_tag = request.args.get('tag', '')
    filter_date_str = request.args.get('date', '')

    entries_query = JournalEntry.query.filter_by(user_id=current_user.id)

    if search_query:
        entries_query = entries_query.filter(
            (JournalEntry.title.ilike(f'%{search_query}%')) |
            (JournalEntry.content.ilike(f'%{search_query}%'))
        )
    if filter_mood != 'all':
        entries_query = entries_query.filter_by(mood=filter_mood)
    if filter_tag:
        entries_query = entries_query.filter(JournalEntry.tags.ilike(f'%{filter_tag}%'))
    if filter_date_str:
        try:
            filter_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
            entries_query = entries_query.filter_by(entry_date=filter_date)
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')

    entries = entries_query.order_by(JournalEntry.entry_date.desc(), JournalEntry.created_at.desc()).all()
    return render_template('index.html', entries=entries, search_query=search_query, filter_mood=filter_mood, filter_tag=filter_tag, filter_date=filter_date_str)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        entry_date_str = request.form.get('entry_date', str(date.today()))
        mood = request.form.get('mood')
        tags = request.form.get('tags', '')
        
        try:
            entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)

        entry = JournalEntry(title=title, content=content, entry_date=entry_date, mood=mood, tags=tags, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry added successfully!')
        return redirect(url_for('index'))
    return render_template('add_entry.html', today_date=date.today().strftime('%Y-%m-%d'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to edit this entry', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        entry_date_str = request.form.get('entry_date')
        entry.mood = request.form.get('mood')
        entry.tags = request.form.get('tags', '')

        try:
            entry.entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)

        db.session.commit()
        flash('Journal entry updated successfully!')
        return redirect(url_for('view_entry', id=entry.id))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Journal entry deleted successfully!')
    return redirect(url_for('index'))

@app.route('/view/<int:id>')
@login_required
def view_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to view this entry', 'danger')
        return redirect(url_for('index'))
    return render_template('view_entry.html', entry=entry)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', current_year=datetime.utcnow().year)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004) 