import string
from datetime import datetime
from random import choice

import validators
from flask import abort
from sqlalchemy import func

from db import db
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

        shortened_url = ShortenedUrl.query.filter_by(
            url=url, account_id=account.id
        ).first()
        if not shortened_url:
            short_url = UrlService.create_short_url()
            shortened_url = ShortenedUrl(
                shortened_url=short_url, url=url, account_id=account.id
            )
            db.session.add(shortened_url)
            db.session.commit()
        return shortened_url

    @staticmethod
    def create_short_url():
        return "".join(choice(string.ascii_letters + string.digits) for _ in range(10))

    @staticmethod
    def validate_url(url):
        if not validators.url(url):
            abort(400, description="Url is not valid")

    def get_original_url(self, short_url):
        return ShortenedUrl.query.filter_by(shortened_url=short_url).first()

    def click(self, url_obj):
        url = ShortenedUrl.query.get(url_obj.id)
        url.click_count += 1
        db.session.add(url)
        db.session.commit()
