from django.db import models


class EmailFile(models.Model):
    file = models.FileField("Файл с email-ами", upload_to='file_emails/')
    created_at = models.DateTimeField("Дата загрузки файла", auto_now_add=True)

    def __str__(self):
        return self.file.name


class EmailResult(models.Model):
    file = models.ForeignKey(EmailFile, on_delete=models.CASCADE)
    email = models.EmailField("Email")
    is_valid = models.BooleanField("Правильность email'a")


