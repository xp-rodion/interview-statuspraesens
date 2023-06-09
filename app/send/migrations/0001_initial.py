# Generated by Django 3.1.4 on 2020-12-21 15:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Когда создан')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Когда изменён')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный идентификатор')),
                ('status', models.SmallIntegerField(choices=[(1, 'Создана'), (11, 'Выполняется'), (21, 'Ошибка'), (31, 'Выполнено')], default=1)),
                ('receiver', models.EmailField(max_length=256, verbose_name='Адрес получателя')),
                ('receiver_copy', models.EmailField(blank=True, max_length=256, verbose_name='Адрес дополнительного получателя')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок письма')),
                ('body', models.TextField(verbose_name='Тело письма')),
                ('departure_date', models.DateTimeField(blank=True, null=True, verbose_name='Когда отправлен')),
                ('result', models.JSONField(default=dict, verbose_name='Результат отправки')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
                'ordering': ('modified',),
            },
        ),
    ]
