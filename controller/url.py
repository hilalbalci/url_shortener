from flask import Blueprint, abort, jsonify, redirect, request
from marshmallow import ValidationError

from configurations import redis_client
from schemas import UrlSchema
from service.url import UrlService
from utils import login_required

url_blueprint = Blueprint("url", __name__)


@url_blueprint.route("/shorten_url", methods=["POST"])
@login_required
def shorten_url():
    url_schema = UrlSchema()
    try:
        data = url_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    url_service = UrlService()
    shortened_url = url_service.shorten_url(
        account=request.account, url=data.get("url")
    )
    redis_client.set(shortened_url, data.get("url"))
    return jsonify({"short_url": shortened_url}), 201


@url_blueprint.route("/<string:short_url>", methods=["GET"])
@login_required
def redirect_url(short_url):
    original_url = redis_client.get(short_url)
    url_service = UrlService()

    if original_url:
        url_service.click(short_url)
        return redirect(original_url)

    url_obj = url_service.get_url_obj_by_short_url(short_url)
    if not url_obj:
        abort(404, description="Url can not be found.")
    url_service.click(short_url)
    redis_client.set(short_url, url_obj.url)
    return redirect(url_obj.url)
