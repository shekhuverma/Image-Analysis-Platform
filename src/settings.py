from pydantic_settings import BaseSettings, SettingsConfigDict

REDIS_EXPIRY = 60 * 60 * 24 * 7

# List of supported image formats for processing
# Can be adjusted as per need
SUPPORTED_FILE_FORMATS = ("jpeg", "jpg", "png")


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    DEBUG: bool = True

    BASEUSER: str = "user"
    BASEUSER_EMAIL: str = "user@example.com"
    BASEUSER_PASSWORD: str = "password"

    REDIS_HOST: str = "127.0.0.1"


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    USER: str = "postgres"
    PASSWORD: str = ""
    SERVER: str = "localhost"
    PORT: str = "5432"
    DB: str = "app"

    @property
    def get_db_url(self):
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.SERVER}:{self.PORT}/{self.DB}"


class JWTconfig(BaseSettings):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "9ebde6d2b2e67230fa346e926bbbdf64eee1c0baaf7b3db6d14d8890aff26066"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALGORITHM: str = "HS256"

    # model_config = SettingsConfigDict(case_sensitive=True)


# def get_db_url():
#     user = os.getenv("POSTGRES_USER", "postgres")
#     password = os.getenv("POSTGRES_PASSWORD", "")
#     server = os.getenv("POSTGRES_SERVER", "localhost")
#     port = os.getenv("POSTGRES_PORT", "5432")
#     db = os.getenv("POSTGRES_DB", "app")

#     return f"postgresql://{user}:{password}@{server}:{port}/{db}"


JWT_config = JWTconfig()
database_config = DatabaseConfig()
config = Config()
