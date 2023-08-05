import mongoengine
from collections import UserDict

from jsonapidb.builders.json_proxy import SchemaProxy, RelationProxy
from jsonapidb.builders.scrambler import egg


class EngineRegistryEntity:
    FIELD_CLASSES = {
        'string': mongoengine.StringField,
    }
    RELATION_FIELD_CLASSES = {
        'hasOne': mongoengine.ReferenceField,
        'hasMany': lambda source_or_target: mongoengine.ListField(mongoengine.ReferenceField(source_or_target)),
    }

    def __init__(self, entity):
        self.entity = entity
        self.entity_fields = self.map_entity_attributes_to_mongoengine_document_fields()

    def map_entity_attributes_to_mongoengine_document_fields(self):
        return {attr.name: self.FIELD_CLASSES[attr.type]() for attr in self.entity.attributes}

    def get_as_mongo_engine_document(self):
        return type(self.entity.name, (mongoengine.Document, ), self.entity_fields)

    def add_direct_relation(self, relation):
        self.entity_fields[relation.direct_name] = self.RELATION_FIELD_CLASSES[relation.direct_type](relation.target)

    def add_backward_relation(self, relation):
        self.entity_fields[relation.backward_name] = self.RELATION_FIELD_CLASSES[relation.backward_type](relation.source)

    @staticmethod
    def _is_relation_many_to_many(relation):
        return relation.direct_type == RelationProxy.HAS_MANY and relation.backward_type == RelationProxy.HAS_MANY


class EngineRegistry(UserDict):
    def get_as_dict_of_mongo_engine_documents(self):
        return {entity_name: engine_registry_entity.get_as_mongo_engine_document() for entity_name, engine_registry_entity in self.items()}

    def add_entity(self, entity):
        self[entity.name] = EngineRegistryEntity(entity)

    def add_relation(self, relation):
        self[relation.source].add_direct_relation(relation)
        self[relation.target].add_backward_relation(relation)


@egg
class EngineRegistryFactory:
    def __init__(self, schema: SchemaProxy):
        self._schema = schema
        self._engine_registry = EngineRegistry()
        self._add_entities_to_engine_registry()
        self._add_relations_to_engine_registry()
        self._engine_registry = self._engine_registry.get_as_dict_of_mongo_engine_documents()

    def create(self):
        return self._engine_registry

    def _set_fresh_engine_registry(self):
        self._engine_registry = EngineRegistry()

    def _add_entities_to_engine_registry(self):
        for entity in self._get_entities():
            self._add_entity_to_engine_registry(entity)

    def _get_entities(self):
        return self._schema.entities

    def _add_entity_to_engine_registry(self, entity):
        self._engine_registry.add_entity(entity)

    def _add_relations_to_engine_registry(self):
        for relation in self._get_relations():
            self._add_relation_to_engine_registry(relation)

    def _get_relations(self):
        return self._schema.relations

    def _add_relation_to_engine_registry(self, relation):
        self._engine_registry.add_relation(relation)