from app import app, db
from app.forms import LoginForm, RegistrationForm, EmptyForm, ResetPasswordRequestForm, ResetPasswordForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Location
from werkzeug.urls import url_parse
from app.email import send_password_reset_email
import json


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='About E-City')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, title='E-CITY User')


@app.route('/save/<location_name>', methods=['POST'])
@login_required
def save(location_name):
    form = EmptyForm()
    if form.validate_on_submit():
        location = Location.query.filter_by(name=location_name).first()
        if location is None:
            flash('Location {} not found.'.format(location_name))
            return redirect(url_for('index'))
        current_user.save_location(location)
        db.session.commit()
        flash('You have saved {}!'.format(location_name))
        return redirect(url_for('explore'))  # redirect to explore page
    else:
        return redirect(url_for('index'))


@app.route('/remove/<location_name>', methods=['POST'])
@login_required
def remove(location_name):
    form = EmptyForm()
    if form.validate_on_submit():
        location = Location.query.filter_by(name=location_name).first()
        if location is None:
            flash('Location {} not found.'.format(location_name))
            return redirect(url_for('index'))
        current_user.remove_location(location)
        db.session.commit()
        flash('You have removed {}'.format(location_name))
        return redirect(url_for('location', location_name=location.name))  # redirect to location page
    else:
        return redirect(url_for('index'))


@app.route('/location/<location_name>')
@login_required
def location(location_name):
    location = Location.query.filter_by(name=location_name).first_or_404()
    form = EmptyForm()
    return render_template('location.html', location=location, form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    return render_template('explore.html');


@app.route('/process_data', methods=['POST'])
@login_required
def process_data():
    data = request.get_json()
    print(data)
    response = {
        "name": None,
        "exists": 0
    }
    #   query to know if user is in a location range, accuracy = 0.000005
    #   calculate user geolocation range
    #   minLongitudeUser = data["longitude"] - 0.000005
    #   maxLongitudeUser = data["longitude"] + 0.000005
    #   minLatitudeUser = data["latitude"] - 0.000005
    #   maxLatitudeUser = data["latitude"] + 0.000005

    #   query to get the nearest location from user if it exists according to accuracy parameter
    #   location = Location.query.filter(Location.latitude >= minLatitudeUser,
    #                                    Location.latitude <= maxLatitudeUser,
    #                                    Location.longitude >= minLongitudeUser,
    #                                 Location.longitude <= maxLongitudeUser).first()

    lat = data[0]["latitude"]
    lon = data[1]["longitude"]
    location = Location.query.filter_by(latitude=lat, longitude=lon).first()

    #   send response to user in either case
    if location:
        response["name"] = location.name
        response["exists"] = 1

    return jsonify(response)


@app.route('/process_location/<location_name>', methods=['POST'])
@login_required
def process_location(location_name):
#    data = request.get_json()
#    print(data)

#    if data["notInterested"]:
#        return None

#    location_name = data["name"]
    return redirect(url_for('location', location_name=location_name))


@app.route('/get_saved_locations/<username>', methods=['GET', 'POST'])
@login_required
def get_saved_locations(username):
    #   get user saved locations
    user = User.query.filter_by(username=username).first()
    user.show_saved_locations()
    locations = user.get_saved_locations()

    response = []
    dummy = {}

    for location in locations:
        dummy["longitude"] = location.longitude
        dummy["latitude"] = location.latitude
        dummy["name"] = location.name
        dummy["body"] = location.body
        dummy["address"] = location.address
        dummy["city"] = location.city
        dummy["country"] = location.country

        response.append(dummy)
    return jsonify(response)
