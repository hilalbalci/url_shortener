from unittest.mock import patch

import pytest
from flask import json

from app import app
from configurations import db, redis_client
from models import Account, ShortenedUrl


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            test_account = Account(
                api_key="test_api_key", daily_limit=50, name="test_name"
            )
            db.session.add(test_account)
            db.session.commit()

            shortened_url = ShortenedUrl(
                url="https://www.google.com",
                account_id=test_account.id,
                shortened_url="123abc",
            )
            db.session.add(shortened_url)
            db.session.commit()

        yield testing_client

        with app.app_context():
            db.drop_all()


@pytest.fixture
def clear_redis():
    redis_client.flushdb()


@patch("utils.login_required", lambda x: x)
def test_shorten_url(client, clear_redis):
    payload = {"url": "https://www.google.com"}
    headers = {"API_KEY": "test_api_key"}
    response = client.post(
        "/shorten_url",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert "short_url" in response_data
    assert redis_client.get(response_data["short_url"]) == "https://www.google.com"


def test_shorten_url_unauthorized(client, clear_redis):
    payload = {"url": "https://www.google.com"}
    headers = {}
    response = client.post(
        "/shorten_url",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 401


def test_redirect_to_original(client, clear_redis):
    redis_client.set("123abc", "https://www.google.com")
    headers = {"API_KEY": "test_api_key"}
    response = client.get("/123abc", headers=headers)
    assert response.status_code == 302
    assert response.location == "https://www.google.com"


def test_shorten_url_validation_error(client, clear_redis):
    payload = {}
    headers = {"API_KEY": "test_api_key"}
    response = client.post(
        "/shorten_url",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert "errors" in response_data


def test_redirect_url_not_found(client, clear_redis):
    headers = {"API_KEY": "test_api_key"}
    response = client.get("/nonexistent", headers=headers)
    assert response.status_code == 404
