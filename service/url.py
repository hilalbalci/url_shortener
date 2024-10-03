import string
from datetime import datetime
from random import choice

import validators
from flask import abort
from sqlalchemy import func

from configurations import db
from models import ShortenedUrl


class UrlService:
    def shorten_url(self, account, url):
        self.validate_url(url)
        today = datetime.utcnow().date()
        today_count = ShortenedUrl.query.filter(
            ShortenedUrl.account_id == account.id,
            func.date(ShortenedUrl.created_at) == today,
        ).count()

        if today_count >= account.daily_limit:
            abort(
                400,
                description="You have exceeded your daily limit of shortening urls.",
            )

        shortened_url_obj = ShortenedUrl.query.filter_by(
            url=url, account_id=account.id
        ).first()
        if not shortened_url_obj:
            short_url = UrlService.create_short_url()
            shortened_url_obj = ShortenedUrl(
                shortened_url=short_url, url=url, account_id=account.id
            )
            db.session.add(shortened_url_obj)
            db.session.commit()
        return shortened_url_obj.shortened_url

    @staticmethod
    def create_short_url():
        return "".join(choice(string.ascii_letters + string.digits) for _ in range(10))

    @staticmethod
    def validate_url(url):
        if not validators.url(url):
            abort(400, description="Url is not valid")

    def get_url_obj_by_short_url(self, short_url):
        return ShortenedUrl.query.filter_by(shortened_url=short_url).first()

    def click(self, short_url):
        url = self.get_url_obj_by_short_url(short_url)
        url.click_count += 1
        db.session.add(url)
        db.session.commit()

    def get_analytics(self, account):
        shortened_urls = ShortenedUrl.query.filter_by(account_id=account.id).all()
        return [url.to_dict() for url in shortened_urls]

