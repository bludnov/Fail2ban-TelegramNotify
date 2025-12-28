# 🚀 Fail2ban-TelegramNotify - Скрипт для телеграмм бота

<div align="center">
  <img src="https://img.shields.io/badge/Fail2ban_TelegramNotify-Anti_Hacking-blue?logo=terminal&logoColor=white" alt="Fail2ban-TelegramNotify">
</div>

## 📝 Описание проекта

Скрипт, который срабатывает на вашем VDS-сервере когда боты пытаются взломать пароль ssh/ищут дыры в Php, админке и т.п, например запросы /admin/.env /admin/.git/config /admin/function.php /admin/controller/extension/extension/jnweppgp.php /admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php и тому подобные

## ⚙️ Требования

- Python 3.* версии
- Мозги

## 🛠️ Как использовать

```bash
Установите Fail2Ban на ваш VDS-сервер, настройте его через файл-конфиг по своему усмотрению
Создайте файл .env с содержимым TelegramAPI="ваш ключ бота"
Откройте script.py и измените CHAT_ID на ваш User ID в телеграмме (Chat ID)
python script.py
```

<div align="center"> <sub>Проект находится под Apache-2.0 license</div>
