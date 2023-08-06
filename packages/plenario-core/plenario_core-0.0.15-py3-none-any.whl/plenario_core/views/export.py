import json
from json.decoder import JSONDecodeError
from typing import Callable, List, Type

from django.conf import settings
from django.http import JsonResponse
from django.views import View

from plenario_core.models import MetaBase
from plenario_core.schemas import ExportRequestSchema
from plenario_core.views.bases import JsonResponseMixin


DB_NAME = settings.DATABASES['default']['NAME']


class GenericMetaExportView(JsonResponseMixin, View):
    models: List[Type[MetaBase]] = []
    async_handler: Callable = None

    def post(self, *args, **kwargs) -> JsonResponse:
        """
        {
            "ds_timerange": ...,
            "ds_bbox": ...,
            "data_sets": [
                {
                    "type": "EtlEventMeta",
                    "pk": 42,
                    "filter_point_field": "_meta_point_0",
                    "filter_date_field": "_meta_date_0",
                    "fields": [
                        "name", "location", "date"
                    ]
                }
            ]
        }
        """
        try:
            payload = json.loads(self.request.body)
        except JSONDecodeError:
            return self.render({'error': 'Could not parse request.'}, 400)

        schema = ExportRequestSchema()
        params, errors = schema.load(payload)
        if errors:
            return self.render(errors, 400)

        model_names = {
            model.__name__: model
            for model in self.models
        }

        requestor = params['email_address']
        timerange = params['ds_timerange']
        bbox = params['ds_bbox']
        data_sets = []
        for obj in params['data_sets']:
            model_class_name = obj['type']
            model = model_names[model_class_name]

            fields = obj['fields']
            pk = obj['pk']
            point_field = obj['filter_point_field']
            date_field = obj['filter_date_field']

            instance = model.objects.get(pk=pk)

            if not fields:
                fields = [
                    field['name']
                    for field in instance.ds_source_fields
                ]

            data_sets.append({
                'meta_model_app_label': instance._meta.app_label,
                'meta_model_class_name': instance.__class__.__name__,
                'meta_model_pk': instance.pk,
                'fields': fields,
                'point_field': point_field,
                'date_field': date_field,
                'timerange': timerange,
                'bbox': bbox,
            })

        job_id = self.async_handler(
            requestor_email=requestor.email, ds_info=data_sets)

        return self.render({'job_id': job_id})
