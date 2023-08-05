from typing import List, Set

from . import json_proxy


class InvalidSchema(Exception):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super().__init__(*args, **kwargs)


class InvalidAttributeValidators(InvalidSchema):
    pass


class InvalidAttributeValidator(InvalidSchema):
    pass


class InvalidAttributeType(InvalidSchema):
    pass


class AttributeTypeMissing(InvalidSchema):
    pass


class AttributeValidatorsMissing(InvalidSchema):
    pass


class InvalidAttributes(InvalidSchema):
    pass


class InvalidEntity(InvalidSchema):
    pass


class EntityAttributesMissing(InvalidSchema):
    pass


class InvalidEntities(InvalidSchema):
    pass


class RelationsExpectedToBeList(InvalidSchema):
    pass


class TargetEntityNotFoundInEntities(InvalidSchema):
    pass


class SourceEntityNotFoundInEntities(InvalidSchema):
    pass


class RequiredAttributeNotFoundInRelation(InvalidSchema):
    pass


class RelationAttributeValueExpectedToBeString(InvalidSchema):
    pass


class InvalidDirectType(InvalidSchema):
    pass


class InvalidBackwardType(InvalidSchema):
    pass


class FoundRepetitiveSourceAndDirectNamePair(InvalidSchema):
    pass


class FoundRepetitiveTargetAndBackwardNamePair(InvalidSchema):
    pass


class EntitiesNotFoundInSchema(InvalidSchema):
    pass


class RelationsNotFoundInSchema(InvalidSchema):
    pass


class EntityExpectedToBeDict(InvalidSchema):
    pass


class AttributesExpectedToBeDict(InvalidSchema):
    pass


class SchemaValidator:
    AVAILABLE_RELATION_TYPES = {'hasOne', 'hasMany'}
    EXPECTED_ATTRIBUTES_IN_RELATION = {
        'source',
        'target',
        'directType',
        'backwardType',
        'directName',
        'backwardName',
    }

    def __init__(self, schema):
        self.schema = schema
        self.schema_proxy = json_proxy.SchemaProxy(schema)

    def validate(self):
        path = []
        self.validate_if_schema_has_entities(self.schema, ['entities'])
        self.validate_if_schema_has_relations(self.schema, ['relations'])
        self.validate_entities(self.schema['entities'], self.get_extended_path(path, 'entities'))
        entity_names = self.get_schema_entity_names_set()
        self.validate_relations(self.schema['relations'], entity_names, self.get_extended_path(path, 'relations'))

    def get_schema_entity_names_set(self):
        return set(self.schema_proxy.entity_names)

    @classmethod
    def validate_if_schema_has_entities(cls, schema, path):
        if 'entities' not in schema:
            raise EntitiesNotFoundInSchema(path)

    @classmethod
    def validate_if_schema_has_relations(cls, schema, path):
        if 'relations' not in schema:
            raise RelationsNotFoundInSchema(path)

    @classmethod
    def validate_relations(cls, relations, entity_names: Set[str], path):
        cls.validate_if_relations_object_is_list(relations, path)
        for i, relation in enumerate(relations):
            cls.validate_relation(relation, entity_names, cls.get_extended_path(path, str(i)))

        cls.validate_if_all_direct_name_and_source_pairs_are_unique(relations, path)
        cls.validate_if_all_backward_name_and_target_pairs_are_unique(relations, path)

    @classmethod
    def validate_relation(cls, relation, entity_names, path):
        cls.validate_if_relation_has_all_required_keys(relation, path)
        cls.validate_if_relation_values_are_all_strings(relation, path)
        cls.validate_direct_type(relation, path)
        cls.validate_backward_type(relation, path)
        cls.validate_if_relation_source_entity_exists(relation, entity_names, cls.get_extended_path(path, 'source'))
        cls.validate_if_relation_target_entity_exists(relation, entity_names, cls.get_extended_path(path, 'target'))

    @classmethod
    def validate_if_relation_has_all_required_keys(cls, relation, path):
        for expected_attribute in cls.EXPECTED_ATTRIBUTES_IN_RELATION:
            if expected_attribute not in relation:
                raise RequiredAttributeNotFoundInRelation(cls.get_extended_path(path, expected_attribute))

    @classmethod
    def validate_if_relation_values_are_all_strings(cls, relation: dict, path):
        for attribute_name, relation_attribute_value in relation.items():
            if not cls.is_string(relation_attribute_value):
                raise RelationAttributeValueExpectedToBeString(cls.get_extended_path(path, attribute_name))

    @classmethod
    def validate_if_relation_source_entity_exists(cls, relation, entity_names, path):
        if relation['source'] not in entity_names:
            raise SourceEntityNotFoundInEntities(path)

    @classmethod
    def validate_if_relation_target_entity_exists(cls, relation, entity_names, path):
        if relation['target'] not in entity_names:
            raise TargetEntityNotFoundInEntities(path)

    @classmethod
    def validate_direct_type(cls, relation, path):
        if relation['directType'] not in cls.AVAILABLE_RELATION_TYPES:
            raise InvalidDirectType(path)

    @classmethod
    def validate_backward_type(cls, relation, path):
        if relation['directType'] not in cls.AVAILABLE_RELATION_TYPES:
            raise InvalidBackwardType(path)

    @classmethod
    def get_direct_name_and_source_pairs(cls, relations):
        return cls.get_pairs_from_relations(relations, 'source', 'directName')

    @classmethod
    def get_backward_name_and_target_pairs(cls, relations):
        return cls.get_pairs_from_relations(relations, 'target', 'backwardName')

    @staticmethod
    def get_pairs_from_relations(relations, attribute_name1, attribute_name2):
        return tuple((relation[attribute_name1], relation[attribute_name2]) for relation in relations)

    @classmethod
    def validate_if_all_direct_name_and_source_pairs_are_unique(cls, relations, path):
        pairs = cls.get_direct_name_and_source_pairs(relations)

        if len(pairs) != len(set(pairs)):
            raise FoundRepetitiveSourceAndDirectNamePair(path)

    @classmethod
    def validate_if_all_backward_name_and_target_pairs_are_unique(cls, relations, path):
        pairs = cls.get_backward_name_and_target_pairs(relations)

        if len(pairs) != len(set(pairs)):
            raise FoundRepetitiveTargetAndBackwardNamePair(path)

    @classmethod
    def validate_if_relations_object_is_list(cls, relations, path):
        if not cls.is_list(relations):
            raise RelationsExpectedToBeList(path)

    @staticmethod
    def is_list(relations):
        return isinstance(relations, list)

    @classmethod
    def validate_entities(cls, entities, path):
        if not isinstance(entities, dict):
            raise InvalidEntities(path)

        for entity_name, entity in entities.items():
            cls.validate_entity(entity, cls.get_extended_path(path, entity_name))

    @classmethod
    def validate_entity(cls, entity, path):
        cls.validate_if_entity_is_dict(entity, path)
        path_with_attributes = cls.get_extended_path(path, 'attributes')
        cls.validate_if_entity_contains_attributes(entity, path)
        cls.validate_attributes(entity['attributes'], path_with_attributes)

    @classmethod
    def validate_if_entity_is_dict(cls, entity, path):
        if not isinstance(entity, dict):
            raise EntityExpectedToBeDict(path)

    @classmethod
    def validate_if_entity_contains_attributes(cls, entity, path):
        if 'attributes' not in entity:
            raise EntityAttributesMissing(path)

    @classmethod
    def validate_attributes(cls, attributes, path):
        cls.validate_if_attributes_obj_is_dict(attributes, path)

        for attribute_name, attribute in attributes.items():
            cls.validate_attribute(attribute, cls.get_extended_path(path, attribute_name))

    @classmethod
    def validate_if_attributes_obj_is_dict(cls, attributes, path):
        if not isinstance(attributes, dict):
            raise AttributesExpectedToBeDict(path)

    @classmethod
    def validate_attribute(cls, attribute, path):
        cls.validate_if_attribute_has_type_and_validators(attribute, path)
        cls.validate_attribute_type(attribute['type'], cls.get_extended_path(path, 'type'))
        cls.validate_attribute_validators(attribute['validators'], cls.get_extended_path(path, 'validators'))

    @classmethod
    def validate_if_attribute_has_type_and_validators(cls, attribute, path):
        cls.validate_if_attribute_has_type(attribute, cls.get_extended_path(path, 'type'))
        cls.validate_if_attribute_has_validators(attribute, cls.get_extended_path(path, 'validators'))

    @classmethod
    def validate_if_attribute_has_type(cls, attribute, path):
        if 'type' not in attribute:
            raise AttributeTypeMissing(path)

    @classmethod
    def validate_if_attribute_has_validators(cls, attribute, path):
        if 'validators' not in attribute:
            raise AttributeValidatorsMissing(path)

    @classmethod
    def validate_attribute_type(cls, attribute_type, path: List[str]):
        if not cls.is_string(attribute_type):
            raise InvalidAttributeType(path)

    @classmethod
    def validate_attribute_validators(cls, validators, path: List[str]):
        cls.validate_if_validators_are_dict(validators, path)
        for validator_name, validator in validators.items():
            cls.validate_attribute_validator(validator, cls.get_extended_path(path, validator_name))

    @classmethod
    def validate_if_validators_are_dict(cls, validators, path):
        if not cls.is_dict(validators):
            raise InvalidAttributeValidators(path)

    @classmethod
    def validate_attribute_validator(cls, validator, path):
        if not cls.is_dict(validator):
            raise InvalidAttributeValidator(path, 'Attribute validator expected to be dict')

    @staticmethod
    def is_dict(obj):
        return isinstance(obj, dict)

    @staticmethod
    def is_string(obj):
        return isinstance(obj, str)

    @staticmethod
    def get_extended_path(path, new_element):
        return path + [new_element]