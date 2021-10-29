# API Review

- The Review project collects user reviews(Review) for works (Titles). The works are divided into categories: "Books", "Films", "Music". The list of categories can be expanded by the administrator.
- The works themselves are not stored in Review, you can not watch a movie or listen to music here.
- In each category there are works: books, movies or music.
- A work can be assigned a genre from the list of preset ones. Only the administrator can create new genres.
- Grateful or outraged users leave text reviews for the works and give the work a rating in the range from one to ten (an integer); an average rating of the work is formed from user ratings — a rating (an integer). The user can leave only one review for one work.

## Functionality

* Getting confirmation code using email and then Auth with JWT-token.
* Permission system for different roles: admin/moderator/user.
* CRUD title, category, genre, review, comment.

## What I used

- Python 3
- Django REST Framework
- Django 2.2
- PostgreSQL
- Simple-JWT
- OpenAPI.
- Docker

## Local deploy

+ Uncomment .env in .gitignore and set secrets in .env like:
    ```sh
    SECRET_KEY=YOUR_SECRET_KEY
    DEBUG=TRUE # if you want to work in dev
    ALLOWED_HOSTS=host1, host2, etc 
    CORS_ALLOWED_ORIGINS=host1, host2, etc. # uncomment CORS_ALLOWED_ORIGINS and comment CORS_ALLOW_ALL_ORIGINS in settings.py, if you want  special hosts for CORS
    DJANGO_SUPERUSER_USERNAME=admin # set instead admin, username of superuser
    DJANGO_SUPERUSER_EMAIL=admin@gmail.com # set instead admin@gmail.com, email of superuser
    DJANGO_SUPERUSER_PASSWORD=admin # set instead admin, password of superuser
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres # set instead postgres, name of db
    POSTGRES_USER=postgres # set instead postgres, nikname of superuser of db
    POSTGRES_PASSWORD=postgres # set instead postgres, password of db
    DB_HOST=db # you can rename it or set a needed host, but before make changes to docker-compose.yaml
    DB_PORT=5432
    ```
+ [Install docker ](https://docs.docker.com/get-docker/)
+ If you don't need any files or dirs in container, you can set them in .dockerignore
+ In dir with project run:
    ```sh
    $ docker-compose up
    ```
+ Open a new window of terminal and from dir of project run:
    ```sh
    docker-compose exec web ./manage.py migrate --noinput
    docker-compose exec web ./manage.py database
    docker-compose exec web ./manage.py create_admin
    docker-compose exec web ./manage.py collectstatic --no-input 
    ```
+ You can get admin panel in http://localhost/admin/ with username and password, that you set in .env (DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD)

## Documentation and requests examples

If you local deployed project, you can see that here:
* [ Task and full documentation (Redoc) ]( http://localhost/redoc/ )
* [ Documentation and requests - Swagger]( http://localhost/swagger/ )
* [ Documentation and requests - Redoc ]( http://localhost/redoc_main/ )

## Task

- Проект Review собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
- Сами произведения в Review не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
- В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
- Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

**Техническое описание проекта Review**
-  Вам доступен репозиторий, в нём сохранён пустой Django-проект.
К проекту по адресу http://127.0.0.1:8000/redoc/ вы можете найти полное ТЗ. В нем описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.
Ваша задача — написать бэкенд проекта (приложение reviews) и API для него (приложение api) так, чтобы они полностью соответствовали документации.

**Пользовательские роли**
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладает правами администратора (admin).

**Алгоритм регистрации пользователей**
- Для добавления нового пользователя нужно отправить POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис Review отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
- После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).
- Если пользователя создаёт администратор, например, через POST-запрос на эндпоинт api/v1/users/ — письмо с кодом отправлять не нужно (описание полей запроса для этого случая — в документации).

**Ресурсы API Review**
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
- Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

**Связанные данные и каскадное удаление**
- При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
- При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
- При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
- При удалении объекта категории Category не нужно удалять связанные с этой категорией произведения.
- При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.

**База данных**
- В репозитории с заданием, в директории /static/data, подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Review и Comments. Тестировать пустой проект будет неудобно, а наполнять его руками — долго.
После того как вы подготовите модели, заполните базу данных контентом из приложенных csv-файлов.
