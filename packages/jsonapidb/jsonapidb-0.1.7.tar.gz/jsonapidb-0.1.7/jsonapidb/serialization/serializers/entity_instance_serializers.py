import json
from typing import List

from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import EntityInstance
from jsonapidb.serialization.serializers.relation_instance_serializer import RelationInstancesSerializerFactory


class SingleEntityInstanceSerializer:
    def __init__(self, relation_instance_serializer_factory: RelationInstancesSerializerFactory, request_context):
        self.relation_instance_serializer_factory = relation_instance_serializer_factory
        self.request_context = request_context

    def serialize(self, entity_instance: EntityInstance, append_links_inside=False, append_links_outside=True,
                  serialize_with_relations=True) -> dict:
        result = {
            'data': self._serialize_to_data_json_object(entity_instance)
        }
        self._attach_pk_if_exists(entity_instance, result)
        self._attach_relations_if_required(entity_instance, result, serialize_with_relations)
        self._attach_links_if_required(entity_instance, result, append_links_inside, append_links_outside)
        return result

    def _attach_relations_if_required(self, entity_instance, result: dict, serialize_with_relations):
        serialized_relation_instances = self.relation_instance_serializer_factory \
            .create(entity_instance.relation_instances, self.request_context).serialize()

        if serialize_with_relations and serialized_relation_instances:
            result['data']['relationships'] = serialized_relation_instances
        return result

    def _attach_links_if_required(self, entity_instance, result: dict, append_links_inside, append_links_outside):
        links = {
            'self': '{root}/{path}/{pk}'
                .format(root=self.request_context.origin,
                        path=self.request_context.resource_name,
                        pk=entity_instance.pk)
        }
        if append_links_outside:
            result['links'] = links
        if append_links_inside:
            result['data']['links'] = links
        return result

    @staticmethod
    def _serialize_to_data_json_object(entity_instance) -> dict:
        result = {
            'type': entity_instance.meta.name,
            'attributes': entity_instance.attributes,
        }
        return result

    @staticmethod
    def _attach_pk_if_exists(entity_instance, result: dict):
        if entity_instance.pk is not None:
            result['data']['id'] = entity_instance.pk
        return result


@egg
class SingleEntityInstanceSerializerFactory:
    def __init__(self, relation_instance_serializer_factory: RelationInstancesSerializerFactory):
        self.relation_instance_serializer_factory = relation_instance_serializer_factory

    def create(self, request_context):
        return SingleEntityInstanceSerializer(self.relation_instance_serializer_factory, request_context)


class MultipleEntityInstanceSerializer:
    def __init__(self, single_entity_instance_serializer: SingleEntityInstanceSerializer,
                 request_context):
        self.request_context = request_context
        self.single_entity_instance_serializer = single_entity_instance_serializer

    def serialize(self, entity_instances: List[EntityInstance], append_links_inside_single_object=True,
                  append_links_outside=True, serialize_with_relations=True) -> dict:
        serialized_entity_instances = []
        for entity_instance in entity_instances:
            serialized_entity_instances.append(
                self.single_entity_instance_serializer.serialize(entity_instance, append_links_inside_single_object,
                                                                 False, serialize_with_relations)['data'])
        result = {'data': serialized_entity_instances}
        self._attach_links_if_required(result, append_links_outside)
        return result

    def _attach_links_if_required(self, result: dict, append_links_outside):
        query_string = ''
        if self.request_context.query_available:
            query_string = '?q={q}'.format(q=self.request_context.query)

        links = {
            'self': '{root}/{path}{query_string}'
                .format(root=self.request_context.origin,
                        path=self.request_context.resource_name,
                        query_string=query_string)
        }

        if append_links_outside:
            result['links'] = links
        return result


@egg
class MultipleEntityInstanceSerializerFactory:
    def __init__(self, single_entity_instance_serializer_factory: SingleEntityInstanceSerializerFactory):
        self.single_entity_instance_serializer_factory = single_entity_instance_serializer_factory

    def create(self, request_context):
        return MultipleEntityInstanceSerializer(self.single_entity_instance_serializer_factory.create(request_context),
                                                request_context)


class EntityInstanceSerializer:
    def __init__(self, single_entity_instance_serializer: SingleEntityInstanceSerializer,
                 multiple_entity_instance_serializer: MultipleEntityInstanceSerializer,
                 request_context):
        self.single_entity_instance_serializer = single_entity_instance_serializer
        self.multiple_entity_instance_serializer = multiple_entity_instance_serializer
        self.request_context = request_context

    def serialize_single(self, entity_instance: EntityInstance, append_links_inside=False,
                         append_links_outside=True, serialize_with_relations=True) -> str:
        return json.dumps(self.serialize_single_to_dict(entity_instance, append_links_inside,
                                                        append_links_outside, serialize_with_relations))

    def serialize_single_to_dict(self, entity_instance: EntityInstance, append_links_inside=False,
                                 append_links_outside=True, serialize_with_relations=True) -> dict:
        return self.single_entity_instance_serializer.serialize(entity_instance,
                                                                        append_links_inside,
                                                                        append_links_outside,
                                                                        serialize_with_relations)

    def serialize_multiple(self, entity_instances: List[EntityInstance],
                           append_links_inside_single_object=True, append_links_outside=True,
                           serialize_with_relations=True):
        return json.dumps(self.multiple_entity_instance_serializer.serialize(entity_instances,
                                                                             append_links_inside_single_object,
                                                                             append_links_outside,
                                                                             serialize_with_relations))

    def serialize_multiple_to_dict(self, entity_instances: List[EntityInstance],
                                   append_links_inside_single_object=True, append_links_outside=True,
                                   serialize_with_relations=True):
        return self.multiple_entity_instance_serializer.serialize(entity_instances,
                                                                  append_links_inside_single_object,
                                                                  append_links_outside,
                                                                  serialize_with_relations)

@egg
class EntityInstanceSerializerFactory:
    def __init__(self, single_entity_instance_serializer_factory: SingleEntityInstanceSerializerFactory,
                 multiple_entity_instance_serializer_factory: MultipleEntityInstanceSerializerFactory):
        self.single_entity_instance_serializer_factory = single_entity_instance_serializer_factory
        self.multiple_entity_instance_serializer_factory = multiple_entity_instance_serializer_factory

    def create(self, request_context):
        return EntityInstanceSerializer(self.single_entity_instance_serializer_factory.create(request_context),
                                        self.multiple_entity_instance_serializer_factory.create(request_context),
                                        request_context)