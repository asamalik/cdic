# coding: utf-8


import sys
import time
import logging

log = logging.getLogger(__name__)


from cdic.app import app
from cdic.util import setup_logging
from cdic.app.util.dockerhub import Creator

logging.basicConfig(
    filename="/tmp/try_dockerhub.log",
    # stream=sys.stdout,
    # format='[%(asctime)s][%(name)s][PID: %(process)d][%(levelname)6s]: %(message)s',
    format='[%(asctime)s][%(levelname)6s][%(name)s]: %(message)s',
    level=logging.DEBUG
    # level=logging.INFO
)


def main(lst):
    cr = Creator(app.config, lst)
    return cr


if __name__ == "__main__":
    main(['t1', 't2', 't3'])
