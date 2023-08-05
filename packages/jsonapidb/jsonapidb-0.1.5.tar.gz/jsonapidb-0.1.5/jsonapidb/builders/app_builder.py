from importlib import import_module

from jsonapidb.builders import scrambler
from jsonapidb.builders.json_proxy import SchemaProxy
from pyramid.config import Configurator


class AppConfig:
    def __init__(self, db_name, url_root):
        self.db_name = db_name
        self.url_root = url_root


class AppBuilder:
    def __init__(self, schema: SchemaProxy, config: AppConfig):
        self.schema = schema
        self.config = config

    def build_app(self):
        eggs = self.build_eggs()
        config = Configurator()

        config.add_route('create_item', '/{entity_name}', request_method='POST')
        config.add_view(eggs['CreateItemHandler'].handle, route_name='create_item', request_method='POST')

        config.add_route('update_item', '/{entity_name}/{pk}', request_method='PATCH')
        config.add_view(eggs['UpdateItemHandler'].handle, route_name='update_item', request_method='PATCH')

        config.add_route('delete_item', '/{entity_name}/{pk}', request_method='DELETE')
        config.add_view(eggs['DeleteItemHandler'].handle, route_name='delete_item')

        config.add_route('get_single_item', '/{entity_name}/{pk}', request_method='GET')
        config.add_view(eggs['GetSingleItemHandler'].handle, route_name='get_single_item')

        config.add_route('get_all_items', '/{entity_name}', request_method='GET')
        config.add_view(eggs['FindAllItemsHandler'].handle, route_name='get_all_items')

        config.add_route('find_relation', '/{entity_name}/{pk}/relationships/{relation_name}', request_method='GET')
        config.add_view(eggs['FindRelationHandler'].handle, route_name='find_relation')

        config.add_route('update_relation', '/{entity_name}/{pk}/relationships/{relation_name}', request_method='PATCH')
        config.add_view(eggs['UpdateRelationHandler'].handle, route_name='update_relation')

        app = config.make_wsgi_app()

        return app

    def build_eggs(self):
        eggs = scrambler.ModulesBuilder(
            modules=[
                import_module('jsonapidb.model.repository.engine_registry'),
                import_module('jsonapidb.model.repository.repository'),
                import_module('jsonapidb.model.repository.relations_repository'),
                import_module('jsonapidb.model.validators.attr_validation'),
                import_module('jsonapidb.model.validators.validator'),
                import_module('jsonapidb.model.validators.relations_validation'),
                import_module('jsonapidb.model.core'),
                import_module('jsonapidb.conversion.converters'),
                import_module('jsonapidb.serialization'),
                import_module('jsonapidb.api.handlers'),
                import_module('jsonapidb.api.context_producers')
            ],
            initial_eggs=[
                scrambler.EggFactory.create_from_instance(self.schema),
                scrambler.EggFactory.create_from_instance(self.config),
            ]
        ).build()

        return eggs