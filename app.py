from flask import Flask, render_template, request, g, url_for
from flask_babel import Babel, gettext, get_locale

app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = 'change-this-secret'

# Babel / i18n configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Supported languages
LANGUAGES = ['ru', 'en', 'et']


# --- i18n / Flask-Babel usage ---
# Все текстовые строки в Python и шаблонах должны быть обёрнуты в gettext / _():
#   _('Имя'), _('Фамилия'), ...
# Файлы переводов хранятся только в translations/<lang>/LC_MESSAGES/messages.po
# и компилируются в messages.mo.
#
# Основные команды PyBabel (запускать из корня проекта):
#
# 1) Извлечь строки из Python и Jinja2-шаблонов:
#    pybabel extract -F babel.cfg -o messages.pot .
#
# 2) Инициализировать переводы (однократно для каждого языка):
#    pybabel init -i messages.pot -d translations -l ru
#    pybabel init -i messages.pot -d translations -l en
#    pybabel init -i messages.pot -d translations -l et
#
# 3) После изменения строк в коде/шаблонах обновлять каталоги:
#    pybabel update -i messages.pot -d translations
#
# 4) Скомпилировать переводы (обязательно перед запуском для боевого режима):
#    pybabel compile -d translations


def select_locale():
    """Определение текущего языка по параметру ?lang=.

    Если параметр не задан или язык не поддерживается, используем ru.
    Текущее значение сохраняем в g.current_lang, чтобы формировать ссылки,
    но для подсветки активного языка в шаблоне используем get_locale().
    """
    lang = request.args.get('lang')
    if lang in LANGUAGES:
        g.current_lang = lang
        return lang

    # Fallback to default
    g.current_lang = app.config.get('BABEL_DEFAULT_LOCALE', 'ru')
    return g.current_lang


# Инициализация Babel с функцией выбора языка
babel = Babel(app, locale_selector=select_locale)


@app.context_processor
def inject_globals():
    """Глобальные переменные и функции, доступные во всех шаблонах.

    _  — это настоящий gettext из Flask‑Babel.
    current_lang — текущий язык (для подсветки активной кнопки и action формы).
    LANGUAGES    — список доступных языков (для переключателя).
    url_for      — стандартный Flask url_for.
    """
    try:
        # Текущий язык берём у Flask‑Babel, чтобы он совпадал с тем,
        # который реально использует система переводов.
        current = str(get_locale())
    except Exception:
        current = app.config.get('BABEL_DEFAULT_LOCALE', 'ru')

    return {
        'current_lang': current,
        'LANGUAGES': LANGUAGES,
        '_': gettext,
        'url_for': url_for,
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    message_sent = False

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')

        # Минимальная валидация: email обязателен для успешной отправки
        if email:
            # Логируем отправленные данные (дальше можно добавить отправку на email)
            app.logger.info(
                "NL PRODUCTION contact: name=%s, phone=%s, email=%s, message=%s",
                name,
                phone,
                email,
                message,
            )
            message_sent = True
        else:
            message_sent = False

    return render_template('index.html', message_sent=message_sent)


if __name__ == '__main__':
    # Для разработки оставляем debug=True. На проде заменить на False / убрать.
    app.run(debug=True)
