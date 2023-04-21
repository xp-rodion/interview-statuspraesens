from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.urls import reverse
from validate_email.forms import EmailFileForm
from validate_email.models import EmailFile, EmailResult
from validate_email.tasks import validate_email_task


def upload_email_file(request):
    if request.method == 'POST':
        form = EmailFileForm(request.POST, request.FILES)
        if form.is_valid():
            email_file = EmailFile.objects.create(file=request.FILES['file'])
            validate_email_task.apply_async(kwargs={'email_file_id': email_file.id}, queue='validate_email') # Перезагружать страницу для отображения контента.
            return redirect(reverse('validate_email:email_detail', kwargs={"email_file_id": email_file.id}))
    else:
        form = EmailFileForm()
    return render(request, 'upload_email_file.html', context={'form': form})


def email_file_detail(request, email_file_id):
    results = EmailResult.objects.select_related('file').filter(file__pk=email_file_id)
    email_file_name = results.first().file.__str__()
    return render(request, 'detail_email_file.html', context={'email_file_name': email_file_name, 'results': results})
