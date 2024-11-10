# Приложение "SecretMaker"

API сервис для одноразовых секретов. Он позволяет создать секрет, задать кодовую фразу для его открытия и 
генерирует код, по которому можно прочитать секрет только один раз.


## Структура проекта:
```
.
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── main.py
├── requirements.txt
├── src
│   ├── api
│   │   └── api_v1
│   │       └── routers
│   │           └── secret_router.py
│   └── core
│       ├── config.py
│       ├── database
│       │   ├── db_helper.py
│       │   ├── models.py
│       │   └── schemas.py
│       └── utils.py
└── tests
    ├── conftest.py
    └── test_secret.py
```

## В проекте были использованы такие библиотеки:

1. Python 3.7
2. FastApi
3. PostgreSQL
4. SqlAlchemy(async)
5. Pytest
6. Docker

## Установка

1. Клонируйте репозиторий на вашу локальную машину:  
   git clone https://github.com/AndrewTarev/secret_maker.git

2. Добавьте файл .env, скопируйте туда шаблон .env.template и вставьте свои переменные

3. Запустите docker-compose командой:  
   docker compose build  
   docker compose up