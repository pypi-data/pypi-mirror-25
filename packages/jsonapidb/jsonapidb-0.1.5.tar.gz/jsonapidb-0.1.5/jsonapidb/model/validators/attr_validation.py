import abc
import re
import six
from typing import List

from jsonapidb.builders import json_proxy
from jsonapidb.builders.scrambler import egg
from jsonapidb.model.repository.repository import Repository


class AbstractValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def validate(self, raw_value, entity_name, repository) -> List[str]:
        pass


class AttributeRequirements:
    def __init__(self, name, type_validator: AbstractValidator, required: bool,
                 validators: List[AbstractValidator]):
        self.type_validator = type_validator
        self.name = name
        self.required = required
        self.validators = validators


class EntityAttributesRequirements:
    def __init__(self, name, attribute_requirements: List[AttributeRequirements]):
        self.name = name
        self.attribute_requirements = {attribute.name: attribute for attribute in attribute_requirements}

    def attribute_expected(self, attribute):
        return attribute in self.attribute_requirements


class Requirements:
    def __init__(self, entity_attribute_requirements: List[EntityAttributesRequirements]):
        self.entity_attribute_requirements = {entity.name: entity for entity in entity_attribute_requirements}

    def attribute_expected(self, entity_name, attribute_name):
        return self.entity_attribute_requirements[entity_name].attribute_expected(attribute_name)

    def get_attribute_validators(self, entity_name, attribute_name):
        return self._get_attribute_requirements(entity_name, attribute_name).validators

    def get_attribute_type_validator(self, entity_name, attribute_name):
        return self._get_attribute_requirements(entity_name, attribute_name).type_validator

    def get_all_required_attributes(self, entity_name):
        return [attr_name for attr_name, attr_req in self._get_entity_requirements(entity_name).attribute_requirements.items() if attr_req.required]

    def _get_entity_requirements(self, entity_name):
        return self.entity_attribute_requirements[entity_name]

    def _get_attribute_requirements(self, entity_name, attribute_name):
        return self._get_entity_requirements(entity_name).attribute_requirements[attribute_name]


class IsStringValidator(AbstractValidator):
    def validate(self, raw_value, entity_name=None, repository=None):
        if not isinstance(raw_value, six.string_types):
            error_msg = 'Expected string'
            return [error_msg]

        return []


class LenValidator(AbstractValidator):
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, raw_value, entity_name=None, repository=None):
        if self.min_length and len(raw_value) < self.min_length:
            error_msg = 'Value {0} requires at least {1} characters'.format(raw_value, self.min_length)
            return [error_msg]

        if self.max_length and len(raw_value) > self.max_length:
            error_msg = 'Value {0} requires at most {1} characters'.format(raw_value, self.max_length)
            return [error_msg]

        return []

@egg
class RequirementsFactory:
    VALIDATOR_CLASS_MAPPING = {
        'lenValidator': LenValidator
    }

    TYPE_VALIDATOR_CLASS_MAPPING = {
        'string': IsStringValidator
    }

    def __init__(self, schema: json_proxy.SchemaProxy, repository: Repository):
        self.schema = schema
        self.repository = repository

    def create(self):
        entity_attribute_requirements = self._generate_entity_attribute_requirements()
        return Requirements(entity_attribute_requirements)

    def _generate_entity_attribute_requirements(self):
        entity_attribute_requirements = []
        for entity_proxy in self.schema.entities:
            attr_requirements = self._generate_attribute_requirements(entity_proxy)
            entity_attr_requirement = EntityAttributesRequirements(entity_proxy.name, attr_requirements)
            entity_attribute_requirements.append(entity_attr_requirement)
        return entity_attribute_requirements

    def _generate_attribute_requirements(self, entity_proxy: json_proxy.EntityProxy):
        attribute_requirements = []
        for attr_proxy in entity_proxy.attributes:
            type_validator = self._generate_type_validator(attr_proxy)
            is_attr_required = self._check_attr_is_required(attr_proxy)
            attr_validators = self._generate_single_attribute_validators(attr_proxy)
            attr_requirements = AttributeRequirements(attr_proxy.name, type_validator, is_attr_required,
                                                             attr_validators)
            attribute_requirements.append(attr_requirements)
        return attribute_requirements

    def _generate_single_attribute_validators(self, attr_proxy: json_proxy.AttributeProxy):
        validators = []
        for validator_proxy in attr_proxy.validators:
            kwargs = dict((self._camel_case_to_underscore(k), v) for k, v in validator_proxy.kwargs.items())
            validators.append(self.VALIDATOR_CLASS_MAPPING[validator_proxy.name](**kwargs))
        return validators

    @classmethod
    def _generate_type_validator(cls, attr_proxy: json_proxy.AttributeProxy):
        return cls.TYPE_VALIDATOR_CLASS_MAPPING[attr_proxy.type]()

    @staticmethod
    def _check_attr_is_required(attr_proxy: json_proxy.AttributeProxy):
        return attr_proxy.required

    @staticmethod
    def _camel_case_to_underscore(string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@egg
class AttributesValidator:
    def __init__(self, repository: Repository, requirements_factory: RequirementsFactory):
        self.requirements = requirements_factory.create()
        self.repository = repository

    def validate(self, entity_name, attributes: dict) -> dict:
        # TODO add handling unexpected attributes(now they are ignored)
        missing_attributes = self._find_missing_attributes(entity_name, attributes)
        missing_attributes_errors = {missing_attribute: ['Required, but not found'] for missing_attribute in missing_attributes}

        errors = self.validate_and_ignore_missing_attributes(entity_name, attributes)
        errors.update(missing_attributes_errors)

        return errors

    def validate_and_ignore_missing_attributes(self, entity_name, attributes: dict):
        errors = {}

        for attribute_name, attribute_value in attributes.items():
            if not self._attribute_expected(entity_name, attribute_name):
                continue

            attribute_errors = self._validate_attribute(entity_name, attribute_name, attribute_value)
            if attribute_errors:
                errors[attribute_name] = attribute_errors

        return errors

    def _find_missing_attributes(self, entity_name, provided_attributes) -> List[str]:
        required_attributes = self.requirements.get_all_required_attributes(entity_name)
        return list(filter(lambda req_attr: req_attr not in provided_attributes, required_attributes))

    def _validate_attribute(self, entity_name, attribute_name, attribute_value) -> List[str]:
        type_validator = self.requirements.get_attribute_type_validator(entity_name, attribute_name)
        type_error = type_validator.validate(attribute_value, entity_name, self.repository)

        if type_error:
            return type_error

        errors = []
        for attribute_validator in self.requirements.get_attribute_validators(entity_name, attribute_name):
            validation_errors = attribute_validator.validate(attribute_value, entity_name, self.repository)
            errors.extend(validation_errors)

        return errors

    def _attribute_expected(self, entity_name, attribute_name):
        return self.requirements.attribute_expected(entity_name, attribute_name)