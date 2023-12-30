<h1>Бот для парсинга сообщений из групп</h1>

<h2>Описание и ключевые моменты</h2>
<li>Парсинг сообщений из групп в специальном формате</li>
<li>Наличие стоп слов</li>
<li>Команда /join для автоматического поиска и захода в группы по фразе</li>

<h2>Подготовка проекта и запуск</h2>
<p>API_ID и API_HASH возьмите от своего аккаунта на сайте https://my.telegram.org/ и вставьте данные в файл config.py</p>
<h3>Установка вирутальной среды и установка зависимостей</h3>
```
python -m venv env
env/Scripts/activate.ps1
pip install -r requiremens.txt
```
<h3>Запуск</h3>
`python main.py`
