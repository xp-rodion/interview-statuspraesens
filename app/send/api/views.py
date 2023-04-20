from rest_framework import generics

from . import serializers
from .. import models


class CreateEmailAPI(generics.CreateAPIView):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()


class RetrieveEmailAPI(generics.RetrieveAPIView):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()
