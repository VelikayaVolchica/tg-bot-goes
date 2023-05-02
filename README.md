# Telegram bot save places

## Что умеет этот бот
Бот сохраняет места и мероприятия, которые хочется посетить в будущем. Бот работает с базой MySQL.

### Инициализация бота:
```bash
git clone https://github.com/VelikayaVolchica/tg-bot-goes.git
# Переходим в директорию проекта, устанавливаем необходимые библиотеки и кладем свой тг токен бота и свой тг id
cd <Название проекта>
pip install -r app/requirements.txt
echo API_TOKEN=<YOUR_TELEGRAM:TOKEN> > .env
echo TELEGRAM_ID=<YOUR_TELEGRAM:ID> > .env
```

### Запуск бота
```bash
python3 app/bot.py
```

## ToDo list
1. Сделать встроенные кнопки (клавиатуру)
2. Автоматическое удаление неактуальных мероприятий
3. Отображение списка мест небольшими партиями, а не все сразу
