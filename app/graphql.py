from flask import request, jsonify
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.explorer.apollo import APOLLO_HTML
from app.resolvers import query, mutation
from flask_jwt_extended import jwt_required
import logging

# Load the schema and create the executable schema
type_defs = load_schema_from_path("app/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)


def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        # middleware=[jwt_auth_middleware],
        debug=True
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


def graphql_playground():
    logging.info("Accessing GraphQL Playground")
    return APOLLO_HTML, 200
