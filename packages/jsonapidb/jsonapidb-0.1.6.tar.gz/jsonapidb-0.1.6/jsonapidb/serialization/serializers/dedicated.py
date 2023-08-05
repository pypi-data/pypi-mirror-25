import json
from typing import List

from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import EntityInstance
from jsonapidb.serialization.serializers.entity_instance_serializers import EntityInstanceSerializerFactory, \
    EntityInstanceSerializer


class GetSingleObjectSerializer:
    def __init__(self, entity_instance_serializer: EntityInstanceSerializer):
        self.entity_instance_serializer = entity_instance_serializer

    def serialize(self, entity_instance: EntityInstance, included_instances: List[EntityInstance]=None):
        result = self.entity_instance_serializer.serialize_single_to_dict(entity_instance)
        if included_instances:
            result['included'] = self._serialize_included(included_instances)
        return json.dumps(result)

    def _serialize_included(self, included_instances: List[EntityInstance]=None):
        included = self.entity_instance_serializer.serialize_multiple_to_dict(included_instances,
                                                                              append_links_inside_single_object=False,
                                                                              append_links_outside=False,
                                                                              serialize_with_relations=False)
        return self._serialized_result_without_data_keyword(included)

    @staticmethod
    def _serialized_result_without_data_keyword(result):
        return result['data']


@egg
class GetSingleObjectSerializerFactory:
    def __init__(self, entity_instance_serializer_factory: EntityInstanceSerializerFactory):
        self.entity_instance_serializer_factory = entity_instance_serializer_factory

    def create(self, request_context):
        return GetSingleObjectSerializer(self.entity_instance_serializer_factory.create(request_context))


class FindAllItemsSerializer(GetSingleObjectSerializer):
    def __init__(self, entity_instance_serializer: EntityInstanceSerializer):
        super().__init__(entity_instance_serializer)

    def serialize(self, entity_instance_list: List[EntityInstance],
                  included_instances: List[EntityInstance]=None):
        result = self.entity_instance_serializer.serialize_multiple_to_dict(entity_instance_list)
        if included_instances:
            result['included'] = self._serialize_included(included_instances)
        return json.dumps(result)


@egg
class FindAllItemsSerializerFactory:
    def __init__(self, entity_instance_serializer_factory: EntityInstanceSerializerFactory):
        self.entity_instance_serializer_factory = entity_instance_serializer_factory

    def create(self, request_context):
        return FindAllItemsSerializer(self.entity_instance_serializer_factory.create(request_context))