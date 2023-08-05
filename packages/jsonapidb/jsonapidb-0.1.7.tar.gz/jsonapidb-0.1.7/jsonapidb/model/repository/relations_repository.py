from bson import ObjectId

from jsonapidb.builders.scrambler import egg
from jsonapidb.model import domain
from jsonapidb.model.domain import Empty
from jsonapidb.model.repository.engine_registry import EngineRegistryFactory


@egg
class RelationManagerRepository:
    def __init__(self, engine_registry_factory: EngineRegistryFactory):
        self.registry = engine_registry_factory.create()

    def update_related(self, entity_instance: domain.EntityInstance):
        for relation_instance in entity_instance.relation_instances:
            if isinstance(relation_instance, domain.OneToManyRelationInstance) and\
                    not isinstance(relation_instance.related_pk, Empty):
                self._update_one_to_many(relation_instance)
            elif isinstance(relation_instance, domain.ManyToOneRelationInstance) and\
                    not isinstance(relation_instance.related_pks, Empty):
                self._update_many_to_one(relation_instance)
            elif isinstance(relation_instance, domain.ManyToManyRelationInstance) and\
                    not isinstance(relation_instance.related_pks, Empty):
                self._update_many_to_many(relation_instance)
            elif isinstance(relation_instance, domain.OneToOneRelationInstance) and\
                    not isinstance(relation_instance.related_pk, Empty):
                self._update_one_to_one(relation_instance)

    def _update_one_to_one(self, one_to_one: domain.OneToOneRelationInstance):
        self._update_one_to_many(one_to_one)

    def _update_one_to_many(self, one_to_many: domain.OneToManyRelationInstance):
        document = self.registry[one_to_many.meta.source_entity.name]\
            .objects.get(id=one_to_many.entity_instance.pk)

        related_document = self.registry[one_to_many.meta.target_entity.name]\
            .objects.get(id=one_to_many.related_pk)

        setattr(document, one_to_many.meta.direct_name, related_document)
        document.save()

        refreshed_has_many = list(self.registry[one_to_many.meta.source_entity.name].objects.filter(
            **{one_to_many.meta.direct_name: one_to_many.related_pk}
        ))
        setattr(related_document, one_to_many.meta.backward_name, refreshed_has_many)
        related_document.save()

    def _update_many_to_one(self, many_to_one: domain.ManyToOneRelationInstance):
        documents = self.registry[many_to_one.meta.target_entity.name]\
            .objects.filter(**{many_to_one.meta.backward_name: many_to_one.entity_instance.pk})

        for doc in documents:
            setattr(doc, many_to_one.meta.backward_name, None)
            doc.save()

        related_documents = []
        for pk in many_to_one.related_pks:
            document = self.registry[many_to_one.meta.target_entity.name]\
                .objects.get(id=pk)
            setattr(document, many_to_one.meta.backward_name,
                    ObjectId(many_to_one.entity_instance.pk))
            document.save()
            related_documents.append(document)

            has_many_host_to_refresh = self.registry[many_to_one.meta.source_entity.name].objects.get(**{many_to_one.meta.direct_name: pk})
            getattr(has_many_host_to_refresh, many_to_one.meta.direct_name).remove(document)
            has_many_host_to_refresh.save()

        source_document = self.registry[many_to_one.meta.source_entity.name]\
            .objects.get(id=many_to_one.entity_instance.pk)
        setattr(source_document, many_to_one.meta.direct_name, related_documents)
        source_document.save()

    def _update_many_to_many(self, many_to_many: domain.ManyToManyRelationInstance):
        doc = self.registry[many_to_many.meta.source_entity.name]\
            .objects.get(id=many_to_many.entity_instance.pk)
        for related_doc in self.registry[many_to_many.meta.target_entity.name]\
                .objects.filter(**{many_to_many.meta.backward_name: doc}):
            getattr(related_doc, many_to_many.meta.backward_name).remove(doc)
            related_doc.save()

        doc[many_to_many.meta.direct_name] = []
        doc.save()

        for related_doc_pk in many_to_many.related_pks:
            related_doc = self.registry[many_to_many.meta.target_entity.name]\
                .objects.get(id=related_doc_pk)
            doc.update(**{'push__' + many_to_many.meta.direct_name: related_doc})
            related_doc.update(**{'push__' + many_to_many.meta.backward_name: doc})
            doc.save()
            related_doc.save()