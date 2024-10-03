from functools import wraps

from flask import abort, request

from service.account import AccountService


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        api_key = request.headers.get("api_key")
        account_service = AccountService()
        account = account_service.get_account_by_api_key(api_key)
        if not account:
            abort(401, description="Unauthorized.")
        request.account = account
        return f(*args, **kwargs)

    return wrap
