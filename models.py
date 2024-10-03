from datetime import datetime

from configurations import db


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    api_key = db.Column(db.String, unique=True)
    daily_limit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ShortenedUrl(db.Model):
    __tablename__ = "shortened_urls"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    url = db.Column(db.String, nullable=False)
    shortened_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'original_url': self.url,
            'short_url': self.shortened_url,
            'created_at': self.created_at.isoformat(),
            'click_count': self.click_count
        }
