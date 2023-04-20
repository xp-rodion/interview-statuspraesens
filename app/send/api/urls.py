from django.urls import path

from . import views

app_name = 'send'

urlpatterns = [
    path('', views.CreateEmailAPI.as_view(), name='create_email'),
    path('result/<uuid:pk>', views.RetrieveEmailAPI.as_view(), name='result'),
]
