from random import randrange

from django.utils.timezone import now
from rest_framework import serializers
from common.func import send_message

from .. import models


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = (
            'uid', 'receiver', 'receiver_copy', 'title', 'body', 'created', 'modified', 'departure_date', 'result',
            'status')
        read_only_fields = ('uid', 'created', 'modified', 'departure_date', 'result', 'status')

    def to_representation(self, obj):
        ret = super(EmailSerializer, self).to_representation(obj)
        ret['status'] = dict(models.Email.STATUS_CHOICES)[ret['status']]
        return ret

    def create(self, validated_data):
        email = models.Email.objects.create(**validated_data)
        send_message(email=email)
        return email
