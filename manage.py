import os
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
'''
Сценарий начинается с создания приложения. Конфигурация
приложения определяется переменной окружения FLASK_CONFIG, если
она определена; в противном случае используется конфигурация по
умолчанию. Затем производится инициализация расширений Flask-
Script, Flask-Migrate и контекста для интерактивной оболочки Py-
thon.
'''
# 1)В create_app инициализация приложения
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 2)
'''
Расширение Flask-Script экспортирует класс
Manager, который импортируется из flask_script.
Метод инициализации этого расширения является типичным для
большинства расширений: экземпляр главного класса инициализи-
руется передачей экземпляра приложения конструктору. Затем соз-
данный объект используется там, где необходимы функциональные
возможности расширения. В данном случае для запуска сервера ис-
пользуется метод manager.run() объекта расширения, поддерживаю-
щего парсинг командной строки.
'''
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tasks."""

    from flask_migrate import init
    from flask_migrate import migrate
    from flask_migrate import upgrade

    from app.models import Role, User

    # migrate database to latest revision
    migrate()
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()


# 3) Запуск приложения 4 в app.init
if __name__ == '__main__':
    manager.run()
