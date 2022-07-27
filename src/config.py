from pydantic import Field, BaseSettings


class ApplicationSettings(BaseSettings):
    BACKEND_URL: str = Field(env='BACKEND_URL')
    DB_HOST: str = Field(env='DB_HOST')
    DB_PORT: int = Field(env='DB_PORT')
    DB_BASENAME: str = Field(env='DB_BASENAME')
    DB_USERNAME: str = Field(env='DB_USERNAME')
    DB_PASSWORD: str = Field(env='DB_PASSWORD')
    DB_PROTOCOL: str = Field(env='DB_PROTOCOL')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(env='JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
    JWT_SECRET: str = Field(env='JWT_SECRET')
    JWT_ALGORITHM: str = Field(env='JWT_ALGORITHM')

    @property
    def dsn(self):
        dsn = f"{self.DB_PROTOCOL}://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
              f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASENAME}"
        return dsn

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings_app = ApplicationSettings()
