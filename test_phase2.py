import unittest
from app import create_app
from extensions import db
from models.user import User

class Phase2Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_1_registration(self):
        res = self.client.post('/auth/register', data={
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'college': 'Test College',
            'department': 'CS',
            'academic_year': 'Junior',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Your account has been created', res.data)
        
    def test_2_duplicate_registration(self):
        self.client.post('/auth/register', data={
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        res_dup = self.client.post('/auth/register', data={
            'full_name': 'Test User2',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Email is already registered', res_dup.data)

    def test_3_login_and_logout(self):
        with self.app.app_context():
            user = User(full_name='Test', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
        res = self.client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b'Dashboard', res.data)
        
        res_logout = self.client.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', res_logout.data)

    def test_4_invalid_login(self):
        with self.app.app_context():
            user = User(full_name='Test', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
        res_invalid = self.client.post('/auth/login', data={'email': 'test@example.com', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b'Invalid email or password', res_invalid.data)

    def test_5_protected_routes(self):
        res = self.client.get('/student/dashboard', follow_redirects=True)
        self.assertIn(b'Sign in', res.data)
        
    def test_6_profile_update(self):
        with self.app.app_context():
            user = User(full_name='Test', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
        self.client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
        
        res = self.client.post('/student/profile', data={
            'full_name': 'Updated Name',
            'phone': '0987654321',
            'college': 'New College',
            'department': 'IT',
            'academic_year': 'Senior'
        }, follow_redirects=True)
        self.assertIn(b'Profile updated successfully', res.data)
        
        with self.app.app_context():
            updated_user = User.query.filter_by(email='test@example.com').first()
            self.assertEqual(updated_user.full_name, 'Updated Name')

if __name__ == '__main__':
    unittest.main()
