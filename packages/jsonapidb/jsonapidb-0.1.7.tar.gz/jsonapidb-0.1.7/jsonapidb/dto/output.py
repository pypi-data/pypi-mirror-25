from typing import List

from jsonapidb.model.domain import EntityInstance


class GetSingleObjectOutputDTO:
    def __init__(self, entity_instance: EntityInstance,
                 included_instances: List[EntityInstance]):
        self.entity_instance = entity_instance
        self.included_instances = included_instances


class FindAllObjectsOutputDTO:
    def __init__(self, entity_instances: List[EntityInstance],
                 included_instances: List[EntityInstance]):
        self.entity_instances = entity_instances
        self.included_instances = included_instances
