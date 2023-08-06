import logging
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError as DjValidationError
from django.db import transaction, IntegrityError as DjIntegrityError
from django.http import JsonResponse
from marshmallow import ValidationError as MmValidationError
from psycopg2 import IntegrityError as PgIntegrityError

from plenario_core.views.bases import DetailView, JsonResponseMixin, ListView


logger = logging.getLogger(__name__)


class GenericMetaFetchView(JsonResponseMixin, DetailView):
    """A generic view for fetching a single instance of a meta data model.
    """

    def get(self, *args, **kwargs) -> JsonResponse:
        try:
            instance = self._get_object()
        except self.model.DoesNotExist:
            return self.render({'error': f'Could not find {self.model}'}, 404)

        response_body = self._prepare_response_body(instance)
        return self.render(response_body)


class GenericMetaListView(JsonResponseMixin, ListView):
    """A generic view for listing multiple instances of a meta data model.
    """

    def get(self, *args, **kwargs) -> JsonResponse:
        instances = self._get_objects()
        response_body = self._prepare_response_body(instances)
        return self.render(response_body)


class GenericMetaCreateView(JsonResponseMixin, ListView):
    """A generic view for creating a new instance of a meta data model.
    """

    def post(self, *args, **kwargs) -> JsonResponse:
        try:
            instance = self._handle_request_body()
        except JSONDecodeError:
            return self.render({'error': 'Could not decode payload.'}, 400)
        except MmValidationError as error:
            return self.render(error.normalized_messages(), 400)

        try:
            with transaction.atomic():
                instance.save()
        except (DjIntegrityError, PgIntegrityError, DjValidationError) as error:
            logger.exception(error)
            message = str(error).split(':')[0]
            return self.render({'error': message}, 400)

        response_body = self._prepare_response_body(instance)
        return self.render(response_body, 201)


class GenericMetaUpdateView(JsonResponseMixin, DetailView):
    """A generic view for updating a single instance of a meta data model.
    """

    def put(self, *args, **kwargs) -> JsonResponse:
        try:
            instance = self._get_object()
        except self.model.DoesNotExist:
            return self.render({'error': f'Could not find {self.model}'}, 404)

        try:
            updated = self._handle_request_body(instance)
        except JSONDecodeError:
            return self.render({'error': 'Could not decode payload.'}, 400)
        except MmValidationError as error:
            return self.render(error.normalized_messages(), 400)

        try:
            with transaction.atomic():
                updated.save()
        except (DjIntegrityError, PgIntegrityError, DjValidationError) as error:
            logger.exception(error)
            message = str(error).split(':')[0]
            return self.render({'error': message}, 400)

        response_body = self._prepare_response_body(updated)
        return self.render(response_body)

    def patch(self, *args, **kwargs) -> JsonResponse:
        try:
            instance = self._get_object()
        except self.model.DoesNotExist:
            return self.render({'error': f'Could not find {self.model}'}, 404)

        try:
            updated = self._handle_request_body(instance, partial=True)
        except JSONDecodeError:
            return self.render({'error': 'Could not decode payload.'}, 400)
        except MmValidationError as error:
            return self.render(error.normalized_messages(), 400)

        try:
            with transaction.atomic():
                updated.save()
        except (DjIntegrityError, PgIntegrityError, DjValidationError) as error:
            logger.exception(error)
            message = str(error).split(':')[0]
            return self.render({'error': message}, 400)

        response_body = self._prepare_response_body(updated)
        return self.render(response_body)


class GenericMetaDeleteView(JsonResponseMixin, DetailView):
    """A generic view for deleting a single instance of a meta data model.
    """

    def delete(self, *args, **kwargs) -> JsonResponse:
        try:
            instance = self._get_object()
        except self.model.DoesNotExist:
            return self.render({'error': f'Could not find {self.model}'}, 404)

        with transaction.atomic():
            instance.delete()

        return self.render({'deleted': True}, 204)
