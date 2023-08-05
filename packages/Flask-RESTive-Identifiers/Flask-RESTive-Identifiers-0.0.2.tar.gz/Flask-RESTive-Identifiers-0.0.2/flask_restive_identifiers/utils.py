# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_restive_identifiers.services import Service


def generate_id(namespace):
    """
    Generate next value of the counter.

    :param namespace: counter name
    :type namespace: str
    :return: next counter value
    :rtype int
    """
    with Service(namespace) as service:
        nextid = service.generate_id()
    return nextid
