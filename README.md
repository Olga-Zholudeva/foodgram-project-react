# Продуктовый помощник

## Описание проекта:

Онлайн-сервис, который позволяет пользователям:
- публиковать рецепты
- подписываться на публикации других пользователей
- добавлять понравившиеся рецепты в список «Избранное»
- скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд

### Технологии:
- Python 3.7.9
- Django 3.2.18
- Gunicorn 20.0.4

## Пользовательские роли и права доступа:

### Неавторизованные пользователи могут:
- Просматривать рецепты, в т.ч. страницу отдельного рецепта
- Зарегистрироваться на сайте

### Авторизованные пользователи могут:
- Просматривать рецепты, в т.ч. страницу отдельного рецепта
- Зарегистрироваться на сайте
- Создавать новые рецепты и редактировать свои рецепты
- Подписываться на других авторов
- Добавлять рецепты в избранное
- Выгружать список покупок с игрединетами для выбранных рецептов

### Запуск проекта на удаленном сервере:
 - Клонируем репозиторий: **git clone [foodgram-project-react](https://github.com/Olga-Zholudeva/foodgram-project-react)**
 - Устанавливаем на сервере Docker, Docker Compose:
     sudo apt install curl                                   # установка утилиты для скачивания файлов
     curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
     sh get-docker.sh                                        # запуск скрипта
     sudo apt-get install docker-compose-plugin              # последняя версия docker compose
 - Копируем на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды необходимо выполнять находясь в папке infra):
     scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                     # IP - публичный IP сервера
 - Создаем переменные окружения для работы с GitHub Actions в репозитории в разделе Secrets > Actions:
     SECRET_KEY              # секретный ключ Django проекта
     DOCKER_PASSWORD         # пароль от Docker Hub
     DOCKER_USERNAME         # логин Docker Hub
     HOST                    # публичный IP сервера
     USER                    # имя пользователя на сервере
     PASSPHRASE              # *если ssh-ключ защищен паролем
     SSH_KEY                 # приватный ssh-ключ
     TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
     TELEGRAM_TOKEN          # токен бота, посылающего сообщение
     
     DB_ENGINE               # django.db.backends.postgresql
     DB_NAME                 # postgres
     POSTGRES_USER           # postgres
     POSTGRES_PASSWORD       # postgres
     DB_HOST                 # db
     DB_PORT                 # 5432 (порт по умолчанию)
 - Создаем и запускаем контейнеры Docker, выполняем команду на сервере: **sudo docker compose up -d**
 - Выполняем миграции: **sudo docker compose exec backend python manage.py migrate**
 - Создаем супер пользователя: **sudo docker compose exec backend python manage.py createsuperuser**
 - Применяем статику: **sudo docker compose exec backend python manage.py collectstatic --noinput**
 - Наполняем базу данных содержимым из файла ingredients.csv: **sudo docker compose exec backend python manage.py loaddata ingredients.csv**

### Локальный запуск проекта:
- Клонируем репозиторий: **git clone [foodgram-project-react](https://github.com/Olga-Zholudeva/foodgram-project-react)**
- Cоздаем и активировируем виртуальное окружение: **python3 -m venv env source env/bin/activate**
- Устанавливаем зависимости из файла requirements.txt: **pip install -r requirements.txt**
- Создаем и запускаем контейнеры Docker, последовательно выполняя команды по созданию миграций, сбору статики, созданию суперпользователя, как указано выше.
     docker-compose -f docker-compose-local.yml up -d
  
После запуска проект будут доступен по адресу: http://localhost/

### Использование проекта через запросы:
- Пользоваться проектом можно через запросы к API
- Документация к API: http://localhost/api/docs/redoc.html

### Проект выполнила:

 **Ольга Жолудева**


