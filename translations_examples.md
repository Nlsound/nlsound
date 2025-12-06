# Translation examples for Flask-Babel (messages.po)

Below are example entries for RU, EN, ET to paste into `translations/<lang>/LC_MESSAGES/messages.po` after initializing with `pybabel`.

Remember to run:

```
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l ru
pybabel init -i messages.pot -d translations -l en
pybabel init -i messages.pot -d translations -l et
# later updates
pybabel update -i messages.pot -d translations
# compile
pybabel compile -d translations
```

## RU (ru/LC_MESSAGES/messages.po)
```
msgid "NL PRODUCTION"
msgstr "NL PRODUCTION"

msgid "event technical solutions"
msgstr "event technical solutions"

msgid "Связаться с нами"
msgstr "Связаться с нами"

msgid "Видео, свет, звук, трансляции — опишите задачу, и мы вернёмся к вам."
msgstr "Видео, свет, звук, трансляции — опишите задачу, и мы вернёмся к вам."

msgid "Спасибо! Заявка отправлена, мы свяжемся с вами."
msgstr "Спасибо! Заявка отправлена, мы свяжемся с вами."

msgid "Имя"
msgstr "Имя"

msgid "Фамилия"
msgstr "Фамилия"

msgid "Номер телефона"
msgstr "Номер телефона"

msgid "E-mail"
msgstr "E-mail"

msgid "Сообщение"
msgstr "Сообщение"

msgid "Отправить"
msgstr "Отправить"

msgid "Введите имя"
msgstr "Введите имя"

msgid "Введите фамилию"
msgstr "Введите фамилию"

msgid "Ваш телефон"
msgstr "Ваш телефон"

msgid "Коротко опишите задачу"
msgstr "Коротко опишите задачу"
```

## EN (en/LC_MESSAGES/messages.po)
```
msgid "NL PRODUCTION"
msgstr "NL PRODUCTION"

msgid "event technical solutions"
msgstr "event technical solutions"

msgid "Связаться с нами"
msgstr "Contact us"

msgid "Видео, свет, звук, трансляции — опишите задачу, и мы вернёмся к вам."
msgstr "Video, light, sound, streaming — describe your project and we’ll get back to you."

msgid "Спасибо! Заявка отправлена, мы свяжемся с вами."
msgstr "Thank you! Your request has been sent, we will contact you soon."

msgid "Имя"
msgstr "First name"

msgid "Фамилия"
msgstr "Last name"

msgid "Номер телефона"
msgstr "Phone number"

msgid "E-mail"
msgstr "E-mail"

msgid "Сообщение"
msgstr "Message"

msgid "Отправить"
msgstr "Send"

msgid "Введите имя"
msgstr "Enter first name"

msgid "Введите фамилию"
msgstr "Enter last name"

msgid "Ваш телефон"
msgstr "Your phone number"

msgid "Коротко опишите задачу"
msgstr "Briefly describe your project"
```

## ET (et/LC_MESSAGES/messages.po)
```
msgid "NL PRODUCTION"
msgstr "NL PRODUCTION"

msgid "event technical solutions"
msgstr "event technical solutions"

msgid "Связаться с нами"
msgstr "Võta meiega ühendust"

msgid "Видео, свет, звук, трансляции — опишите задачу, и мы вернёмся к вам."
msgstr "Video, valgus, heli, ülekanded — kirjelda oma projekti ja võtame sinuga ühendust."

msgid "Спасибо! Заявка отправлена, ��ы свяжемся с вами."
msgstr "Aitäh! Sinu päring on saadetud, võtame sinuga peagi ühendust."

msgid "Имя"
msgstr "Eesnimi"

msgid "Фамилия"
msgstr "Perekonnanimi"

msgid "Номер телефона"
msgstr "Telefoninumber"

msgid "E-mail"
msgstr "E-post"

msgid "Сообщение"
msgstr "Sõnum"

msgid "Отправить"
msgstr "Saada"

msgid "Введите имя"
msgstr "Sisesta eesnimi"

msgid "Введите фамилию"
msgstr "Sisesta perekonnanimi"

msgid "Ваш телефон"
msgstr "Sinu telefoninumber"

msgid "Коротко опишите задачу"
msgstr "Kirjelda lühidalt oma projekti"
```
