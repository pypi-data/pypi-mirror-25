import abc

from pyramid.request import Request
from pyramid.response import Response

from ..builders.scrambler import egg
from . import context_producers


class RequestContextAndData:
    def __init__(self, origin, resource_name, body=None, params=None, query_params=None):
        # builder ?
        self.origin = origin
        self.body = body
        self.resource_name = resource_name
        self.params = params
        self.query_params = query_params

    @property
    def query_available(self):
        return 'q' in self.query_params

    @property
    def query(self):
        return self.query_params['q']

    @property
    def included_relations(self):
        return self.query_params['include'].split(',') if 'include' in self.query_params else []


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, context_producer):
        self.context_producer = context_producer

    @abc.abstractmethod
    def handle(self, request: Request) -> Response:
        pass

    @staticmethod
    def get_request_param(request: Request, param_name):
        return request.matchdict[param_name]

    @staticmethod
    def get_request_body(request: Request):
        return request.body.decode()

    def get_response(self, *args, **kwargs) -> Response:
        context = self.get_context(*args, **kwargs)
        return Response(**context, headers={'Content-Type': 'application/json'})

    def get_context(self, *args, **kwargs) -> dict:
        return self.context_producer.get_context(*args, **kwargs)


@egg
class CreateItemHandler(Handler):
    def __init__(self, context_producer: context_producers.CreateItemContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        request_body = self.get_request_body(request)
        request_context = RequestContextAndData(body=request_body,
                                                resource_name=entity_name,
                                                origin=request.host_url)

        return self.get_response(request_context)


@egg
class UpdateItemHandler(Handler):
    def __init__(self, context_producer: context_producers.UpdateItemContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        pk = self.get_request_param(request, 'pk')
        request_body = self.get_request_body(request)
        request_context = RequestContextAndData(body=request_body,
                                                resource_name=entity_name,
                                                params={'pk': pk},
                                                origin=request.host_url)
        return self.get_response(request_context)


@egg
class DeleteItemHandler(Handler):
    def __init__(self, context_producer: context_producers.DeleteItemContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        item_pk = self.get_request_param(request, 'pk')
        request_context = RequestContextAndData(resource_name=entity_name,
                                                params={'pk': item_pk},
                                                origin=request.host_url)

        return self.get_response(request_context)


@egg
class GetSingleItemHandler(Handler):
    def __init__(self, context_producer: context_producers.GetSingleItemContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        item_pk = self.get_request_param(request, 'pk')
        request_context = RequestContextAndData(resource_name=entity_name,
                                                params={'pk': item_pk},
                                                origin=request.host_url,
                                                query_params=request.params)
        return self.get_response(request_context)


@egg
class FindAllItemsHandler(Handler):
    def __init__(self, context_producer: context_producers.FindAllItemsContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        request_context = RequestContextAndData(resource_name=entity_name,
                                                origin=request.host_url,
                                                query_params=request.params)
        return self.get_response(request_context)


@egg
class FindRelationHandler(Handler):
    def __init__(self, context_producer: context_producers.FindRelationContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        item_pk = self.get_request_param(request, 'pk')
        relation_name = self.get_request_param(request, 'relation_name')
        request_context = RequestContextAndData(resource_name=entity_name,
                                                params={'pk': item_pk, 'relation_name': relation_name},
                                                origin=request.host_url)
        return self.get_response(request_context)


@egg
class UpdateRelationHandler(Handler):
    def __init__(self, context_producer: context_producers.UpdateRelationContextProducerWithErrorHandling):
        super().__init__(context_producer)

    def handle(self, request):
        entity_name = self.get_request_param(request, 'entity_name')
        item_pk = self.get_request_param(request, 'pk')
        relation_name = self.get_request_param(request, 'relation_name')
        request_body = self.get_request_body(request)
        request_context = RequestContextAndData(resource_name=entity_name,
                                                params={'pk': item_pk, 'relation_name': relation_name},
                                                body=request_body,
                                                origin=request.host_url)
        return self.get_response(request_context)