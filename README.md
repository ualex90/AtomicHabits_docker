# AtomicHabits

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. 
<br/>
Данный проект представляет из себя бэкенд-часть SPA веб-приложения, реализующая напоминания пользователям о необходимости выполнения действий для выработки привычек
<br/><br/>
<h4>В проекте реализован следующий функционал:</h4>
- Регистрация<br/>
- Авторизация посредством bearer токена<br/>
- Создание привычки (для любого зарегистрированный пользователя кроме модератора)<br/>
- Вывод списка привычек текущего пользователя с пагинацией<br/>
- Вывод списка всех привычек (для модератора)<br/>
- Просмотр привычки (для создателя или модератора и для всей зарегистрированных если привычка публичная)<br/>
- Вывод списка публичных привычек<br/>
- Редактирование привычки (для создателя или модератора)<br/>
- Удаление привычки (только для создателя)<br/>
<br/><br/>
В проекте предусмотренны настройки безопасности CORS. По умолчанию, доступ к приложению только с localhost
<br/><br/>

<h4>Ограничения:</h4>
- Исключен одновременный выбор связанной привычки и указания вознаграждения<br/>
- При обновлении значений "вознаграждение" и "связанная привычка", будет сохранено только одно из этих значений. Сохранится введенное, существующее будет очищено<br/>
- Время выполнения должно быть не больше 120 секунд<br/>
- В связанные привычки могут попадать только привычки с признаком приятной привычки<br/>
- У приятной привычки не может быть вознаграждения или связанной привычки<br/>
- Нельзя выполнять привычку реже, чем 1 раз в 7 дней<br/>
<br/><br/>

<h3>Запуск проекта:</h3>

1. Клонируйте репозиторий;
2. Создайте Telegram бота и получите его токен;
3. Создайте в корне проекта и заполните файл .env:

```
DEBUG=on
SECRET_KEY=

DATABASE_NAME='postgres'
DATABASE_USER='postgres'
DATABASE_PASSWORD='mysecretpassword'
DATABASE_HOST='db'

TELEGRAM_BOT_TOKEN=
```

4. Для первого запуска необходимо собрать образ контейнера. Для этого, находясь в корневой директории проекта
необходимо выполнить команду:

```bash
sudo docker-compose build
```

5. Для запуска проекта:

```bash
sudo docker-compose up
```

Веб приложение будет доступно по адресу: http://127.0.0.1:8000

10. Для получения документации, запустите проект и при помощи браузера перейдите по адресу:
http://127.0.0.1:8000/swagger/
<br/><br/>

Проект готов к заполнению базы данных.

<h3>Инструкция для быстрого заполнения базы данных:</h3>

<h4>Заполнение базы данных из фикстур</h4>

```bash
docker-compose exec app python3 manage.py loaddata fixtures/db.json
```
Далее необходимо указать Telegram ID для всех тестовых пользователей:

```bash
docker-compose exec app python3 manage.py settg --tg TelegramID
```

Где "TelegramID" необходимо заменить на ваш ID, например 123456789
<br/><br/>
По умолчанию, пользователи в базе данных имеют следующие параметры:
<br/>
Администратор:
```
email = 'admin@sky.pro'
password = 'admin'
```
Пользователи:
```
ivanov@sky.pro - MODERATOR
petrov@sky.pro
sidorov@sky.pro

password - 123qwe
```

<h4>Cоздание демонстрационных пользователей</h3>

Если вы желаете заполнить базу привычками самостоятельно, то можно упростить задачу создав тестовых пользователей.
<br/>
Пользователи создаются с параметром --tg. В нем указывается Telegram ID на который будут приходить сообщения.
<br/>
Админ:

```bash
docker-compose exec app python3 manage.py ccsu --tg 123456789
```
Обычные пользователи и 1 из них модератор:

```bash
docker-compose exec app python3 manage.py ccusers --tg 123456789
```
При создании пользователей в консоль выведутся email, пароли, привилегии и Telegram ID# AtomicHabits_docker
