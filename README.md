# log_processor
### Загрузка и обработка логов

#### Реализована загрузка nginx лога из файла формата json

Для добавления других логов нужно добавить модель данных 
и класс-загрузчик (подкласс logs.utils.loaders.loaders.BaseLoader)

Для добавления других источников нужно добавить класс-reader (подкласс logs.utils.loaders.readers.BaseReader)

Для добавления других форматов данных нужно добавить класс-парсер (logs.utils.loaders.parsers.BaseParser)


Индексы на NginxLog будут зависеть от операций чтения, в данных момент индексы не висят на полях с низкой
селективностью, но при постоянном включении этих полей в фильтрацию результатов можно подумать о добавлении
их в составной индекс.

В идеале добавить elastic для операций чтения, возможно через django-haystack или например с помощью
django-elasticsearch-dsl, но это не в рамках тестового


Запуск проекта: 
```
- git clone git@github.com:fsowme/log_processor.git && cd log_processor
- docker-compose -f develop/docker-compose.yml up -d
- docker-compose -f develop/docker-compose.yml run --rm app python manage.py migrate
- docker-compose -f develop/docker-compose.yml run --rm app python manage.py collectstatic
- docker-compose -f develop/docker-compose.yml run --rm app python manage.py createsuperuser
```

Загрузка логов:
```
- Скопировать файл в папку src
- docker-compose -f develop/docker-compose.yml run --rm app python manage.py load_log \
  nginx --parser=json --reader=file --source=<имя файла>
```
