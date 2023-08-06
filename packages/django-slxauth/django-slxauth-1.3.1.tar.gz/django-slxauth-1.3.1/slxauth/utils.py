import jwt
from django.contrib.auth import get_user_model, login
from jwt import DecodeError


def get_user_from_token(token):
    extra_data = jwt.decode(token, verify=False)

    user_model = get_user_model()
    u, created = user_model.objects.get_or_create(email=extra_data['email'])
    u.customer_no = extra_data['customerNumber']
    u.customer_name = extra_data['customerName']
    u.last_name = extra_data['lastName']
    u.first_name = extra_data['firstName']
    u.title = extra_data['title']
    u.is_customer_admin = extra_data['isCustomerAdmin']
    u.language = extra_data['language']
    u.crm_contact_id = extra_data['crmContactId']

    u.save()
    return u


def login_using_token(request, access_token):
    try:
        user = get_user_from_token(access_token)
        login(request, user)
    except DecodeError:
        pass

