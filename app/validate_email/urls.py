from django.urls import path
from validate_email.views import upload_email_file, email_file_detail

app_name = 'validate_email'

urlpatterns = [
    path('upload/', upload_email_file, name='upload'),
    path('email_detail/<int:email_file_id>/', email_file_detail, name='email_detail'),
]
