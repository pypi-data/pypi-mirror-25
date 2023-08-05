from jsonapidb import serialization
from jsonapidb import model as models
from jsonapidb.builders.scrambler import egg
from jsonapidb.serialization.deserialiers.entity_instance_deserializers import SingleEntityInstanceDeserializerFactory
from jsonapidb.serialization.deserialiers.relation_instance_deserializers import SingleRelationInstanceDeserializerFactory
from jsonapidb.serialization.serializers.entity_instance_serializers import EntityInstanceSerializerFactory
from jsonapidb.serialization.serializers.dedicated import GetSingleObjectSerializerFactory, FindAllItemsSerializerFactory
from .errors_context_producers import ContextProducerWithErrorHandling
from .errors_context_producers import EntitiesInRequestAndUrlDoNotMatch
from .errors_context_producers import PrimaryKeysInRequestAndUrlDoNotMatch


@egg
class CreateItemContextProducer:
    def __init__(self, model: models.Model,
                 deserializer_factory: SingleEntityInstanceDeserializerFactory,
                 serializer_factory: EntityInstanceSerializerFactory):
        self.deserializer_factory = deserializer_factory
        self.serializer_factory = serializer_factory
        self.model = model

    def get_context(self, request_context) -> dict:
        entity_instance = self.deserializer_factory.create(request_context.body).deserialize()

        if entity_instance.meta.name != request_context.resource_name:
            raise EntitiesInRequestAndUrlDoNotMatch(entity_instance.meta.name, request_context.resource_name)

        created_entity_instance = self.model.create(entity_instance)
        body = self.serializer_factory.create(request_context).serialize_single(created_entity_instance)
        context = {
            'body': body,
            'status': 201
        }
        return context


@egg
class CreateItemContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: CreateItemContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class DeleteItemContextProducer:
    def __init__(self, model: models.Model):
        self.model = model

    def get_context(self, request_context) -> dict:
        self.model.delete(request_context.resource_name, request_context.params['pk'])
        context = {
            'body': None,
            'status': 200
        }
        return context


@egg
class DeleteItemContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: DeleteItemContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class UpdateItemContextProducer:
    def __init__(self, deserializer_factory: SingleEntityInstanceDeserializerFactory,
                 model: models.Model):
        self.deserializer_factory = deserializer_factory
        self.model = model

    def get_context(self, request_context) -> dict:
        entity_instance = self.deserializer_factory.create(request_context.body).deserialize()

        if entity_instance.meta.name != request_context.resource_name:
            raise EntitiesInRequestAndUrlDoNotMatch(entity_instance.meta.name, request_context.resource_name)
        if entity_instance.pk is not None and entity_instance.pk != request_context.params['pk']:
            raise PrimaryKeysInRequestAndUrlDoNotMatch(entity_instance.pk, request_context.params['pk'])

        self.model.update(entity_instance)
        context = {
            'body': None,
            'status': 204
        }
        return context


@egg
class UpdateItemContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: UpdateItemContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class GetSingleObjectContextProducer:
    def __init__(self, model: models.Model,
                 serializer_factory: GetSingleObjectSerializerFactory):
        self.model = model
        self.serializer_factory = serializer_factory

    def get_context(self, request_context) -> dict:
        get_single_object_dto = self.model.find_one(request_context.resource_name, request_context.params['pk'],
                                                                  request_context.included_relations)
        context = {
            'body': self.serializer_factory.create(request_context).serialize(
                get_single_object_dto.entity_instance,
                get_single_object_dto.included_instances
            ),
            'status': 200
        }
        return context


@egg
class GetSingleItemContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: GetSingleObjectContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class FindAllItemsContextProducer:
    def __init__(self, model: models.Model,
                 serializer_factory: FindAllItemsSerializerFactory):
        self.model = model
        self.serializer_factory = serializer_factory

    def get_context(self, request_context) -> dict:
        find_all_objects_dto = self.model.find_all(request_context.resource_name, request_context.included_relations)

        serialized_entity_instances = self.serializer_factory.create(request_context).serialize(
            find_all_objects_dto.entity_instances,
            find_all_objects_dto.included_instances
        )

        context = {
            'body': serialized_entity_instances,
            'status': 200
        }
        return context


@egg
class FindAllItemsContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: FindAllItemsContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class FindRelationContextProducer:
    def __init__(self, relation_instance_serializer_factory: serialization.SingleRelationInstanceSerializerFactory,
                 model: models.Model):
        self.relation_instance_serializer_factory = relation_instance_serializer_factory
        self.model = model

    def get_context(self, request_context) -> dict:
        relation = self.model.find_relation(
            request_context.resource_name,
            request_context.params['pk'],
            request_context.params['relation_name']
        )
        relation_instance_serializer = self.relation_instance_serializer_factory\
            .create(relation, request_context)
        return {
            'body': relation_instance_serializer.serialize_to_final_form(),
            'status': 200
        }


@egg
class FindRelationContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: FindRelationContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)


@egg
class UpdateRelationContextProducer:
    def __init__(self, single_relation_instance_deserializer_factory: SingleRelationInstanceDeserializerFactory,
                 model: models.Model):
        self.single_relation_instance_deserializer_factory = single_relation_instance_deserializer_factory
        self.model = model

    def get_context(self, request_context) -> dict:
        entity_instance = self.single_relation_instance_deserializer_factory\
            .create(request_context.resource_name,
                    request_context.params['pk'],
                    request_context.params['relation_name'],
                    request_context.body)\
            .deserialize()
        self.model.update_relation(entity_instance)

        return {
            'body': None,
            'status': 204
        }


@egg
class UpdateRelationContextProducerWithErrorHandling(ContextProducerWithErrorHandling):
    def __init__(self, context_producer: UpdateRelationContextProducer,
                 single_error_serializer_factory: serialization.SingleErrorSerializerFactory,
                 multiple_error_serializer_factory: serialization.MultipleErrorSerializerFactory):
        super().__init__(context_producer, single_error_serializer_factory, multiple_error_serializer_factory)