import re
from collections import OrderedDict
from send.models import Email
from send.tasks import send_email
import openpyxl


def is_not_empty(d):
    if isinstance(d, list):
        return any([is_not_empty(x) for x in d])
    if isinstance(d, dict) or isinstance(d, OrderedDict):
        return any([is_not_empty(x) for x in d.values()])
    else:
        return bool(d)


def none_to_blank(s: str) -> str:
    if s is None:
        return ''
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def dict_none_to_blank(d: dict) -> dict:
    for key, value in d.items():
        if isinstance(value, str) or value is None:
            d[key] = none_to_blank(value)
    return d


def get_domain_name_email(email_address: str) -> str:
    """The function truncates the string from @ to the end of the domain name."""
    at_index = email_address.find('@')
    domain_name = email_address[at_index:]
    return domain_name


def send_message(email: Email) -> None:
    """
    The function has 3 celery queues.
    Where two domains are allocated with the same name queue,
    and the others have the same name queue.
    """
    domain_dict = {'@gmail.com': 'gmail.com_queue', '@mail.ru': 'mail.ru_queue'}
    email_address = email.receiver
    domain_name = get_domain_name_email(email_address)
    queue = 'anything_queue'
    if domain_name in domain_dict:
        queue = domain_dict[domain_name]
    try:
        send_email.apply_async(kwargs={'email_uid': email.uid}, queue=queue)
        email.status = Email.STATUS_SUCCESS
        email.result = {'status': 'OK'}
    except (Exception, ):
        email.status = Email.STATUS_ERROR
        email.result = {'error': 'Error code 451. Requested action aborted: local error in processing.'}
    email.save()


def get_email_addresses(name_xlsx_file):
    workbook = openpyxl.load_workbook(name_xlsx_file)
    columns = []

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]

        used_columns = sheet.columns

        for column in used_columns:
            if column[0].value == "mail":
                for mail in column:
                    if not (mail.value is None):
                        columns.append(mail.value)

    return columns[1:]