import json
from typing import Tuple, List

from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import RelationInstance


class SingleRelationInstanceSerializer:
    def __init__(self, relation_instance: RelationInstance,
                 request_context):
        self.relation_instance = relation_instance
        self.request_context = request_context

    def serialize_to_final_form(self):
        _, serialized_relation_instance = self.serialize()
        return json.dumps(serialized_relation_instance)

    def serialize(self) -> Tuple[str, dict]:
        if self.relation_instance.meta.is_directly_has_one():
            return self.relation_instance.meta.direct_name, self._serialize_has_one_relation_instance()
        else:
            return self.relation_instance.meta.direct_name, self._serialize_has_many_relation_instance()

    def _serialize_has_one_relation_instance(self) -> dict:
        if self.relation_instance.related_pk:
            result = self._relation_instance_representation(
                self._relation_instance_data_element_representation(self.relation_instance.related_pk,
                                                                    self.relation_instance.meta.target_entity.name))
        else:
            result = None
        return result

    def _serialize_has_many_relation_instance(self) -> dict:
        if self.relation_instance.related_pks:
            result = self._relation_instance_representation(self._relation_instance_data_items_representation())
        else:
            result = {'data': [], 'links': self._generate_links()}

        return result

    def _relation_instance_data_items_representation(self) -> list:
        return [self._relation_instance_data_element_representation(pk, self.relation_instance.meta.target_entity.name) for pk in
                self.relation_instance.related_pks]

    @staticmethod
    def _relation_instance_data_element_representation(pk, entity_name):
        return {'id': pk, 'type': entity_name}

    def _relation_instance_representation(self, data):
        return {
            'links': self._generate_links(),
            'data': data
        }

    def _generate_links(self):
        return {
            'self': '{root}/{resource}/{pk}/relationships/{relation_name}'.format(
                root=self.request_context.origin,
                resource=self.request_context.resource_name,
                pk=self.relation_instance.entity_instance.pk,
                relation_name=self.relation_instance.meta.direct_name
            ),
            'related': '{root}/{resource}/{pk}/{relation_name}'.format(
                root=self.request_context.origin,
                resource=self.request_context.resource_name,
                pk=self.relation_instance.entity_instance.pk,
                relation_name=self.relation_instance.meta.direct_name
            ),
        }


@egg
class SingleRelationInstanceSerializerFactory:
    @staticmethod
    def create(relation, request_context):
        return SingleRelationInstanceSerializer(relation, request_context)


class RelationInstancesSerializer:
    def __init__(self, relation_instances: List[RelationInstance],
                 single_relation_instance_serializer_factory: SingleRelationInstanceSerializerFactory,
                 request_context):
        self.relation_instances = relation_instances
        self.current_relation_instance = None
        self.single_relation_instance_serializer_factory = single_relation_instance_serializer_factory
        self.request_context = request_context

    def serialize(self) -> dict:
        result = {}
        for relation_instance in self.relation_instances:
            single_relation_instance_serializer = self.single_relation_instance_serializer_factory\
                .create(relation_instance, self.request_context)
            relation_name, serialized_relation_instance = single_relation_instance_serializer.serialize()
            result[relation_name] = serialized_relation_instance
        return result


@egg
class RelationInstancesSerializerFactory:
    def __init__(self, single_relation_instance_serializer_factory: SingleRelationInstanceSerializerFactory):
        self.single_relation_instance_serializer_factory = single_relation_instance_serializer_factory

    def create(self, relation_instances: List[RelationInstance], request_context):
        return RelationInstancesSerializer(relation_instances,
                                           self.single_relation_instance_serializer_factory,
                                           request_context)