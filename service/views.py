from flask import Blueprint, jsonify
from . import db


bp = Blueprint(name='secret-number-blueprint',
               import_name=__name__,
               url_prefix='/')


@bp.route('/return_secret_number', methods=['GET'])
def handler():
    return jsonify({'secret_number': db.secret_number})

