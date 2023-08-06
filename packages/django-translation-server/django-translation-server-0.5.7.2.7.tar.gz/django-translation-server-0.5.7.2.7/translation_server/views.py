from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.conf import settings
from translation_server.models import *
from translation_server.serializers import *
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from rest_framework.permissions import AllowAny


class TranslationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'tag', 'type')


class TranslationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TranslationType.objects.all()
    serializer_class = TranslationTypeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'tag')


class LastTranslationTagView(views.APIView):
    def get(self, request, *args, **kwargs):
        if len(kwargs['tag']) > 0:
            try:
                int(kwargs['tag'])
            except ValueError:
                try:
                    model = TranslationType.objects.get(tag=kwargs['tag'])
                except TranslationType.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    model = TranslationType.objects.get(pk=kwargs['tag'])
                except TranslationType.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            last_translation_tag = LastTranslationTag(model.tag, *args, **kwargs)
            result = last_translation_tag.return_last_tag()
        else:
            result = dict(result=dict())
        return Response(result, status=status.HTTP_200_OK)