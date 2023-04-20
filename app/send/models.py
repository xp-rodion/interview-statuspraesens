from django.db import models

from common.models import StripStringFieldsModel, ShortNameModel, CodeNameModel, TimeStampedModel, UidPrimaryModel, \
    UniqueCodeModel, NameModel, ShortNameModel


class Email(TimeStampedModel, UidPrimaryModel):
    STATUS_GENERATED = 1
    STATUS_PERFORMING = 11
    STATUS_ERROR = 21
    STATUS_SUCCESS = 31
    STATUS_CHOICES = (
        (STATUS_GENERATED, 'Создана'),
        (STATUS_PERFORMING, 'Выполняется'),
        (STATUS_ERROR, 'Ошибка'),
        (STATUS_SUCCESS, 'Выполнено'),
    )

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    receiver = models.EmailField('Адрес получателя', max_length=256)
    receiver_copy = models.EmailField('Адрес дополнительного получателя', max_length=256, blank=True)
    title = models.CharField('Заголовок письма', max_length=256)
    body = models.TextField('Тело письма')
    departure_date = models.DateTimeField(null=True, blank=True, verbose_name='Когда отправлен')
    result = models.JSONField('Результат отправки', default=dict)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ('modified',)

