from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

saved_locations = db.Table('saved_locations',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('location_id', db.Integer, db.ForeignKey('location.id'), primary_key=True)
                           )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    my_locations = db.relationship('Location', secondary=saved_locations,
                                   backref=db.backref('saved_locations', lazy='dynamic'),
                                   lazy='dynamic')

    def save_location(self, location):
        if not self.has_saved(location):
            self.my_locations.append(location)

    def remove_location(self, location):
        if self.has_saved(location):
            self.my_locations.remove(location)

    def has_saved(self, location):
        return self.my_locations.filter(
            saved_locations.c.location_id == location.id).count() > 0

    def show_saved_locations(self):
        return self.my_locations

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))

    def __repr__(self):
        return '<Location {}'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
