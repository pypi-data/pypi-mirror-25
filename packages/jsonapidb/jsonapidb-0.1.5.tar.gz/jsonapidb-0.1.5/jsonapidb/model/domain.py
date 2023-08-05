from typing import List, Dict

from jsonapidb.builders.json_proxy import SchemaProxy
from jsonapidb.builders.scrambler import egg


class Empty:
    def __iter__(self):
        yield

    def __len__(self):
        return 0


def metainfo(obj):
    return obj


def instance(obj):
    return obj


class EntityNotFound(ValueError):
    pass


class RelationNotFound(ValueError):
    pass


class InvalidRelationType(ValueError):
    pass


@metainfo
class MetaEntity:
    def __init__(self, name,
                 attributes: List[str]):
        self.name = name
        self.attributes = attributes
        self.relations = []

        self._relations_dict = {}

    def create_instance(self, attributes: Dict[str, object], pk=None):
        return EntityInstance(self, attributes, pk)

    def add_relation(self, relation):
        self.relations.append(relation)
        self._add_relation_to_search_optimized_relations(relation)

    def relation_exists(self, relation_name):
        return relation_name in self._relations_dict

    def get_relation(self, relation_name):
        try:
            return self._relations_dict[relation_name]
        except KeyError:
            raise RelationNotFound('{entity_name}/{relation_name} relation not found'.format(entity_name=self.name,
                                                                                             relation_name=relation_name))

    def get_direct_relations(self):
        return [relation for relation in self.relations if relation.source_entity == self]

    def get_backward_relations(self):
        return [relation for relation in self.relations if relation.target_entity == self]

    def _add_relation_to_search_optimized_relations(self, relation):
        if relation.source_entity == self:
            self._relations_dict[relation.direct_name] = relation
        elif relation.target_entity == self:
            self._relations_dict[relation.backward_name] = relation

    def __eq__(self, other):
        return self.name == other.name and \
               self.relations == other.relations and \
               self.attributes == other.attributes

    def __hash__(self):
        return hash((self.name, tuple(self.attributes), tuple(self.relations)))


@metainfo
class MetaRelation:
    HAS_ONE = 'hasOne'
    HAS_MANY = 'hasMany'

    def __init__(self, source_entity: MetaEntity,
                 target_entity: MetaEntity, direct_name, backward_name, direct_type):
        self.source_entity = source_entity
        self.target_entity = target_entity
        self.direct_name = direct_name
        self.backward_name = backward_name
        self.direct_type = direct_type

    def create_empty(self, entity_instance):
        return self.create_instance(entity_instance, Empty())

    def is_directly_has_one(self):
        return self.direct_type == self.HAS_ONE

    def is_directly_has_many(self):
        return not self.is_directly_has_one()

    def __eq__(self, other):
        return self.name == other.name and \
               self.source_entity.name == other.source_entity.name and \
               self.target_entity.name == other.target_entity.name and \
               self.direct_name == other.direct_name and \
               self.backward_name == other.backward_name

    def __hash__(self):
        return hash((self.source_entity.name, self.target_entity.name, self.direct_name,
                     self.backward_name))


@metainfo
class MetaOneToXRelation(MetaRelation):
    def __init__(self, source_entity: MetaEntity,
                 target_entity: MetaEntity, direct_name, backward_name):
        super().__init__(source_entity, target_entity, direct_name, backward_name, self.HAS_ONE)

    def validate_related_pk(self, related_pk):
        if not isinstance(related_pk, str) and not isinstance(related_pk, Empty) and related_pk is not None:
            raise InvalidRelationType('Relation "{relation_name}" has incorrect type'
                                      .format(relation_name=self.direct_name))


@metainfo
class MetaOneToManyRelation(MetaOneToXRelation):
    def create_instance(self, entity_instance, related_pk):
        self.validate_related_pk(related_pk)
        return OneToManyRelationInstance(related_pk, self, entity_instance)


@metainfo
class MetaOneToOneRelation(MetaOneToXRelation):
    def create_instance(self, entity_instance, related_pk):
        self.validate_related_pk(related_pk)
        return OneToOneRelationInstance(related_pk, self, entity_instance)


@metainfo
class MetaManyToXRelation(MetaRelation):
    def __init__(self, source_entity: MetaEntity,
                 target_entity: MetaEntity, direct_name, backward_name):
        super().__init__(source_entity, target_entity, direct_name, backward_name, self.HAS_MANY)

    def validate_related_pks(self, related_pks):
        if not isinstance(related_pks, list) and not isinstance(related_pks, Empty) and related_pks is not None:
            raise InvalidRelationType('Relation "{relation_name}" has incorrect type'
                                      .format(relation_name=self.direct_name))

    def create_empty(self, entity_instance):
        return self.create_instance(entity_instance, Empty())


@metainfo
class MetaManyToOneRelation(MetaManyToXRelation):
    def create_instance(self, entity_instance, related_pks):
        self.validate_related_pks(related_pks)
        return ManyToOneRelationInstance(related_pks, self, entity_instance)


@metainfo
class MetaManyToManyRelation(MetaManyToXRelation):
    def create_instance(self, entity_instance, related_pks):
        self.validate_related_pks(related_pks)
        return ManyToManyRelationInstance(related_pks, self, entity_instance)


@instance
class RelationInstance:
    def __init__(self, meta: MetaRelation, entity_instance):
        self.meta = meta
        self.entity_instance = entity_instance


@instance
class OneToXRelationInstance(RelationInstance):
    def __init__(self, related_pk, meta, entity_instance):
        super().__init__(meta, entity_instance)
        self.related_pk = related_pk

    def is_empty(self):
        return isinstance(self.related_pk, Empty)

    def __eq__(self, other):
        return id(other.meta) == id(self.meta) and \
                other.related_pk == self.related_pk

    def __hash__(self):
        return hash((self.meta, self.related_pk, self.entity_instance.meta, self.entity_instance.pk))


@instance
class OneToManyRelationInstance(OneToXRelationInstance):
    pass


@instance
class OneToOneRelationInstance(OneToXRelationInstance):
    pass


@instance
class ManyToXRelationInstance(RelationInstance):
    def __init__(self, related_pks, meta, entity_instance):
        super().__init__(meta, entity_instance)
        self.related_pks = related_pks

    def is_empty(self):
        return isinstance(self.related_pks, Empty)

    def __eq__(self, other):
        return id(other.meta) == id(self.meta) and \
                set(other.related_pks) == set(self.related_pks) and \
                other.entity_instance.meta == self.entity_instance.meta and \
                other.entity_instance.pk == self.entity_instance.pk

    def __hash__(self):
        return hash((self.meta, tuple(self.related_pks), self.entity_instance.meta, self.entity_instance.pk))


@instance
class ManyToOneRelationInstance(ManyToXRelationInstance):
    pass


@instance
class ManyToManyRelationInstance(ManyToXRelationInstance):
    pass


@instance
class EntityInstance:
    def __init__(self, meta: MetaEntity, attributes: Dict[str, object], pk=None):
        self.meta = meta
        self.attributes = attributes
        self._relation_instances_registry = {}
        self.relation_instances = self._get_initial_empty_relations()
        self.pk = pk

    def _get_initial_empty_relations(self):
        relation_instances = []
        for relation_meta in self.meta.relations:
            relation_instances.append(relation_meta.create_empty(self))
        return relation_instances

    @property
    def relation_instances(self):
        return self._relation_instances_registry.values()

    @relation_instances.setter
    def relation_instances(self, relation_instances):
        for r in relation_instances:
            self._relation_instances_registry[r.meta.direct_name] = r

    def __eq__(self, other):
        return id(other.meta) == id(self.meta) and \
            other.attributes == self.attributes and \
            other.pk == self.pk and \
            set(other.relation_instances) == set(self.relation_instances)

    def __hash__(self):
        return hash((self.meta, tuple(self.attributes.items()), self.pk, tuple(self.relation_instances)))


class Domain:
    def __init__(self, entities):
        self._entities = {entity.name: entity for entity in entities}

    def entity_exists(self, name):
        try:
            self.get_entity(name)
            return True
        except EntityNotFound:
            return False

    def get_entity(self, name) -> MetaEntity:
        try:
            return self._entities[name]
        except KeyError:
            raise EntityNotFound('{entity_name} entity not found'.format(entity_name=name))


@egg
class DomainFactory:
    def __init__(self, schema_proxy: SchemaProxy):
        self._schema_proxy = schema_proxy

        self._entities = self._generate_entities()
        self._domain = Domain(self._entities)
        self._generate_relations_meta_and_append_them_to_entities()

    def create(self):
        return self._domain

    def _generate_entities(self) -> List[MetaEntity]:
        domain_entities = []
        for entity_proxy in self._schema_proxy.entities:
            attributes = [attribute.name for attribute in entity_proxy.attributes]
            domain_entities.append(MetaEntity(entity_proxy.name, attributes))
        return domain_entities

    def _generate_relations_meta_and_append_them_to_entities(self):
        for r in self._schema_proxy.relations:
            source_entity = self._domain.get_entity(r.source)
            target_entity = self._domain.get_entity(r.target)

            if r.direct_type == r.HAS_ONE and r.backward_type == r.HAS_MANY:
                source_entity.add_relation(MetaOneToManyRelation(source_entity, target_entity, r.direct_name, r.backward_name))
                target_entity.add_relation(MetaManyToOneRelation(target_entity, source_entity, r.backward_name, r.direct_name))
            elif r.direct_type == r.HAS_MANY and r.backward_type == r.HAS_MANY:
                source_entity.add_relation(MetaManyToManyRelation(source_entity, target_entity, r.direct_name, r.backward_name))
                target_entity.add_relation(MetaManyToManyRelation(target_entity, source_entity, r.backward_name, r.direct_name))
            elif r.direct_type == r.HAS_ONE and r.backward_type == r.HAS_ONE:
                source_entity.add_relation(MetaOneToOneRelation(source_entity, target_entity, r.direct_name, r.backward_name))
                target_entity.add_relation(MetaOneToOneRelation(target_entity, source_entity, r.backward_name, r.direct_name))