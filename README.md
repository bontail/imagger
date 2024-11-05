
# Веб - API

## Django Rest Framework, PostgreSQL, RabbitMQ, Celery, Docker-compose

###

Создать env файл по примеру
```shell
cp .example.env .env
```

Собрать контейнеры
```shell
docker-compose build
```

Запустить контейнеры
```shell
docker-compose up
```

Собрать статические файлы
```shell
make collectstatic
```

Запустить тесты
```shell
make tests
```

Документация API находится на http://localhost:8000/swagger/

-   Загрузка нового изображения - **/create_image/**

-   Получение списка всех загруженных изображений - **/get_all_images/**

-   Получение информации о конкретном изображении по id - **/get_image/id/**

-   Обновление информации об изображении (например, имени или тегов) - **/update_image/id/**

-   Удаление изображения - **/delete_image/id/**


### Дополнительные задания

Декоратор @retry находится в [additional_task.py](additional_task.py)