from jsonapidb.builders.scrambler import egg
from jsonapidb.model.domain import DomainFactory
from jsonapidb.serialization import utils
from jsonapidb.serialization.deserialiers.relation_instance_deserializers import RelationInstancesDeserializerFactory
from jsonapidb.serialization.utils import handle_invalid_format, invalid_format


class SingleEntityInstanceDeserializer:
    def __init__(self, raw_data: str,
                 relation_instances_deserializer_factory: RelationInstancesDeserializerFactory,
                 domain_factory: DomainFactory):
        self.relation_instances_deserializer_factory = relation_instances_deserializer_factory
        self.data = utils.unpack_data(raw_data)
        self.domain = domain_factory.create()

    @handle_invalid_format
    def deserialize(self):
        entity_instance = self._create_entity_instance()
        relation_instances = self._deserialize_relation_instances(entity_instance)
        if relation_instances is not None:
            entity_instance.relation_instances = relation_instances
        return entity_instance

    def _create_entity_instance(self):
        pk = self.data.get('id', None)
        attributes = self._deserialize_attributes()
        return self.domain.get_entity(self.data['type']).create_instance(attributes, pk)

    def _deserialize_relation_instances(self, entity_instance):
        if self._relations_in_data() and self._json_relations_are_valid():
            relations_data = self.data['relationships']
            relation_instances_deserializer = self.relation_instances_deserializer_factory\
                .create(relations_data, entity_instance)
            return relation_instances_deserializer.deserialize()
        elif self._relations_in_data() and not self._json_relations_are_valid():
            raise invalid_format()
        else:
            return None

    def _relations_in_data(self):
        return 'relationships' in self.data

    def _json_relations_are_valid(self) -> bool:
        return isinstance(self.data['relationships'], dict)

    def _deserialize_attributes(self) -> dict:
        if self._attributes_in_item() and self._item_attributes_are_valid():
            attributes = self.data['attributes']
        elif self._attributes_in_item() and not self._item_attributes_are_valid():
            raise invalid_format()
        else:
            attributes = {}

        return attributes

    def _attributes_in_item(self):
        return 'attributes' in self.data

    def _item_attributes_are_valid(self) -> bool:
        return isinstance(self.data['attributes'], dict)


@egg
class SingleEntityInstanceDeserializerFactory:
    def __init__(self, relation_instances_deserializer_factory: RelationInstancesDeserializerFactory,
                 domain_factory: DomainFactory):
        self.relation_instances_deserializer_factory = relation_instances_deserializer_factory
        self.domain_factory = domain_factory

    def create(self, data: str):
        return SingleEntityInstanceDeserializer(data, self.relation_instances_deserializer_factory, self.domain_factory)