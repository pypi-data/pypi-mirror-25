from jsonapidb.builders.scrambler import egg
from jsonapidb.model.repository.repository import Repository


class InvalidRelationType(ValueError):
    pass


class InvalidRelatedType(ValueError):
    pass


class RelatedItemWithGivenPkDoesNotExist(ValueError):
    pass


@egg
class RelationsValidator:
    def __init__(self, repository: Repository):
        self.repository = repository

    def validate_relation_instances(self, relation_instances):
        for relation_instance in filter(lambda r: not r.is_empty(), relation_instances):
            self._validate_related_data(relation_instance)

    def _validate_related_data(self, relation_instance):
        related_entity_name = relation_instance.meta.target_entity.name
        if relation_instance.meta.is_directly_has_one():
            self._related_item_with_given_pk_exists_or_error(related_entity_name, relation_instance.related_pk)
        else:
            for related_pk in relation_instance.related_pks:
                self._related_item_with_given_pk_exists_or_error(related_entity_name, related_pk)

    def _related_item_with_given_pk_exists_or_error(self, related_entity_name, related_pk):
        if not self.repository.exists(related_entity_name, related_pk):
            raise self._related_item_with_given_pk_does_not_exist(related_entity_name, related_pk)

    @staticmethod
    def _related_item_with_given_pk_does_not_exist(related_entity_name, related_pk):
        return RelatedItemWithGivenPkDoesNotExist('Related entity "{related_entity_name}" with pk="{related_pk}" does not exist'
                                                    .format(related_entity_name=related_entity_name,
                                                            related_pk=related_pk))