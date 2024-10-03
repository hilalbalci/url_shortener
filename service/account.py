import random
import string

from db import db
from models import Account


class AccountService:
    @staticmethod
    def generate_api_key():
        return "".join(random.choices(string.ascii_letters + string.digits, k=30))

    def create_account(self, name, daily_limit):
        api_key = self.generate_api_key()
        account = Account(name=name, api_key=api_key, daily_limit=daily_limit)
        db.session.add(account)
        db.session.commit()
        return account

    def update_account(self, account_id, daily_limit):
        account = self.get_account_by_id(account_id)
        if account:
            account.daily_limit = daily_limit
            db.session.add(account)
            db.session.commit()
        return account

    def get_account_by_api_key(self, api_key):
        return Account.query.filter_by(api_key=api_key).first()

    def get_account_by_id(self, account_id):
        return Account.query.get(account_id)
