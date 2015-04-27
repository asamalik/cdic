# coding: utf-8

import os

DEBUG = True

ADMINS = frozenset(['nobody@example.com'])
SECRET_KEY = 'This string will be replaced with a proper key in production.'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join("/tmp", 'cdic', 'app.db')
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"

OPENID_STORE = "/tmp/cdic/openid/"
CDIC_WORKPLACE = "/tmp/cdic/wp"

DOCKERHUB_URL = 'https://hub.docker.com'
DOCKERREGISTRY_URL = 'https://registry.hub.docker.com'
DOCKERHUB_USERNAME = 'FILL DOCKER USERNAME'
DOCKERHUB_PASSWORD = 'FILL DOCKER PASSWORD'
HUB_PROJECT_URL_TEMPLATE = "http://registry.hub.docker.com/u/FILL DOCKER USERNAME AGAIN/cdic-{username}-{project_id}"

GITHUB_TOKEN = "FILL GITHUB TOKEN"
GITHUB_USER = "FILL GITHUB USER"
GITHUB_API_ROOT = "https://api.github.com"
GITHUB_URL = "https://github.com"

COPR_BASE_URL = "https://copr.fedoraproject.org"
