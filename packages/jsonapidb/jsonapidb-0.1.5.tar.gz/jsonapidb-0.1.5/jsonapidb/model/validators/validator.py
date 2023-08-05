from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import EntityInstance, DomainFactory
from jsonapidb.model.repository.repository import Repository
from jsonapidb.model.validators.attr_validation import AttributesValidator
from jsonapidb.model.validators.relations_validation import RelationsValidator


class EntityDoesNotExist(ValueError):
    pass


class ItemWithGivenPkDoesNotExist(ValueError):
    pass


class InvalidItemAttributes(ValueError):
    def __init__(self, message, errors):
        super(InvalidItemAttributes, self).__init__(message)
        self.errors = errors


class RelationDoesNotExist(ValueError):
    pass


@egg
class ModelValidator:
    def __init__(self, repository: Repository, attributes_validator: AttributesValidator,
                 new_relations_validator: RelationsValidator, domain_factory: DomainFactory):
        self.repository = repository
        self.attributes_validator = attributes_validator
        self.relations_validator = new_relations_validator
        self.domain = domain_factory.create()

    def validate_create(self, entity_instance: EntityInstance):
        self._attributes_valid_or_error(entity_instance.meta.name, entity_instance.attributes)
        self.relations_validator.validate_relation_instances(entity_instance.relation_instances)

    def validate_delete(self, entity_name, pk):
        self._entity_exists_or_error(entity_name)
        self._item_with_given_pk_exists_or_error(entity_name, pk)

    def validate_update(self, entity_instance: EntityInstance):
        self._item_with_given_pk_exists_or_error(entity_instance.meta.name, entity_instance.pk)
        self._present_attributes_valid_or_error(entity_instance.meta.name, entity_instance.attributes)
        self.relations_validator.validate_relation_instances(entity_instance.relation_instances)

    def validate_find_one(self, entity_name, pk, included_relations=None):
        self._entity_exists_or_error(entity_name)
        self._validate_included_relations(entity_name, included_relations)
        self._item_with_given_pk_exists_or_error(entity_name, pk)

    def validate_find_all(self, entity_name, included_relations=None):
        self._entity_exists_or_error(entity_name)
        self._validate_included_relations(entity_name, included_relations)

    def validate_find_relation(self, entity_name, pk, relation_name):
        self._entity_exists_or_error(entity_name)
        self._item_with_given_pk_exists_or_error(entity_name, pk)
        self._relation_exists_or_error(entity_name, relation_name)

    def validate_update_relation(self, entity_instance: EntityInstance):
        self._item_with_given_pk_exists_or_error(entity_instance.meta.name, entity_instance.pk)
        self.relations_validator.validate_relation_instances(entity_instance.relation_instances)

    def _validate_included_relations(self, entity_name, included_relations):
        if included_relations:
            for relation_name in included_relations:
                self._relation_exists_or_error(entity_name, relation_name)

    def _entity_exists_or_error(self, entity_name):
        if not self.domain.entity_exists(entity_name):
            raise self._entity_does_not_exist(entity_name)

    def _item_with_given_pk_exists_or_error(self, entity_name, pk: str):
        if not self.repository.exists(entity_name, pk):
            raise self._item_with_given_pk_does_not_exist(entity_name, pk)

    def _relation_exists_or_error(self, entity_name, relation_name):
        if not self.domain.get_entity(entity_name).relation_exists(relation_name):
            raise self._relation_does_not_exist(entity_name, relation_name)

    def _attributes_valid_or_error(self, entity_name, attributes):
        errors = self.attributes_validator.validate(entity_name, attributes)
        if errors:
            raise self._invalid_item_attributes(errors)

    def _present_attributes_valid_or_error(self, entity_name, attributes):
        errors = self.attributes_validator.validate_and_ignore_missing_attributes(entity_name, attributes)
        if errors:
            raise self._invalid_item_attributes(errors)

    @staticmethod
    def _entity_does_not_exist(entity_name):
        return EntityDoesNotExist(
            'Entity with name "{entity_name}" does not exist'.format(entity_name=entity_name))

    @staticmethod
    def _item_with_given_pk_does_not_exist(entity_name, pk: str):
        return ItemWithGivenPkDoesNotExist(
            '{entity_name} with pk="{pk}" does not exist'.format(entity_name=entity_name,
                                                                 pk=pk))

    @staticmethod
    def _invalid_item_attributes(errors):
        return InvalidItemAttributes('Provided attributes are invalid', errors)


    @staticmethod
    def _relation_does_not_exist(entity_name, relation_name):
        return RelationDoesNotExist('Relation %s does not exist for entity %s' % (relation_name, entity_name))