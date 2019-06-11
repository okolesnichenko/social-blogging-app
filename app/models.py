import hashlib
from app import db
from app.exceptions import ValidationError
from flask import current_app, request, url_for
from flask_login import UserMixin, login_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from markdown import markdown
from time import time
import jwt
import bleach
'''
class User class Role
Переменная класса __tablename__ определяет имя таблицы в базе
данных. Расширение Flask-SQLAlchemy может автоматически при-
своить переменной __tablename__ имя таблицы по умолчанию, но при
выборе имен по умолчанию расширение не следует соглашению об
использовании множественного числа, поэтому лучше указывать
имена таблиц явно. Остальные переменные класса, объявленные как
экземпляры класса db.Column, – это атрибуты модели.

def generate_confirmation_token()
Пакет itsdangerous содержит несколько генераторов маркеров раз-
ных типов. Среди них имеется класс TimedJSONWebSignatureSerializer,
генерирующий веб-сигнатуры JSON (JSON Web Signatures, JWS)
с определенным сроком действия. Конструктор этого класса прини-
мает ключ шифрования, который в приложениях на основе Flask мо-
жет быть определен как параметр SECRET_KEY.
Метод dumps() генерирует цифровую подпись для данных, передан-
ных в аргументе, и затем сериализует данные с подписью в строковый
маркер. Аргумент expires_in определяет срок действия маркера в се-
кундах.
Расшифровка маркера выполняется методом loads() объекта
Serializer, который принимает маркер в виде единственного аргумен-
та. Функция проверяет сигнатуру и срок хранения и, если все в по-
рядке, возвращает исходные данные. Когда метод loads() получает
недопустимый маркер или определяет, что срок хранения истек, он
возбуждает исключение.

class Role
Поле default должно иметь значение True только для одной роли,
для остальных ролей оно должно быть установлено в значение False.
Роль по умолчанию (со значением True в поле default) – это роль, ко-
торая присваивается всем новым пользователям в процессе регистра-
ции.

@staticmethod
    def insert_roles():
Чтобы добавить новую роль или изменить набор привилегий для
имеющейся роли, внесите необходимые изменения в массив roles и
вызовите функцию.

def can(self, permissoins):
def is_administrator(self):
Чтобы упростить реализацию ролей и привилегий, в модель User
можно добавить вспомогательный метод, проверяющий наличие ука-
занной привилегии,
Метод can(), добавленный в модель User, выполняет операцию по-
разрядного И между проверяемыми привилегиями и привилегиями,
присвоенными роли. Если все проверяемые биты в роли установлены
в значение 1, метод возвращает True. Это означает, что пользователь
обладает всеми требуемыми привилегиями.

@login_manager.user_loader
def load_user(user_id):
Наконец, Flask-Login требует, чтобы приложение определило
функцию обратного вызова для загрузки информации о пользователе
по заданному идентификатору.

@staticmethod
    def generate_fake(count=100):
Адреса электронной почты и имена пользователей должны быть
уникальными, но, так как генераторы из ForgeryPy действуют доста-
точно случайно, есть вероятность создания дубликатов. В этих редких
ситуациях попытка подтвердить сеанс базы данных будет возбуждать
исключение IntegrityError. Обработчик этого исключения просто от-
катывает сеанс перед продолжением. Итерации цикла, сгенерировав-
шие повторяющиеся значения, не сохраняют информацию о пользо-
вателе в базу данных, поэтому общее число созданных фиктивных
пользователей может оказаться меньше запрошенного.

Преобразование разметки Markdown в разметку HTML можно
организовать в шаблоне _posts.html, но это неэффективно, так как
сообщения придется преобразовывать при каждом отображении
страницы. Чтобы избежать многократных преобразований, преобра-
зованную версию можно сохранять вместе с самим сообщением в мо-
мент его создания. Разметку HTML для отображения можно хранить
в новом поле модели Post, непосредственно доступном из шаблонов.
Оригинальный текст сообщений в формате Markdown также можно
сохранять в базе данных, на случай, если его потребуется отредакти-
ровать.
Функция on_changed_body регистрируется как обработчик собы-
тия «set» для поля body. Это означает, что она автоматически будет
вызываться при изменении поля body в любом экземпляре класса.
Функция создает HTML-версию сообщения и сохраняет ее в поле
body_html, обеспечивая тем самым автоматическое преобразование
разметки Markdown в разметку HTML.
Фактическое преобразование выполняется в три этапа. Сначала
с помощью функции markdown() выполняется начальное преобразо-
вание текста в разметку HTML. Затем результат со списком допус-
тимых тегов HTML передается функции clean(). Функция clean()
удаляет из разметки все теги, отсутствующие в «белом списке». В за-
ключение вызывается функция linkify(), предоставляемая фрейм-
ворком Bleach, которая преобразует адреса URL, присутствующие
в тексте, в правильно оформленные ссылки <a>. Этот последний этап
необходим, потому что автоматическое создание ссылок не преду-
сматривается спецификацией Markdown. PageDown поддерживает ее
как расширение, поэтому linkify() используется для совместимости.

ОТНОШЕНИЕ МНОГИЕ-КО-МНОГИМ
Отношение определяется с помощью все той же конструкции
db.relationship(), которая использовалась для определения отноше-
ний «один ко многим», но при определении отношений «многие ко
многим» необходимо добавлять аргумент secondary с объектом ассо-
циативной таблицы. Отношение можно определить в любом из двух
классов с аргументом backref, экспортирующим отношение с одной
стороны в другую. Ассоциативная таблица определяется как простая
таблица, а не как модель, потому что этой таблицей будет управлять
сам фреймворк SQLAlchemy.
Отношение classes использует семантику списка, что делает рабо-
ту с отношениями «многие ко многим», созданными таким способом,
чрезвычайно простой.

Отношения, в которых с обеих сторон находится одна и та же таб-
лица, называют самоссылочными (self-referential). В данном случае
сущностями слева являются пользователи, которые могут называть-
ся «читающими» («followers»). Сущностями справа также являются
пользователи, но они уже называются «читаемыми» («followed»).
Обычно при работе с отношения-
ми «многие ко многим» требуется хранить дополнительные данные, так
или иначе связанные с отношениями между двумя сущностями. Так,
для отношений между читающими и читаемыми может пригодиться
дата, когда один пользователь стал читающим другого, что позволит
сор тировать списки читающих в хронологическом порядке. Един-
ственное место, где может храниться такая информация, – ассоциатив-
ная таб лица, но в реализации, подобной той, что была показана выше,
в примере со студентами и предметами, ассоциативная таблица явля-
ется внут ренней, полностью управляемой фреймворком SQLAlchemy.
Чтобы получить возможность работать с дополнительными дан-
ными в отношениях, ассоциативную таблицу следует реализовать как
полноценную модель, доступную для приложения.

class Follow(db.Model):
    __tablename__='follows' + class User:
Здесь отношения followed и followers определены как отдельные
отношения «один ко многим». Обратите внимание, что с целью устра-
нения неоднозначности для каждого отношения потребовалось явно
указать, какой внешний ключ используется, добавив необязательный
именованный аргумент foreign_keys. Аргументы в вызове db.backref()
в этих отношениях применяются не друг к другу, а к модели Follow.
Аргумент lazy в вызовах db.backref() определяет, как выполняется
соединение. В режиме lazy='joined' связанные объекты извлекают-
ся немедленно из запроса соединения. Например, если пользователь
читает сотню других пользователей, вызов user.followed.all() вернет
список, содержащий 100 экземпляров Follow, каждый из которых бу-
дет иметь свойства follower и followed, ссылающиеся на соответствую-
щих пользователей. Режим lazy='joined' позволяет выполнять все
необходимые операции в единственном запросе к базе данных. Если
в аргументе lazy передать значение по умолчанию select, выборка
читающих и читаемых будет отложена до первого обращения, а для
установки каждого атрибута потребуется выполнить отдельный за-
прос, то есть для получения полного списка читаемых пользователей
понадобится выполнить 100 дополнительных запросов к базе данных.
Аргументы lazy в вызовах db.relationship() в обоих отношениях
преследуют иные цели. Они соответствуют стороне «один» и воз-
вращают списки со стороны «ко многим»; в режиме dynamic при обра-
щении к атрибутам отношений возвращаются объекты запросов, а не
сами данные, благодаря чему открывается возможность применить
дополнительные фильтры перед выполнением запроса.

@property 
def followed_posts(self):
Обратите внимание, что метод followed_posts() определен как
свойство (c помощью декоратора @property), благодаря чему отпадает
необходимость указывать скобки () при обращении к нему, и все от-
ношения получают единообразный синтаксис.
'''


# Констатнты привелегий
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Follow(db.Model):
    __tablename__='follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer) # Привелегии битовые стр 136

    def __repr__(self):
        return '<Role {}>'.format(self.name)
    # Отношение один ко многим
    users = db.relationship('User', backref='role')
    # Функция автозаполенния ролей
    @staticmethod
    def insert_roles():
        roles = {
            'User':(
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES, True),
            'Moderator':(Permission.FOLLOW |
                         Permission.COMMENT |
                         Permission.WRITE_ARTICLES |
                         Permission.MODERATE_COMMENTS, False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    # Отношение один ко многим
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Автоприсваивание ролей
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    # Шифрация пароля
    # @property - свойства типа геттеров и сеттеров
    @property
    def password(self):
        raise AttributeError('password is not readible attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Функция создания токена аутентификации в апи
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # Функция подтверждения токена аутентификации в апи
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def generate_confirmation_token(self, expires_in=3600):
        return jwt.encode(
                {'reset_password': self.id, 'exp': time() + expires_in},
                current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')



    def confirm(self, token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return False
        if id != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # Функция проверки прав доступа
    def can(self, permissoins):
        return self.role is not None and \
               (self.role.permissions & permissoins) == permissoins

    # Функция проверки прав доступа администратор
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # Функция обновления времени последнего онлайна
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # Функция создания URL аватара
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format\
            (url=url, hash=hash, size=size, default=default, rating=rating)

    # Функция генерации фоктивных данных
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            user = User(email=forgery_py.internet.email_address(),
                        username=forgery_py.internet.user_name(True),
                        password=forgery_py.lorem_ipsum.word(),
                        confirmed=True,
                        name=forgery_py.name.full_name(),
                        location=forgery_py.address.city(),
                        about_me=forgery_py.lorem_ipsum.sentence(),
                        member_since=forgery_py.date.date(True))
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    # Вспомогательный метод подписки
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    # Вспомогательный метод отписки
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    # Вспомогательный метод проверки подписчика
    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    # Вспомогательный метод проверки подписок
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_since': self.last_seen,
            'posts': url_for('api.get_user_posts', id = self.id, _external=True),
            'followed_posts':url_for('api.get_user_followed_posts', id = self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, olvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'), tags=allowed_tags, strip=True))

    # Функция генерации фоктивных данных
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            # Offset - Этот фильтр отбрасывает указанное число результатов.
            user = User.query.offset(randint(0, user_count-1)).first()
            post = Post(body=forgery_py.lorem_ipsum.sentence(),
                        timestamp=forgery_py.date.date(True),
                        author=user)
            db.session.add(post)
            db.session.commit()

    # Функция преобразования ресурсов в вформат JSON и обратно
    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'comments': url_for('api.get_post_comments', id=self.id, _external=True),
            'comments_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                       tags=allowed_tags, strip=True))


# Собственная реализация класса AnonymousUserMixin
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Comment.body, 'set', Comment.on_changed_body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))