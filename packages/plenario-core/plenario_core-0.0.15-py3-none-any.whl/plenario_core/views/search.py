import json
import logging
from json.decoder import JSONDecodeError
from typing import Dict, Type

from django.db.models import Manager, Q
from django.http import JsonResponse
from django.views import View
from marshmallow import Schema

from plenario_core import services
from plenario_core.models import MetaBase
from plenario_core.schemas import SearchSchema
from plenario_core.views.bases import JsonResponseMixin

logger = logging.getLogger(__name__)


class GenericMetaSearchView(JsonResponseMixin, View):
    """A generic view for handling searches of meta data.
    """

    manager_map: Dict[Type[MetaBase], Manager] = None
    serializer_map: Dict[Type[MetaBase], Schema] = None

    def post(self, *args, **kwargs) -> JsonResponse:
        try:
            payload = json.loads(self.request.body)
        except JSONDecodeError:
            return self.render({'error': 'Could not parse payload.'}, 400)

        search_schema = SearchSchema()
        params, errors = search_schema.load(payload)
        if errors:
            return self.render(errors, 400)

        results = []
        for model, manager in self.manager_map.items():
            # build the filters depending on model attrs
            qs = []
            for key, value in params.items():
                if hasattr(model, key):
                    if key == 'ds_timerange':
                        key = f'{key}__overlap'
                    elif key == 'ds_bbox':
                        key = f'{key}__intersects'
                    qs.append(Q(**{key: value}))

            # filter the queryset
            result = manager.filter(*qs)

            # get the serializer and dump the queryset to json
            serializer = self.serializer_map[model]
            serialized = services.serialize_meta_model(
                result, serializer, many=True)

            # add the serialized queryset to the output
            results.extend(serialized)

        return self.render(results)
