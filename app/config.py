from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Majors API"
    app_version: str = "1.0.0"
    mongodb_url: str = "mongodb://root:password123@localhost:27017/majors?authSource=admin"
    database_name: str = "majors"

settings = Settings()
