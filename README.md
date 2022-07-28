#Steam Open Case Calculator

## Настройка и запуск проекта:

    Необходимые зависимости:
        - git
        - docker

    $ git clone https://github.com/dimadeck/steam-open-case-calculator
    $ cd steam-open-case-calculator

    Создать файл .env с содержимым (при необходимости, выставить свои значения):

        DB_HOST=db
        DB_PORT=5432
        DB_USERNAME=inventory_sum_user
        DB_PASSWORD=inventory_sum_user_password
        DB_BASENAME=inventory_sum
        DB_PROTOCOL=postgresql+asyncpg
        BACKEND_URL=http://127.0.0.1:8004/api/v1
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=43200
        JWT_SECRET=31f04487001ce91ec7c2fa1615fcd744614a3c4fda18f1ad
        JWT_ALGORITHM=HS256

        LOG_CONSOLE=True
        LOG_LEVEL=info
        LOG_FILENAME=SOCC.log
    
    Для настройки базы данных(применения миграций) изменить переменную окружения:
        DB_HOST=127.0.0.1
    
    $ python -m venv env
    $ env\Scripts\activate.exe 
    или $ source env/bin/activate
    $ pip install -r requirements.txt
        
    Если папка migrations пустая или необходимо пересоздать миграции:
        $ alembic revision --autogenerate -m 'Message for commit'
    $ alembic upgrade head 

    Запуск контейнеров:

    $ docker-compose build
    $ docker-compose run



## Цель проекта: 

    Собрать сервис, для стрима с открытием 100 капсул (с наклейками) 
    для автоматического подсчета стоимости наклеек. 


## Описание

    Проект для отслеживания стоимости предметов, выпадающих из капсул и кейсов, 
    а также выводом описания на экран для интеграции с OBS.

    После открытия кейса/капсулы на экране появляется название, стоимость, качество, 
    изображение дропа и общий "Банк" за открытие. 


## Модули:

    1) Core - модуль для получения информации о предмете и записи в БД
        - название, стоимость, качество (+флот), изображение 
        - tags-> [{"category": "Rarity"}] -> color
            - тип, классификация

    2) DataBase - модуль для подключения и взаимодействия с базой данных Postgres 

    3) Worker - запускает core-модуль когда нужно

    4) Server - Веб-сервер для получения информации из базы данных


## Мысли по модулям:

    Core
        Отправляем запрос (раз в 10 секунд) на получение последнего предмета в инвентаре, сравниваем last_assetid из запроса со значением из таблицы WatchedProfile
        Если assetID отличается - записываем в таблицу DropDetail новое значение, 
        полученное из Данных запроса (assets, descriptions) + делаем доп. запросы на получение стоимости и флота (?). 
        Обновляем LastAssetID для текущего профиля. Обновляем TotalCount и TotalAmount. Если isWatching = False ИЛИ LastModifiedDate > 60 минут -> меняем статус isWatching = False и останавливаем наблюдение.
        
    DataBase
    Технологии: Postgresql, SQLAlchemy (интерфейс для подключения), Alembic (для миграций), Pydantic (для моделей JSON)
    Таблицы (Модели):
        WatchedProfile:
            ProfileID - PK, Unique
            LastAssetID (default 0/Null)
            isWatching
            LastModifiedDate
            TotalAmount - общий "банк" за открытие
            TotalCount - количество предметов за открытие

        DropDetail:
            ProfileID
            AssetID
            ClassID
            InstanceID
            Name - (Name)
            MarketName (на всякий случай)
            Type (tags->[1 (category = 'Type')]->localized_tag_name) Оружие (например наклейка или винтовка)
            Опционально Weapon (tags->[1 (category = 'Weapon')]->localized_tag_name) Тип предмета (например М4А4)
            Опционально Exterior (tags->[5 (category = 'Exterior')]->localized_tag_name) - Состояние (например немного поношеное)
            Rarity (tags->[5 (category = 'Rarity')]->color) - цвет предмета (в HEX)
            Price
            Float (не знаем как получить)
            ImageURL
            isShow (флаг вывода на экран, default=False)

    Worker:
        Технология: Celery
    
    Server
        Технология: FastAPI
        Сервер принимающий запросы:
            ? - Регистрация профиля - в теле запроса передаем ProfileID
                Создать запись в таблице WatchedProfile
            - Запустить подсчет кейсов/капсул - обновление записи в WatchedProfile c заданным ProfileID - LastAssetID 
                полученным из нового запроса получения предмета, и isWatching = True - Отправка метода наблюдения в Celery
            - Остановить подсчет кейсов/капсул - обновление записи c заданным ProfileID - isWatching = False
            - Получение непросмотренных предметов: 
                Из таблицы DropDetail берем записи с заданным ProfileID и isShow = False
            - Страница (шаблон) для вывода информации о последнем предмете и общем "банке"
            - Страница (шаблон) для настройки и управления наблюдением