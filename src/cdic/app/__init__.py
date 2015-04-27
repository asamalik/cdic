# coding: utf-8

import os
import sys
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

sys.path.append("..")
from cdic.util.git import GitStore

app = Flask(__name__)

# oid = OpenID(app, app.config["OPENID_STORE"], safe_roots=[])
app.config.from_pyfile("../config.py")
app.config.from_pyfile(os.path.expanduser("~/.config/cdic.py"))

Bootstrap(app)

git_store = GitStore(app.config["CDIC_WORKPLACE"])

db = SQLAlchemy()
db.init_app(app)

from .filters import time_ago

from .views.main import main_bp
from .views.auth import auth_bp
from .views.copr import copr_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(copr_bp)

@app.route('/api/help', methods=['GET'])
def help_urls():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', error=error), 404
