from flask import Flask, render_template, request, g, url_for, flash, redirect, send_from_directory
from flask_babel import Babel, gettext, get_locale
import os
import requests

app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = 'change-this-secret'

# Babel / i18n configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Mailgun configuration (from environment)
app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')
app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')
app.config['MAILGUN_FROM_EMAIL'] = os.environ.get('MAILGUN_FROM_EMAIL')
app.config['MAILGUN_TO_EMAIL'] = os.environ.get('MAILGUN_TO_EMAIL')

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


def send_email_via_mailgun(subject: str, text: str) -> None:
    """
    Отправка email через Mailgun.
    Используется HTTP POST к https://api.mailgun.net/v3/<domain>/messages
    Авторизация: basic auth ('api', MAILGUN_API_KEY).
    """
    api_key = app.config.get('MAILGUN_API_KEY')
    domain = app.config.get('MAILGUN_DOMAIN')
    from_email = app.config.get('MAILGUN_FROM_EMAIL')
    to_email = app.config.get('MAILGUN_TO_EMAIL')

    if not all([api_key, domain, from_email, to_email]):
        raise RuntimeError('Mailgun config is not fully set via environment variables')

    # Используем EU регион, диагностика в терминал
    resp = requests.post(
        f"https://api.eu.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": os.getenv("MAILGUN_FROM_EMAIL"),
            "to": os.getenv("MAILGUN_TO_EMAIL"),
            "subject": subject,
            "text": text,
        },
        timeout=10,
    )

    print("MAILGUN STATUS:", resp.status_code)
    print("MAILGUN RESPONSE:", resp.text)

    if resp.status_code not in (200, 202):
        app.logger.error("Mailgun error: status=%s, body=%s", resp.status_code, resp.text)
        raise RuntimeError(f"Mailgun request failed with status {resp.status_code}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        # Валидация обязательных полей
        if not email or not message:
            flash(gettext('Пожалуйста, укажите e-mail и сообщение.'), 'error')
            return redirect(url_for('index', lang=g.get('current_lang', app.config.get('BABEL_DEFAULT_LOCALE', 'ru'))))

        try:
            subject = "ЗАЯВКА NLProduction"
            body_lines = [
                f"Имя: {name or '-'}",
                f"Телефон: {phone or '-'}",
                f"E-mail: {email}",
                "",
                "Сообщение:",
                message,
            ]
            text = "\n".join(body_lines)

            send_email_via_mailgun(subject, text)

            flash(gettext('Спасибо! Заявка отправлена, мы свяжемся с вами.'), 'success')
            return redirect(url_for('index', lang=g.get('current_lang', app.config.get('BABEL_DEFAULT_LOCALE', 'ru'))))
        except Exception:
            app.logger.exception("Failed to send contact message via Mailgun")
            flash(gettext('Не удалось отправить сообщение. Попробуйте позже.'), 'error')
            return redirect(url_for('index', lang=g.get('current_lang', app.config.get('BABEL_DEFAULT_LOCALE', 'ru'))))

    return render_template('index.html')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/google3193fab71dd9080d.html')

def google_verify():

    return app.send_static_file('google3193fab71dd9080d.html')

if __name__ == '__main__':
    # Для разработки оставляем debug=True. На проде заменить на False / убрать.
    app.run(debug=True)
