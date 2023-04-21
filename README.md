# interview-statuspraesens


1. Clone repository

```shell
$ git clone https://github.com/xp-rodion/interview-statuspraesens
```
   
2. env:
```shell
$ pipenv install
```
Также стоит поменять настройки БД на свои.

3. Run server
```shell
$ python3 manage.py migrate
$ python3 manage.py runserver
$ celery -A config worker --queues=gmail.com_queue,mail.ru_queue,anything_queue,validate_email
```

# Task 1
Сервис был реализован в приложении send.
Описана рассылка с помощью функции send_message, она используется в классе Command.
Используют асихронную функцию send_message, имеется 3 очереди, работают происходит в них в зависимости от домена.
Настроена часть SMTP для корректной рассылки. 

# Task 2 
Сервис был реализован в приложении validate_email.
Написан интерфейс для валидности почт. 
http://127.0.0.1:8000/validate_email/upload/ - url для загрузки файла excel, при загрузке первый столбец должен быть mail. 
Для легковесности использовал встроенную библиотеку, поэтому ориентацию по столбцам не сделал, это можно осуществить с помощью numpy, но не стал грузить проект. В проде обязательно делать с numpy.
http://127.0.0.1:8000/validate_email/email_detail/<int:email_file_id>/ - url, где будут результаты валидации, также хочу отметить, что надо перезагружать страницу, чтобы проверочные mail прогружались, 
т.к таска асихронная и не мешает работать пользователю. 
сделал для нее очередь validate_email.