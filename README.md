<h2> Новостная рекомендательная система, построенная на основе наивного Байесовского классификатора</h2>

<h3>Как развернуть проект локально?</h3>

<b>а) С помощью Docker</b>

    docker-compose build
    docker-compose up -d

<b>б) Самостоятельно</b>

    pip install -r requirements/base.txt
    cd ./src/
    python3 manage.py runserver

<br>
<i>Запущенный сервер доступен по адресу 127.0.0.1:8000</i>
<br>
<h3>Авторизация</h3>

![login](https://github.com/EvilPug/news/raw/hackernews/previews/login.png)

<h3>Регистрация</h3>

![signup](https://github.com/EvilPug/news/raw/hackernews/previews/signup.png)

<h3>Главная страница</h3>
Размечаем новости, используя один из трех вариантов: 'Не интересно', 'Возможно интересно', 'Интересно'

![index](https://github.com/EvilPug/news/raw/hackernews/previews/index.png)

<h3>Рекомендации</h3>
Прогоняя размеченные новости через классификатор, мы получаем список тех из них, которые, скорее всего, будут нам интересны.

![recommendations](https://github.com/EvilPug/news/raw/hackernews/previews/recommendations.png)

<h3>Избранные новости</h3>

![favorite](https://github.com/EvilPug/news/raw/hackernews/previews/favorite.png)

> ### TODO list :
> - [x] Авторизация пользователей
> - [x] Личный кабинет
> - [x] Переработать пользовательский интерфейс
> - [x] Возможность добавлять новости в избранное
> - [x] Подтверждение регистрации на эл. почту
> - [ ] Вывод новостей по страницам
> - [ ] Автоматическое пополнение неразмеченных новостей
> - [ ] Забыли пароль?
