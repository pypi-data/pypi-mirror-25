from collections import UserList

from jsonapidb.builders.scrambler import egg


class RelationProxy:
    HAS_ONE = 'hasOne'
    HAS_MANY = 'hasMany'

    def __init__(self, relation_schema):
        self.source = relation_schema['source']
        self.target = relation_schema['target']
        self.direct_type = relation_schema['directType']
        self.backward_type = relation_schema['backwardType']
        self.direct_name = relation_schema['directName']
        self.backward_name = relation_schema['backwardName']


# TODO change RelationsProxy to UserList child
class RelationsProxy:
    def __init__(self, relations_schema):
        self.relations_schema = relations_schema

    @property
    def relations(self):
        return map(RelationProxy, self.relations_schema)


class EntityProxy:
    def __init__(self, entity_name, entity_schema):
        self.name = entity_name
        self.entity_schema = entity_schema

    @property
    def attributes(self):
        return AttributesProxy(self.entity_schema['attributes'])


# TODO change EntitiesProxy to UserList child
class EntitiesProxy:
    def __init__(self, entities_schema):
        self.entities_schema = entities_schema

    @property
    def entities(self):
        ENTITY_NAME = 0
        ENTITY_SCHEMA = 1
        return map(
            lambda entity_name_and_schema: EntityProxy(entity_name_and_schema[ENTITY_NAME],
                                                       entity_name_and_schema[ENTITY_SCHEMA]),
            self.entities_schema.items()
        )


class AttributesProxy(UserList):
    def __init__(self, attributes_schema):
        super().__init__(AttributeProxy(attribute_name, attribute_schema['type'], attribute_schema['required'],
                                        attribute_schema['validators'])
                         for attribute_name, attribute_schema in attributes_schema.items())


class AttributeProxy:
    def __init__(self, attribute_name, attribute_type, required, validators_schema):
        self.name = attribute_name
        self.type = attribute_type
        self.required = required
        self.validators_schema = validators_schema

    @property
    def validators(self):
        return ValidatorsProxy(self.validators_schema)


class ValidatorProxy:
    def __init__(self, validator_name, validator_kwargs):
        self.name = validator_name
        self.kwargs = validator_kwargs


class ValidatorsProxy(UserList):
    def __init__(self,  validators_schema):
        super().__init__(ValidatorProxy(name, kwargs) for name, kwargs in validators_schema.items())


@egg
class SchemaProxy:
    def __init__(self, schema):
        self.schema = schema
        self.entities_proxy = EntitiesProxy(schema['entities'])
        self.relations_proxy = RelationsProxy(schema['relations'])

    @property
    def entities(self):
        return self.entities_proxy.entities

    @property
    def relations(self):
        return self.relations_proxy.relations

    @property
    def entity_names(self):
        return [entity.name for entity in self.entities]