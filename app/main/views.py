from flask import make_response, current_app, request, redirect, flash, abort, url_for, render_template, session
from datetime import datetime
from . import main # импорт макета
from flask_login import login_required, current_user
from .forms import CommentForm, PostForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Comment, User, Role, Permission, Post
from ..decorators import admin_required, permission_required
from flask_sqlalchemy import get_debug_queries
'''
@login_required
@main.route('/', methods=['GET', 'POST'])
def index():
-Эта функция передает форму и полный список сообщений в бло-
ге. Список отсортирован по времени создания сообщений в порядке
убывания (то есть от новых к старым). Форма создания нового со-
общения обрабатывается как обычно: если текстовое поле прошло
проверку, создается новый экземпляр Post. Однако перед созданием
выполняется проверка привилегий пользователя на наличие права
создавать новые сообщения.
-Переменная current_user из Flask-Login, подобно всем переменным
контекста, реализована как локальный для потока промежуточный
объект (прокси-объект). Этот объект действует подобно объекту User,
но в действительности это тонкая обертка вокруг фактического объ-
екта User. В базу можно записать только настоящий объект User, для
получения которого следует вызвать метод _get_current_object().
-Номер страницы определяется из строки запроса, доступной как
request.args. Когда номер страницы не указан явно, по умолчанию ис-
пользуется число 1 (первая страница). Аргумент type=int гарантирует
возврат значения по умолчанию, если аргумент не сможет быть пре-
образован в целое число.
Чтобы загрузить единственную страницу записей, вместо мето-
да all() вызывается метод paginate(). Этот метод принимает но-
мер страницы в первом и единственном обязательном аргументе.
Чтобы определить число элементов на странице, можно передать
необязательный аргумент per_page. Если этот аргумент не указан
явно, по умолчанию он принимает значение 20. Еще один необя-
зательный аргумент error_out позволяет генерировать ошибку 404
при попытке запросить страницу за пределами допустимого диа-
пазона, если передать в нем значение True (по умолчанию). Если
передать в error_out значение False, для страниц с номерами вне до-
пустимого диапазона будет возвращаться пустой список элементов.
Чтобы сделать размер страниц настраиваемым, значение аргумента
per_page извлекается из параметра настройки приложения с именем
FLASKY_POSTS_PER_PAGE.

@main.route('/user/<username>')
def user(username):
Этот маршрут должен быть добавлен в макет main. Адрес URL
страницы профиля для пользователя john будет иметь вид http://
localhost:5000/user/john. Если имя пользователя, указанное в URL,
будет найдено в базе данных, шаблон user.html отобразит страницу
профиля для этого пользователя. Неверное имя пользователя вы-
зовет возврат ошибки 404.
Список сообщений, принадлежащих пользователю, извлекается
с помощью отношения User.posts, которое является объектом запро-
са, поддерживающим возможность применения фильтров, таких как
order_by().

show_all(),  show_followed()
Функция set_cookie() принимает имя cookie и значение в первых
двух аргументах. В необязательном аргументе max_age устанавлива-
ется срок хранения cookie в секундах. Если опустить этот аргумент,
cookie будет храниться, пока пользователь не закроет окно браузера.
В данном случае устанавливается срок хранения 30 суток, поэтому
данная настройка сохранится, даже если пользователь не будет захо-
дить в приложение несколько дней.
'''

# Тестовая index страница (функция представления)
@login_required
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
        form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items # Страинца 164, list-постов
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


# Страница профиля (функция представления)
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/time')
def nexturl():
    return render_template('time.html', current_time=datetime.utcnow())

# Страница изменения данных профиля (функция представления)
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

# Страница изменения данных пользователя (функция представления)
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post= Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page =request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count()-1) / \
            current_app.config['FLASKY_COMMENTS_PER_PAGE']+1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post= Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not follow this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are unfollow from user %s' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page,
                                         per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'], error_out=False)
    followers = [{'user': item.follower, 'timestamp': item.timestamp}for item in pagination.items]
    return render_template('followers.html', user=user,
                           title="Followers of", endpoint='.followers', pagination=pagination, follows=followers)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page,
                                         per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'], error_out=False)
    followed = [{'user': item.followed, 'timestamp': item.timestamp}for item in pagination.items]
    return render_template('followers.html', user=user,
                           title="Followed by", endpoint='.followers', pagination=pagination, follows=followed)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_QUERY_TIME']:
            current_app.logger.warning('Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
            (query.statement, query.parameters, query.duration,
            query.context))
    return response
