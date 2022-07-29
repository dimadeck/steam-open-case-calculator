from pydantic import Field, BaseSettings


class ApplicationSettings(BaseSettings):
    BACKEND_URL: str = Field(env='BACKEND_URL')
    BACKEND_TOKEN: str = Field(env='BACKEND_TOKEN')
    DB_HOST: str = Field(env='DB_HOST')
    DB_PORT: int = Field(env='DB_PORT')
    DB_BASENAME: str = Field(env='DB_BASENAME')
    DB_USERNAME: str = Field(env='DB_USERNAME')
    DB_PASSWORD: str = Field(env='DB_PASSWORD')
    DB_PROTOCOL: str = Field(env='DB_PROTOCOL')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(env='JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=60*24*30)
    JWT_SECRET: str = Field(env='JWT_SECRET')
    JWT_ALGORITHM: str = Field(env='JWT_ALGORITHM', default='HS256')
    LOG_LEVEL: str = Field(env='LOG_LEVEL', default='info')
    LOG_FILENAME: str = Field(env='LOG_FILENAME', default='SOCC.log')
    LOG_CONSOLE: str = Field(env='LOG_CONSOLE', default=False)
    OBSERVER_WAITING_TIME: int = Field(env='OBSERVER_WAITING_TIME', default=5)
    CELERY_BROKER_URL: str = Field(env='CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: str = Field(env='CELERY_RESULT_BACKEND')
    REDIS_NEW_ITEM_CHANNEL: str = Field(env='REDIS_NEW_ITEM_CHANNEL')
    REDIS_PUB_SUB_URL: str = Field(env='REDIS_PUB_SUB_URL')

    @property
    def dsn(self):
        dsn = f"{self.DB_PROTOCOL}://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
              f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASENAME}"
        return dsn

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings_app = ApplicationSettings()
