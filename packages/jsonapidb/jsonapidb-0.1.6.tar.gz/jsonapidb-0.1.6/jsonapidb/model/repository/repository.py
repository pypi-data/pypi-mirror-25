import bson
from typing import List
from mongoengine import connect

from jsonapidb.builders.app_builder import AppConfig
from jsonapidb.builders.scrambler import egg
from jsonapidb.conversion.converters import DocumentToEntityInstanceConverterFactory, \
    DocumentsToEntityInstancesConverterFactory
from jsonapidb.dto.output import GetSingleObjectOutputDTO, FindAllObjectsOutputDTO
from jsonapidb.model.domain import EntityInstance
from jsonapidb.model.repository.engine_registry import EngineRegistryFactory
from jsonapidb.model.repository.relations_repository import RelationManagerRepository


@egg
class Repository:
    def __init__(self, engine_registry_factory: EngineRegistryFactory, relation_manager: RelationManagerRepository,
                 config: AppConfig,
                 document_to_entity_instance_converter_factory: DocumentToEntityInstanceConverterFactory,
                 documents_to_entity_instances_converter_factory: DocumentsToEntityInstancesConverterFactory):
        self.registry = engine_registry_factory.create()
        self.relation_manager_repository = relation_manager
        self.document_to_entity_instance_converter_factory = document_to_entity_instance_converter_factory
        self.documents_to_entity_instances_converter_factory = documents_to_entity_instances_converter_factory
        connect(config.db_name)

    def create(self, entity_instance: EntityInstance):
        document = self.registry[entity_instance.meta.name].objects.create(**entity_instance.attributes)
        document.save()
        entity_instance.pk = str(document.pk)
        self.relation_manager_repository.update_related(entity_instance)
        document.reload()
        return entity_instance

    def update(self, entity_instance: EntityInstance):
        update_instructions = {'set__' + attr_name: attr_value for attr_name, attr_value in
                               entity_instance.attributes.items()}
        if update_instructions:
            self.registry[entity_instance.meta.name]. \
                objects(id=bson.ObjectId(entity_instance.pk)).update_one(**update_instructions)
        self.relation_manager_repository.update_related(entity_instance)

    def exists(self, entity_name, pk: str):
        try:
            searched_id = bson.ObjectId(pk)
        except (bson.errors.InvalidId, TypeError):
            return False
        return self.registry[entity_name].objects.filter(id=searched_id).count() > 0

    def delete(self, entity_name, pk: str):
        self.registry[entity_name].objects.get(id=pk).delete()

    def find_one(self, entity_name, pk: str, included_relations_names: List[str] = None):
        if not included_relations_names:
            included_relations_names = []
        included_entity_instances = self._find_included_entity_instances(entity_name, pk, included_relations_names)

        document = self.registry[entity_name].objects.get(id=pk)
        return GetSingleObjectOutputDTO(
            self.document_to_entity_instance_converter_factory.create(document, entity_name).convert(),
            included_entity_instances
        )

    def find_all(self, entity_name, included_relations_names: List[str] = None):
        included_instances = set()
        if not included_relations_names:
            included_relations_names = []
        documents = self.registry[entity_name].objects()
        entity_instance_list = self.documents_to_entity_instances_converter_factory.create(entity_name,
                                                                                           documents).convert()

        for entity_instance in entity_instance_list:
            included_instances.update(
                self._find_included_entity_instances(entity_name, entity_instance.pk, included_relations_names))
        return FindAllObjectsOutputDTO(entity_instance_list, list(included_instances))

    def find_relation(self, entity_name, pk, relation_name):
        document = self.registry[entity_name].objects.get(id=pk)
        entity_instance = self.document_to_entity_instance_converter_factory.create(document, entity_name).convert()

        for relation_instance in entity_instance.relation_instances:
            if relation_instance.meta.direct_name == relation_name:
                return relation_instance
        return None

    def update_relation(self, entity_instance: EntityInstance):
        self.relation_manager_repository.update_related(entity_instance)

    def _find_included_entity_instances(self, entity_name, pk, included_relations: List[str]):
        included_instances = set()
        for relation_name in included_relations:
            relation_instance = self.find_relation(entity_name, pk, relation_name)

            if relation_instance.meta.is_directly_has_one():
                get_single_object_dto = self.find_one(relation_instance.meta.target_entity.name,
                                                      relation_instance.related_pk)
                included_instances.add(get_single_object_dto.entity_instance)
            else:
                for related_pk in relation_instance.related_pks:
                    get_single_object_dto = self.find_one(relation_instance.meta.target_entity.name, related_pk)
                    included_instances.add(get_single_object_dto.entity_instance)
        return list(included_instances)
