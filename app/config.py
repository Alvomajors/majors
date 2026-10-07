from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Majors API"
    app_version: str = "1.0.0"
    mongodb_url: str = "mongodb://root:password123@localhost:27017/majors?authSource=admin"
    database_name: str = "majors"
    secret_key: str = "super-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    ethereum_rpc_url: str = "http://localhost:8545"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
