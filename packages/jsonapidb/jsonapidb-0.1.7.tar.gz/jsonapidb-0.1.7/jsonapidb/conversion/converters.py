from mongoengine import Document

from jsonapidb.builders.scrambler import egg
from jsonapidb.model import domain


class DocumentToEntityInstanceConverter:
    def __init__(self, document: Document, entity_name, domain_factory: domain.DomainFactory):
        self._document = document
        self._domain = domain_factory.create()
        self._entity_name = entity_name
        self._entity = self._domain.get_entity(entity_name)

    def convert(self):
        attributes = self._get_attributes_from_document()
        entity_instance = self._entity.create_instance(attributes, str(self._document.pk))
        entity_instance.relation_instances = self._get_relation_instances_from_document(entity_instance)
        return entity_instance

    def _get_attributes_from_document(self):
        return {attribute_name: self._document[attribute_name] for attribute_name in self._entity.attributes}

    def _get_relation_instances_from_document(self, entity_instance):
        relation_instances = []
        for relation in self._entity.relations:
            if relation.is_directly_has_one():
                relation_instances.append(relation.create_instance(entity_instance, str(self._document[relation.direct_name].pk)))
            else:
                relation_instances.append(relation.create_instance(entity_instance,
                                                                   [str(d.pk) for d in self._document[relation.direct_name]]))
        return relation_instances


@egg
class DocumentToEntityInstanceConverterFactory:
    def __init__(self, domain: domain.DomainFactory):
        self._domain = domain

    def create(self, document, entity_name):
        return DocumentToEntityInstanceConverter(document, entity_name, self._domain)


@egg
class DocumentsToEntityInstancesConverterFactory:
    def __init__(self, document_to_entity_instance_converter_factory: DocumentToEntityInstanceConverterFactory):
        self._document_to_entity_instance_converter_factory = document_to_entity_instance_converter_factory

    def create(self, entity_name, documents):
        return DocumentsToEntityInstancesConverter(entity_name, documents, self._document_to_entity_instance_converter_factory)


class DocumentsToEntityInstancesConverter:
    def __init__(self, entity_name, documents, document_to_entity_instance_converter_factory: DocumentToEntityInstanceConverterFactory):
        self._document_to_entity_instance_converter_factory = document_to_entity_instance_converter_factory
        self._documents = documents
        self._entity_name = entity_name

    def convert(self):
        return [self._document_to_entity_instance_converter_factory.create(doc, self._entity_name).convert() for doc in self._documents]