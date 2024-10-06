import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBITMQ_URL = os.environ['RABBITMQ_URI']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    PRODUCT_CREATED_QUEUE = 'product.created'
    INVENTORY_UPDATED_QUEUE = 'inventory.updated'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
