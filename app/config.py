import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Notice we are using the new psycopg driver here
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg://postgres:postgres@localhost:5432/retail_inventory"
    )

class DevelopmentConfig(Config):
    DEBUG = True

config_by_name = {
    "development": DevelopmentConfig
}