import json

from jsonapidb.builders.scrambler import egg


class SingleErrorSerializer:
    def __init__(self, error):
        self.error = error

    def serialize(self):
        serialized_error = self.serialize_to_raw_form()
        return json.dumps({'errors': serialized_error})

    def serialize_to_raw_form(self):
        serialized_error = dict(code=self.error.code, title=self.error.title, details=self.error.details)
        if self.error.path:
            serialized_error['path'] = self.error.path
        return serialized_error


@egg
class SingleErrorSerializerFactory:
    @staticmethod
    def create(error):
        return SingleErrorSerializer(error)


class MultipleErrorSerializer:
    def __init__(self, errors, single_error_serializer_factory: SingleErrorSerializerFactory):
        self.errors = errors
        self.single_error_serializer_factory = single_error_serializer_factory

    def serialize(self):
        serialized_errors = []
        for error in self.errors:
            serializer = self.single_error_serializer_factory.create(error)
            serialized_errors.append(serializer.serialize_to_raw_form())
        return json.dumps({'errors': serialized_errors})


@egg
class MultipleErrorSerializerFactory:
    def __init__(self, single_item_serializer_factory: SingleErrorSerializerFactory):
        self.single_item_serializer_factory = single_item_serializer_factory

    def create(self, errors):
        return MultipleErrorSerializer(errors, self.single_item_serializer_factory)
