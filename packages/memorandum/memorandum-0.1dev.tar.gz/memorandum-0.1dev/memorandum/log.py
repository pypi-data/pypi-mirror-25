# -*- coding: utf-8 -*-

###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import logging

#level="DEBUG"
#level="INFO"
level="ERROR"

fmt = "%(asctime)-4s - [%(levelname)s] %(filename)s:%(lineno)d::%(funcName)s: %(message)s (pid:%(process)d / tid:%(thread)d)"

logging.basicConfig(level=level, format=fmt)
logger = logging.getLogger()
