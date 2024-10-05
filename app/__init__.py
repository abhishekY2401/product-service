# app/__init__.py
from flask import Flask  # type: ignore
from config import Config
from app.extensions import db, jwt, bcrypt, migrate
from app.graphql import graphql_server, graphql_playground
import logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register GraphQL routes
    app.add_url_rule('/graphql',
                     view_func=graphql_playground, methods=['GET'])
    app.add_url_rule('/graphql', view_func=graphql_server, methods=['POST'])

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    return app
