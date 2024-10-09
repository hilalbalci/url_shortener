from flask import Blueprint, abort, jsonify, request
from marshmallow import ValidationError

from schemas import AccountSchema
from service.account import AccountService

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/account", methods=["POST"])
def create_account():
    account_schema = AccountSchema()
    try:
        data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    account_service = AccountService()
    account = account_service.create_account(
        name=data.get("name"), daily_limit=data.get("daily_limit")
    )
    return jsonify(
        {
            "id": account.id,
            "name": account.name,
            "api_key": account.api_key,
            "daily_limit": account.daily_limit,
        }
    ), 201


@account_blueprint.route("/account/<string:account_id>", methods=["PUT"])
def update_account(account_id):
    account_schema = AccountSchema()
    try:
        data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    daily_limit = data.get("daily_limit")
    name = data.get("name")
    account_service = AccountService()
    account = account_service.update_account(
        account_id=account_id, daily_limit=daily_limit, name=name
    )
    if account:
        return jsonify(
            {
                "id": account.id,
                "name": account.name,
                "api_key": account.api_key,
                "daily_limit": account.daily_limit,
            }
        ), 200
    abort(404, description="Account was not found.")


@account_blueprint.route("/account/<string:account_id>", methods=["GET"])
def get_account(account_id):
    account_service = AccountService()
    account = account_service.get_account_by_id(account_id)
    if account:
        return jsonify(
            {
                "id": account.id,
                "name": account.name,
                "api_key": account.api_key,
                "daily_limit": account.daily_limit,
            }
        ), 200
    abort(404, description="Account was not found.")
