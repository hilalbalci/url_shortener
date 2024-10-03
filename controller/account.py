from flask import Blueprint, abort, jsonify, request

from service.account import AccountService

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/account", methods=["POST"])
def create_account():
    data = request.json
    account_service = AccountService()
    account = account_service.create_account(name=data.get("name"))
    return jsonify({"api_key": account.api_key}), 201


@account_blueprint.route("/account/<string:account_id>", methods=["PUT"])
def update_account(account_id):
    data = request.json
    daily_limit = data.get("daily_limit")
    account_service = AccountService()
    account = account_service.update_account(
        account_id=account_id, daily_limit=daily_limit
    )
    if account:
        return jsonify({"message": "Account has been updated"}), 200
    abort(404, description="Account was not found.")
