from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time
from scheduler import generate_knapsack_schedule  # ⬅️ Import your scheduler

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '--'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------------- Models ---------------------- #
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    subjects = db.relationship('Subject', backref='user', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    days_left = db.Column(db.Integer, nullable=False)
    total_units = db.Column(db.Integer, nullable=False)
    completed_units = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, nullable=False)
    complexity = db.Column(db.Integer, nullable=False)

    @property
    def progress_percent(self):
        if self.total_units > 0:
            return round((self.completed_units / self.total_units) * 100, 1)
        return 0.0

    @property
    def priority_label(self):
        return {1: 'Highest', 2: 'High', 3: 'Medium', 4: 'Low', 5: 'Lowest'}.get(self.priority, 'Unknown')

    @property
    def complexity_label(self):
        return {1: 'Very Easy', 2: 'Easy', 3: 'Medium', 4: 'Hard', 5: 'Very Hard'}.get(self.complexity, 'Unknown')

class TimetableSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    subject = db.relationship('Subject')

# ---------------------- Auth ---------------------- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))

        try:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ---------------------- Pages ---------------------- #
@app.route('/dashboard')
@login_required
def dashboard():
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    overall_progress = round(
        sum(subject.progress_percent for subject in subjects) / len(subjects), 1
    ) if subjects else 0
    return render_template('dashboard.html', username=current_user.username, overall_progress=overall_progress)

@app.route('/subjects')
@login_required
def subjects():
    user_subjects = Subject.query.filter_by(user_id=current_user.id).all()
    return render_template('subjects.html', subjects=user_subjects)

@app.route('/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        try:
            new_subject = Subject(
                user_id=current_user.id,
                name=request.form.get('name'),
                days_left=request.form.get('days_left'),
                total_units=request.form.get('total_units'),
                priority=request.form.get('priority'),
                complexity=request.form.get('complexity')
            )
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            return redirect(url_for('subjects'))
        except Exception:
            db.session.rollback()
            flash('Error adding subject. Please check your inputs.', 'danger')
    return render_template('add_subject.html')

@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('subjects'))
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully.", "success")
    return redirect(url_for('subjects'))

@app.route('/progress', methods=['GET', 'POST'])
@login_required
def progress():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        completed_units = request.form.get('completed_units')
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        if subject:
            try:
                subject.completed_units = min(int(completed_units), subject.total_units)
                db.session.commit()
                flash('Progress updated successfully!', 'success')
            except ValueError:
                flash('Invalid input. Please enter a valid number.', 'danger')
        return redirect(url_for('progress'))

    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    overall_progress = round(
        sum(s.progress_percent for s in subjects) / len(subjects), 1
    ) if subjects else 0
    return render_template("progress.html", subjects=subjects, overall_progress=overall_progress)

@app.route('/pomodoro')
@login_required
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/pomodoro/<subject_name>')
@login_required
def pomodoro_subject(subject_name):
    return render_template('pomodoro.html', subject_name=subject_name)

# ---------------------- Timetable ---------------------- #
@app.route('/timetable')
@login_required
def timetable():
    sessions = TimetableSession.query.filter_by(user_id=current_user.id).order_by(
        TimetableSession.date, TimetableSession.start_time
    ).all()
    return render_template('timetable.html', timetable=sessions)

@app.route('/generate_timetable')
@login_required
def generate_timetable():
   

    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    if not subjects:
        flash("Add subjects before generating a timetable.", "warning")
        return redirect(url_for('subjects'))

    # Clear previous sessions
    TimetableSession.query.filter_by(user_id=current_user.id).delete()

    start_date = datetime.now().date()
    max_days_left = max(subject.days_left for subject in subjects)

    for i in range(max_days_left):
        current_date = start_date + timedelta(days=i)
        current_time = time(9, 0)
        total_minutes = 6 * 60  # 6 hours/day = 360 minutes available

        # Generate daily schedule using knapsack
        daily_schedule = generate_knapsack_schedule(subjects, total_minutes)

        for item in daily_schedule:
            subject = item['subject']
            duration = item['duration']

            end_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=duration)).time()

            session = TimetableSession(
                user_id=current_user.id,
                subject_id=subject.id,
                date=current_date,
                start_time=current_time,
                end_time=end_time,
                duration=duration
            )
            db.session.add(session)

            # 15-minute break between sessions
            current_time = (datetime.combine(datetime.today(), end_time) + timedelta(minutes=15)).time()

    db.session.commit()
    flash("Timetable generated successfully for all days until your exams!", "success")
    return redirect(url_for('timetable'))


# ---------------------- Run ---------------------- #
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
