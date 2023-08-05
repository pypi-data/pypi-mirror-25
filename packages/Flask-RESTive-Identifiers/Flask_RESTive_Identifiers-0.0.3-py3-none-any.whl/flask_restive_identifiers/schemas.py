# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from marshmallow.validate import Range
from flask_restive import DataSchema, fields
from flask_restive.utils import decapitalize

from flask_restive_identifiers.utils import generate_id


class IntegerIDSchema(DataSchema):
    """
    Provides auto-increment id. The counter name can be
    changed with meta attribute identifier_namespace.
    """
    id = fields.Integer(required=True, validate=Range(min=1))

    class Meta(DataSchema.Meta):
        identifier_namespace = None
        primary_key_fields = ('id',)
        sortable_fields = ('id',)
        default_sorting = ('id',)

    def __init__(self, *args, **kwargs):
        super(IntegerIDSchema, self).__init__(*args, **kwargs)
        self._set_identifier_namespace()
        self._set_id_generator()

    def _set_identifier_namespace(self):
        if not self.opts.identifier_namespace:
            self.opts.identifier_namespace = decapitalize(
                self.__class__.__name__)

    def _set_id_generator(self):
        self.fields['id'].missing = self.generate_id
        self.declared_fields['id'].missing = self.generate_id

    def generate_id(self):
        return generate_id(self.opts.identifier_namespace)
