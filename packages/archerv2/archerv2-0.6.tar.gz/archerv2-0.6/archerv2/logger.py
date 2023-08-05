# -*- coding: utf-8 -*-
import logging

base_logger = logging.getLogger('archerv2')


def log(type, message, *args, **kwargs):
    """Log into archerv2 logger.
     Only set up a default log handler if the
     end-user application didn't set anything up.
     """
    if not logging.root.handlers and base_logger.level == logging.NOTSET:
        base_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        base_logger.addHandler(handler)
    getattr(base_logger, type)(message.rstrip(), *args, **kwargs)
