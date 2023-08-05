from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import EntityInstance, DomainFactory
from jsonapidb.serialization import utils
from jsonapidb.serialization.utils import handle_invalid_format, invalid_format


class RelationInstancesDeserializer:
    def __init__(self, relations_data: dict, entity_instance: EntityInstance):
        self.relations_data = relations_data
        self.entity_instance = entity_instance

    @handle_invalid_format
    def deserialize(self):
        result = []
        for relation_name, relation_json in self.relations_data.items():
            if not self._relation_has_proper_type(relation_json):
                raise invalid_format()
            elif self._is_has_one_relation(relation_json):
                result.append(self._deserialize_has_one_relation(relation_json, relation_name))
            elif self._is_has_many_relation(relation_json):
                result.append(self._deserialize_has_many_relation(relation_json, relation_name))
            else:
                raise invalid_format()
        return result

    def _relation_has_proper_type(self, relation_json):
        return isinstance(relation_json, dict)

    def _is_has_one_relation(self, relation_json):
        return isinstance(relation_json['data'], dict)

    def _is_has_many_relation(self, relation_json):
        return isinstance(relation_json['data'], list)

    def _deserialize_has_one_relation(self, relation_json, relation_name):
        relation = self.entity_instance.meta.get_relation(relation_name)
        return relation.create_instance(self.entity_instance, relation_json['data']['id'])

    def _deserialize_has_many_relation(self, relation_json, relation_name):
        pks = [r['id'] for r in relation_json['data']]
        relation = self.entity_instance.meta.get_relation(relation_name)
        return relation.create_instance(self.entity_instance, pks)


@egg
class RelationInstancesDeserializerFactory:
    @staticmethod
    def create(relations_data, entity_instance):
        return RelationInstancesDeserializer(relations_data, entity_instance)


class SingleRelationInstanceDeserializer:
    def __init__(self, entity_name, pk, relation_name, relation_raw_data,
                 relation_instances_deserializer_factory: RelationInstancesDeserializerFactory,
                 domain_factory: DomainFactory):
        self.entity_name = entity_name
        self.pk = pk
        self.relation_name = relation_name
        self.relation_data = utils.to_json(relation_raw_data)
        self.relation_instances_deserializer_factory = relation_instances_deserializer_factory
        self.domain = domain_factory.create()

    def deserialize(self):
        entity = self.domain.get_entity(self.entity_name)
        entity_instance = entity.create_instance({}, self.pk)
        relation_instances = self.relation_instances_deserializer_factory\
            .create({self.relation_name: self.relation_data}, entity_instance)\
            .deserialize()
        entity_instance.relation_instances = relation_instances
        return entity_instance


@egg
class SingleRelationInstanceDeserializerFactory:
    def __init__(self, relation_instances_deserializer_factory: RelationInstancesDeserializerFactory,
                 domain_factory: DomainFactory):
        self.relation_instances_deserializer_factory = relation_instances_deserializer_factory
        self.domain_factory = domain_factory

    def create(self, entity_name, pk, relation_name, relation_raw_data: str):
        return SingleRelationInstanceDeserializer(entity_name, pk, relation_name, relation_raw_data,
                                                  self.relation_instances_deserializer_factory, self.domain_factory)