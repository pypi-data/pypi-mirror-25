# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    import psycopg2  # pylint: disable=unused-import
except ImportError:
    from psycopg2cffi import compat
    compat.register()

from sqlalchemy import Sequence
from flask_restive_sqlalchemy.services import Service as BaseService


class Service(BaseService):
    """
    Sequence service. Provides method
    to generate next counter id value.
    The namespace is mandatory parameter,
    each namespace has independent counter.
    """

    def __init__(self, namespace, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.seq_name = namespace + '_id_seq'
        self.sequence = None

    def open(self):
        super(Service, self).open()
        self.sequence = Sequence(
            self.seq_name, metadata=self.metadata)
        self.sequence.create()

    def reset(self, value=0):
        """
        Reset sequence counter.
        :param value: new value of the sequence counter
        :type value: int
        """
        self.sequence.drop()
        self.sequence = Sequence(self.seq_name, start=value + 1,
                                 metadata=self.metadata)
        self.sequence.create()

    def generate_id(self):
        next_id = self.connection.execute(self.sequence)
        return next_id
