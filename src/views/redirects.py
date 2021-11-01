from flask import Blueprint, redirect, abort

from src import db
from src.api.models import Url

redirects_bp = Blueprint('redirects', __name__)


@redirects_bp.route('/<path:path>')
def redirect_to_target(path):
    if target_url := db.session.query(Url.target_url).filter_by(custom_name=path).scalar():
        return redirect(target_url)
    else:
        abort(404, 'Url not found')
