from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role
from flask_pagedown.fields import PageDownField
'''
class RegistrationForm(Form):
Эта форма также включает два нестандартных валидатора , реа-
лизованных как методы. Если форма определяет метод с именем,
начинающимся с префикса validate_, за которым следует имя поля,
этот метод будет вызываться вместе с любыми другими валидатора-
ми. В данном случае нестандартные валидаторы для полей email и
username проверяют, не дублируются ли значения этих полей.

class EditProfileAdminForm(Form):
Поля email и username определяются так же, как в форме аутенти-
фикации, но к их проверке следует подойти более внимательно. Для
обоих полей сначала необходимо проверить, изменились ли они, и
только если поля изменились, нужно проверить, не совпадают ли они
с данными другого пользователя. Если эти поля не изменялись, про-
верка должна считаться пройденной. Чтобы реализовать эту логику,
конструктор формы принимает объект User и сохраняет его в пере-
менной-члене, которая затем используется в собственных методах-
валидаторах.
'''


# Форма логина
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# Форма регистрации
class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, '
                                  'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# Форма изменения данных пользователя пользователем
class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


# Форма изменения данных пользователя администратором
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(1,64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_/]*$',0,'Usernames must have only letters, '
                                                                           'numbers, dots or underscores')])
    confirmed =BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# Форма написания поста
class PostForm(Form):
    # Было до введедния markdown
    # body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Форма комментария
class CommentForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')