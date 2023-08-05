from jsonapidb import model as models
from jsonapidb import serialization
from jsonapidb.model.domain import RelationNotFound, EntityNotFound, InvalidRelationType

ERROR_META = {
    'EntityNotFound': {
        'code': 100,
        'title': 'Entity does not exists'
    },
    'EntityDoesNotExist': {
        'code': 100,
        'title': 'Entity does not exists'
    },
    'ItemWithGivenPkDoesNotExist': {
        'code': 101,
        'title': 'Item with given pk does not exist'
    },
    'RelationNotFound': {
        'code': 102,
        'title': 'Relation does not exist'
    },
    'RelationDoesNotExist': {
        'code': 102,
        'title': 'Relation does not exist'
    },
    'InvalidRelatedType': {
        'code': 103,
        'title': 'Invalid related item type'
    },
    'InvalidRelationType': {
        'code': 104,
        'title': 'Invalid relation type'
    },
    'RelatedItemWithGivenPkDoesNotExist': {
        'code': 105,
        'title': 'Related item with given pk does not exist'
    },
    'InvalidItemAttributes': {
        'code': 106,
        'title': 'Attribute error'
    },
    'InvalidFormat': {
        'code': 107,
        'title': 'Invalid data format'
    },
    'EntitiesInRequestAndUrlDoNotMatch': {
        'code': 108,
        'title': 'Entities in request body and url do not match'
    }
}


class EntitiesInRequestAndUrlDoNotMatch(Exception):
    def __init__(self, entity_name_found_in_body, entity_name_found_in_url):
        super().__init__("Found in body: '{entity_name_found_in_body}', found in url: '{entity_name_found_in_url}'"
                         .format(entity_name_found_in_body=entity_name_found_in_body,
                                 entity_name_found_in_url=entity_name_found_in_url))


class PrimaryKeysInRequestAndUrlDoNotMatch(Exception):
    def __init__(self, pk_found_in_body, pk_found_in_url):
        super().__init__("Found in body: '{pk_found_in_body}', found in url: '{pk_found_in_url}'"
                         .format(pk_found_in_body=pk_found_in_body,
                                 pk_found_in_url=pk_found_in_url))


class Error:
    def __init__(self, code, title, details, path=None):
        self.code = code
        self.title = title
        self.details = details
        self.path = path

    @classmethod
    def from_model_exception(cls, exception_name, details, path=None):
        meta = ERROR_META[exception_name]
        return cls(details=details, path=path, **meta)


class ContextProducerWithErrorHandling:
    NOT_FOUND_ERRORS = (EntityNotFound, models.ItemWithGivenPkDoesNotExist, RelationNotFound,
                        models.RelatedItemWithGivenPkDoesNotExist, models.EntityDoesNotExist, models.RelationDoesNotExist)
    INVALID_REQUEST_ERRORS = (models.InvalidRelatedType, InvalidRelationType, serialization.InvalidFormat,
                              EntitiesInRequestAndUrlDoNotMatch, models.InvalidRelationType)

    def __init__(self, context_producer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        self.context_producer = context_producer
        self.single_error_serializer_factory = single_error_serializer_factory
        self.multiple_error_serializer_factory = multiple_error_serializer_factory

    def get_context(self, *args, **kwargs):
        try:
            return self.context_producer.get_context(*args, **kwargs)
        except self.NOT_FOUND_ERRORS as e:
            return self._handle_error(404, str(e), type(e).__name__)
        except self.INVALID_REQUEST_ERRORS as e:
            return self._handle_error(400, str(e), type(e).__name__)
        except models.InvalidItemAttributes as e:
            return self._handle_attributes_error(400, e.errors)
        except Exception as e:
            raise e
            print(e)
            print(type(e))
            return self.handle_server_error()

    def _handle_error(self, status, details, error_name):
        error = Error.from_model_exception(error_name, details)
        body = self.single_error_serializer_factory.create(error).serialize()
        context = {
            'body': body,
            'status': status
        }
        return context

    def _handle_attributes_error(self, status, attributes_errors):
        errors = []
        for attr_name, attr_errors in attributes_errors.items():
            for e in attr_errors:
                errors.append(Error.from_model_exception('InvalidItemAttributes', e, '/'.join(['attributes', attr_name])))

        body = self.multiple_error_serializer_factory.create(errors).serialize()

        return {
            'body': body,
            'status': status
        }

    @staticmethod
    def _handle_server_error():
        return {
            'body': '',
            'status': 500
        }