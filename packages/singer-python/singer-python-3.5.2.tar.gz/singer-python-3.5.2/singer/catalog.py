'''Provides an object model for a Singer Catalog.'''

import json
import sys

from singer.schema import Schema


class CatalogEntry(object):

    def __init__(self, tap_stream_id=None, stream=None,
                 key_properties=None, schema=None, replication_key=None,
                 is_view=None, database_name=None, table_name=None, row_count=None,
                 stream_alias=None):

        self.tap_stream_id = tap_stream_id
        self.stream = stream
        self.key_properties = key_properties

        # force Schema instance
        if not isinstance(schema, Schema):
            schema = Schema.from_dict(schema)
        self.schema = schema

        self.replication_key = replication_key
        self.is_view = is_view
        self.database_name = database_name
        self.table_name = table_name
        self.row_count = row_count
        self.stream_alias = stream_alias

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def is_selected(self):
        return self.schema.selected

    def to_dict(self):
        result = {}
        if self.tap_stream_id:
            result['tap_stream_id'] = self.tap_stream_id
        if self.database_name:
            result['database_name'] = self.database_name
        if self.table_name:
            result['table_name'] = self.table_name
        if self.replication_key is not None:
            result['replication_key'] = self.replication_key
        if self.key_properties is not None:
            result['key_properties'] = self.key_properties
        if self.schema is not None:
            schema = self.schema.to_dict()
            result['schema'] = schema
        if self.is_view is not None:
            result['is_view'] = self.is_view
        if self.stream is not None:
            result['stream'] = self.stream
        if self.row_count is not None:
            result['row_count'] = self.row_count
        if self.stream_alias is not None:
            result['stream_alias'] = self.stream_alias
        return result


class Catalog(object):

    def __init__(self, streams=None):
        self.streams = streams or []

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def load(cls, filename):
        with open(filename) as fp:
            return Catalog.from_dict(json.load(fp))

    @classmethod
    def from_dict(cls, data):
        return cls(CatalogEntry(**stream) for stream in data['streams'])

    def to_dict(self):
        return {'streams': [stream.to_dict() for stream in self.streams]}

    def dump(self):
        json.dump(self.to_dict(), sys.stdout, indent=2)

    def get_stream(self, tap_stream_id):
        for stream in self.streams:
            if stream.tap_stream_id == tap_stream_id:
                return stream
        return None
