import unittest
from app import app, db
from app.models import User, Location


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_save_locations(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four locations
        l1 = Location(name='supermarket')
        l2 = Location(name='university')
        l3 = Location(name='gym')
        l4 = Location(name='stadium')
        db.session.add_all([l1, l2, l3, l4])
        db.session.commit()

        # setup saved locations

        u1.save_location(l1)    # john save supermarket
        u1.save_location(l2)    # john save university
        u2.save_location(l3)    # susan save gym
        u3.save_location(l4)    # mary save stadium
        db.session.commit()

        # check the saved locations of each user
        sl1 = u1.show_saved_locations().all()
        sl2 = u2.show_saved_locations().all()
        sl3 = u3.show_saved_locations().all()
        sl4 = u4.show_saved_locations().all()
        self.assertEqual(sl1, [l1, l2])
        self.assertEqual(sl2, [l3])
        self.assertEqual(sl3, [l4])
        self.assertEqual(sl4, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
