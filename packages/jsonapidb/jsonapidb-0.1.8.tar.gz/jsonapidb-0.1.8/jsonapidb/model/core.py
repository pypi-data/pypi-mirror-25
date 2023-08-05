from typing import List

from jsonapidb.builders.scrambler import egg
from jsonapidb.model import domain
from jsonapidb.model.validators.validator import ModelValidator
from .repository.repository import Repository


@egg
class Model:
    def __init__(self, repository: Repository, validator: ModelValidator,
                 new_domain_factory: domain.DomainFactory):
        self.repository = repository
        self.validator = validator
        self.new_domain = new_domain_factory.create()

    def create(self, entity_instance: domain.EntityInstance):
        self.validator.validate_create(entity_instance)
        return self.repository.create(entity_instance)

    def delete(self, entity_name, pk):
        self.validator.validate_delete(entity_name, pk)
        self.repository.delete(entity_name, pk)

    def find_all(self, entity_name, included_relations: List[str]=None):
        self.validator.validate_find_all(entity_name, included_relations)
        return self.repository.find_all(entity_name, included_relations)

    def find_one(self, entity_name, pk, included_relations: List[str]=None):
        self.validator.validate_find_one(entity_name, pk, included_relations)
        return self.repository.find_one(entity_name, pk, included_relations)

    def update(self, entity_instance: domain.EntityInstance):
        self.validator.validate_update(entity_instance)
        item = self.repository.update(entity_instance)
        return item

    def find_relation(self, entity_name, pk, relation_name):
        self.validator.validate_find_relation(entity_name, pk, relation_name)
        return self.repository.find_relation(entity_name, pk, relation_name)

    def update_relation(self, entity_instance: domain.EntityInstance):
        self.validator.validate_update_relation(entity_instance)
        return self.repository.update_relation(entity_instance)