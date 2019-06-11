from flask import render_template, request, jsonify
from . import main
'''
Новая версия обработчика проверяет заголовок Accept запроса,
который фреймворк Werkzeug декодирует в объект request.accept_
mimetypes, и определяет, в каком формате клиент хотел бы получить
ответ. Обычно браузеры не накладывают ограничений на формат от-
вета, поэтому данные в формате JSON возвращаются только клиен-
там, готовым принимать данные в формате JSON и не готовым при-
нимать данных в формате HTML.
'''


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500