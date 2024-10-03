from flask import Blueprint, abort, jsonify, redirect, request
from marshmallow import ValidationError

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
    short_url = url_service.shorten_url(account=request.account, url=data.get("url"))
    return jsonify({"short_url": short_url.shortened_url}), 201


@url_blueprint.route("/<string:short_url>", methods=["GET"])
@login_required
def redirect_url(short_url):
    url_service = UrlService()
    url = url_service.get_original_url(short_url)
    if not url:
        abort(404, description="Url can not be found.")
    url_service.click(url)
    return redirect(url.url)
