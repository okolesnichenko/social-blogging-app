from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_pagedown import PageDown

'''
1)App конструктор импортирует большую часть используемых рас-
ширений фреймворка Flask, но, так как к этому моменту экземпляр
приложения пока отсутствует, он создает их неинициализированны-
ми, вызывая конструкторы расширений без аргументов. Функция
create_app() является фабричной функцией приложения и принимает
аргумент с именем конфигурации. Параметры настройки, хранящие-
ся в одном из классов, объявленных в config.py, можно импортиро-
вать непосредственно в приложение с помощью метода from_object()
объекта app.config. Объект с настройками выбирается по имени из сло-
варя config. Как только приложение будет создано и настроено, можно
выполнить инициализацию созданных расширений вызовом их ме-
тодов init_app().
2)Атрибуту session_protection объекта LoginManager можно присваи-
вать значения None, 'basic' или 'strong', соответствующие разным
уровням защищенности пользовательских сеансов от постороннего
вмешательства. Если установить значение 'strong', Flask-Login бу-
дет следить за IP-адресом клиента и агентом браузера и завершать
сеанс принудительно при обнаружении изменений. Атрибуту login_
view присваивается имя конечной точки, соответствующей странице
аутен тификации. Напомню: так как маршрут login находится внутри
макета, в его начало необходимо добавить имя макета.

Flask-PageDown , обертка вокруг фреймворка PageDown для Flask,
позволяющая интегрировать PageDown в формы Flask-WTF ;
'''
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# Функция создания экземпляра приложения, использувется в manage.py
def create_app(config_name):
    # 4) Инициализация приложения
    app = Flask(__name__)
    # 5) Применение конфигов
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 6) Инициализация расширений
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 7) Добавление макетов с разным функционалом
    # Регистрация макета main
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Регситрация макета auth c префиксом '/auth' т.е. (/auth/login)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # Регистрация макета api
    from app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
