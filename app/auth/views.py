from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User, db
from ..email import send_email
from app.main.forms import LoginForm, RegistrationForm
from flask_login import current_user
import jwt
'''
@auth.route('/login', methods=['GET', 'POST'])
def login():
Эта функция(LoginForm) создает объект LoginForm и использует его как прос тую
форму, подобно тому, как демонстрировалось в главе 4. Когда при-
ложение получает запрос типа GET, функция представления просто
отображает шаблон, возвращая клиенту форму. Когда приложение
получает форму, отправленную в запросе POST, вызывается функция
validate_on_submit() из расширения Flask-WTF, проверяющая пере-
менные формы, и затем выполняется попытка аутентифицировать
пользователя.
Для проведения аутентификации функция сначала извлекает ин-
формацию о пользователе из базы данных по полученному из формы
адресу электронной почты. Если пользователь с указанным электрон-
ным адресом существует, вызывается его метод verify_password(), ко-
торому передается пароль, так же полученный из формы. Если пароль
верный, вызывается функция login_user() из расширения Flask-Login
для запоминания аутентифицированного пользователя. Она прини-
мает объект, представляющий пользователя, и необязательный логи-
ческий флаг «запомнить меня», тоже полученный с формой. Значение
False в этом аргументе приводит к закрытию сеанса пользователя сра-
зу после закрытия окна пользователя, вследствие чего при следую-
щем посещении приложения ему вновь придется пройти процедуру
аутентификации. Значение True вызовет создание cookie с длитель-
ным сроком хранения и отправку его браузеру пользователя, с по-
мощью которого можно будет восстановить прерванный сеанс.

@auth.before_app_request
def before_request():
Обработчик before_app_request перехватывает ВСЕ !запросы!, только
если выполняются следующие три условия:
1. Пользователь был аутентифицирован (вызов current_user.is_
authenticated() должен вернуть True).
2. Учетная запись не подтверждена.
3. Конечная точка запроса (доступна как request.endpoint) нахо-
дится за пределами макета аутентификации. Доступ к маршру-
ту аутентификации должен оставаться открытым, так как эти
маршруты позволяют подтверждать и выполнять другие опе-
рации с учетными записями.
Если все три условия выполняются, производится переадресация
на новый маршрут /auth/unconfirmed, для которого отображается
страница с предложением подтвердить учетную запись.
Метод ping() должен вызываться при приеме любых запросов от
пользователя.
'''

# Страница логина (функция представления)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

# Метод для функционала кнопки logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

# Страница регистрации (функция представления)
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

# Подтверждение токена с почты
@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

# Переотправка сообщения на почту
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email('auth/email/confirm',
                'Confirm Your Account', current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

# Функция, которая выполняется до всех запросов
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

# Страница неподтвержденного пользователя
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')