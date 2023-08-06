import json
import logging
from typing import Optional, Type, Union

from django.db.models import Manager, QuerySet
from django.http import JsonResponse
from django.views import View
from marshmallow import Schema

from plenario_core import services
from plenario_core.models import MetaBase


logger = logging.getLogger(__name__)


class JsonResponseMixin:
    """A mixin model that provides JSON serialized responses.
    """

    @staticmethod
    def render(
            body: Union[dict, list], status: Optional[int]=200) -> JsonResponse:
        """Returns a JSON response to the client.

        :param body: the JSON response body/payload
        :param status: the status code of the response
        :return: a JSON response
        """
        return JsonResponse(data=body, status=status, safe=False)


class BaseView(View):
    """A base view object that provides configurations and lookups.
    """

    model: Type[MetaBase] = None
    manager: Manager = None
    serializer: Schema = None
    deserializer: Schema = None

    def _get_queryset(self) -> QuerySet:
        if self.manager:
            return self.manager.all()
        return self.model.objects.all()  # NOQA

    def _handle_request_body(
            self,
            instance: Optional[MetaBase]=None,
            partial: Optional[bool]=False) -> MetaBase:
        # raises JSONDecodeError
        # raises ValidationError
        payload = json.loads(self.request.body)
        deserialized = services.deserialize_to_meta_model(
            payload=payload, deserializer=self.deserializer,
            model_class=self.model, instance=instance, partial=partial)
        return deserialized

    def _prepare_response_body(
            self, instance_s: Union[MetaBase, QuerySet]) -> dict:
        many = hasattr(instance_s, 'count') and callable(instance_s.count)
        serialized = services.serialize_meta_model(
            instance=instance_s, serializer=self.serializer, many=many)
        return serialized


class DetailView(BaseView):
    """A base view extension for use with single model endpoints.
    """

    pk_url_kwarg: str = 'pk'
    # slug_url_kwarg: str = 'slug'
    # query_pk_and_slug: bool = False

    def _get_object(self) -> MetaBase:
        # raises self.model.DoesNotExist
        queryset = self._get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        # slug = self.kwargs.get(self.slug_url_kwarg)
        # if self.query_pk_and_slug:
        #     return queryset.get(pk=pk, slug=slug)
        if pk:
            return queryset.get(pk=pk)
        # if slug:
        #     return queryset.get(slug=slug)


class ListView(BaseView):
    """A base view extension for use with listed model endpoints.
    """

    order_by: str = '-pk'
    page_size: int = 20
    max_page_size: int = 100

    def _get_objects(self) -> QuerySet:
        order = self.request.GET.get('order', self.order_by)
        page_size = self.request.GET.get('size', self.page_size)
        page_num = self.request.GET.get('page', 1)

        try:  # NOQA
            page_size = int(page_size)
        except (ValueError, TypeError):  # NOQA
            page_size = self.page_size

        try:  # NOQA
            page_num = int(page_num)
        except (ValueError, TypeError):  # NOQA
            page_num = 1

        if page_size > self.max_page_size:
            page_size = self.max_page_size

        queryset = self._get_queryset().order_by(order)

        stop = page_size * page_num
        start = stop - page_size

        return queryset[start:stop]
