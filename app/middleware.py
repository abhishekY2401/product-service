import jwt
from ariadne import MutationType, QueryType
from flask import request, jsonify
from graphql import GraphQLError
from config import Config


def jwt_required(f):
    def wrapper_resolver(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization', '')

        # Check if Authorization header is provided and follows "Bearer <token>" format
        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "success": False,
                "message": "Authorization header missing.",
                "user": None
            }

        try:
            # Extract the token after "Bearer "
            token = auth_header.split("Bearer ")[1]

            # Decode the JWT token using the secret key
            decoded_token = jwt.decode(
                token, Config.JWT_SECRET_KEY, algorithms=['HS256'])

            # Attach the decoded token to the request context, so it can be used later
            request.user = decoded_token

        except IndexError:
            return {
                "success": False,
                "message": "Token format invalid. Expected 'Bearer <token>'.",
                "user": None
            }

        except jwt.ExpiredSignatureError:
            return {
                "success": False,
                "message": "Token has expired.",
                "user": None
            }

        except jwt.InvalidTokenError:
            return {
                "success": False,
                "message": "Invalid token.",
                "user": None
            }

        # Continue with the resolver if the token is valid
        return f(*args, **kwargs)

    return wrapper_resolver
