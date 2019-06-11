import unittest
from flask import current_app
from app.models import Permission
from app import create_app, db
from app.models import User, Role, AnonymousUser
from app.email import send_email
from flask_login import current_user, login_user
'''
В тестах используется пакет unittest из стандартной библиотеки
Python. Методы setUp() и tearDown() выполняются до и после каждого
теста, а любые методы с именами, начинающимися с префикса test_,
выполняются как тесты.
Метод setUp() пытается создать окружение для теста, близко напо-
минающее действующее приложение. Сначала он создает экземпляр
приложения, настроенный для тестирования, и активирует его кон-
текст . Этот шаг гарантирует доступность current_app для теста. Затем
он создает новую базу данных, которая может использоваться теста-
ми. База данных и контекст удаляются в методе tearDown().
Первый тест проверяет наличие экземпляра приложения. Второй
убеждается, что приложение выполняется с настройками для тести-
рования.
'''
class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)


    def test_token_confirmation(self):
        user = User.query.filter_by(email='twichmail@inbox.ru').first()
        db.session.delete(user)
        db.session.commit()
        user = User(email='prokaeser@mail.ru',
                 username='qwe',
                 password='qwe')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
                   user=user, token=token)
        login_user(user)
        if current_user.confirm(token):
            print('True')
        else:
            print('False')

    '''
    def test_roles_and_permissions(self):
        Role.insert_roles()
        user = User(email='twichmail1@inbox.ru',
                    username='qwe12',
                    password='qwe12')
        self.assertTrue(user.can(Permission.WRITE_ARTICLES))
        self.assertFalse(user.can(Permission.MODERATE_COMMENTS))
    '''
    def test_admin_role(self):
        user = User.query.filter_by(email='appleid292@gmail.com').first()
        self.assertTrue(user.can(Permission.ADMINISTER))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))


