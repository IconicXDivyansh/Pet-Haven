from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, Event, Registration
from forms import RegistrationForm, LoginForm, EventForm, RegistrationEventForm
from config import Config
import os
from werkzeug.utils import secure_filename
from datetime import datetime



app = Flask(__name__)
app.config.from_object(Config)


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create database tables
with app.app_context():
    db.create_all()
    # Hardcoded Admin
    if not User.query.filter_by(email="admin@example.com").first():
        hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
        admin = User(username="admin", email="admin@example.com", password=hashed_pw, is_admin=True)
        db.session.add(admin)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()  #Check if email exists
        if existing_user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('login'))  # Redirect to login if email exists
        
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)




@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check credentials.', 'danger')
    return render_template('login.html', form=form)



@app.route('/competitions')
@login_required
def competitions():
    if current_user.is_admin:
        return render_template('admin_dashboard.html', events=Event.query.all())
    
    events = Event.query.all()
    registered_events = Registration.query.filter_by(user_id=current_user.id).all()
    
    registered_event_details = []
    for reg in registered_events:
        event = Event.query.get(reg.event_id)
        if event:
            registered_event_details.append(event)

    return render_template('user_dashboard.html', events=events, registered_events=registered_event_details)
    # return render_template('user_dashboard.html', events=Event.query.all(), registered_events=registered_events)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("discover[team2].html", events=Event.query.all())

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if not current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    form = EventForm()  
    if form.validate_on_submit():
        image_filename = "default.png"
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            form.image.data.save(image_path)

        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            prizes=form.prizes.data,
            eligibility=form.eligibility.data,
            fee=form.fee.data,
            image_filename=image_filename 
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))  #Redirect after adding event
    return render_template('add_event.html', form=form)
    
    

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = RegistrationEventForm()

    if form.validate_on_submit():
        registration = Registration(
            user_id=current_user.id,
            event_id=event_id,
            pet_name=form.pet_name.data,
            pet_type=form.pet_type.data,
            pet_age=form.pet_age.data,
            paid=False  # Assuming payment is done later
        )
        db.session.add(registration)
        db.session.commit()
        flash('Successfully registered!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register_event.html', form=form, event=event)



@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))  # Restrict non-admin users
    events = Event.query.all()  #  Fetch all events
    return render_template('admin_dashboard.html', events=events)

@app.route('/registrations')
@login_required
def registrations():
    registered_events = db.session.query(Registration, Event).join(Event, Registration.event_id == Event.id).filter(Registration.user_id == current_user.id).all()
    
    # Convert event dates to datetime objects for comparison
    current_date = datetime.now().date()
    processed_events = []
    for reg, event in registered_events:
        event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
        can_edit = event_date > current_date
        processed_events.append((reg, event, can_edit))
    
    return render_template("registrations.html", registered_events=processed_events)

@app.route('/edit_registration/<int:registration_id>', methods=['GET', 'POST'])
@login_required
def edit_registration(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    event = Event.query.get_or_404(registration.event_id)
    
    # Check if the registration belongs to the current user
    if registration.user_id != current_user.id:
        flash('You are not authorized to edit this registration.', 'danger')
        return redirect(url_for('registrations'))
    
    # Check if the event date has passed
    event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
    if event_date < datetime.now().date():
        flash('Cannot edit registration for past events.', 'warning')
        return redirect(url_for('registrations'))
    
    form = RegistrationEventForm()
    
    if form.validate_on_submit():
        registration.pet_name = form.pet_name.data
        registration.pet_type = form.pet_type.data
        registration.pet_age = form.pet_age.data
        
        try:
            db.session.commit()
            flash('Registration details updated successfully!', 'success')
            return redirect(url_for('registrations'))
        except:
            db.session.rollback()
            flash('An error occurred while updating the registration.', 'danger')
    
    # Pre-fill form with current values
    if request.method == 'GET':
        form.pet_name.data = registration.pet_name
        form.pet_type.data = registration.pet_type
        form.pet_age.data = registration.pet_age
    
    return render_template('edit_registration.html', form=form, registration=registration, event=event)

@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")






@app.route('/pay/<int:registration_id>', methods=['GET', 'POST'])
@login_required
def pay_fee(registration_id):
    registration = Registration.query.get_or_404(registration_id)

    if registration.user_id != current_user.id:
        abort(403)  # Prevent unauthorized access

    registration.paid = True
    db.session.commit()

    flash("Payment successful!", "success")
    return redirect(url_for('registrations'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('you have been logged out.','info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
