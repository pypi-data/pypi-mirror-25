# from django.conf import settings
from .models import Customer, User


def get_customer(request, create=True):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            if create:
                customer = Customer(user=request.user)
                customer.save()
            else:
                customer = None
    else:
        try:
            customer = Customer.objects.get(session_id=request.session.session_key)
        except Customer.DoesNotExist:
            if create:
                if not request.session.exists(request.session.session_key):
                    request.session.create()
                customer = Customer.objects.create(session_id=request.session.session_key)
                request.session['customer_id'] = str(customer.id)
            else:
                customer = None
    return customer


def create_user_for_customer(customer, email, phone):
    from .models import PasswordResetLink
    user = User.objects.create_user(
        email=email,
        phone=phone,
        password=None,
    )
    user.set_unusable_password()
    user.save()
    customer.user = user
    customer.save()

    # Create a link for setup password
    reset_link = PasswordResetLink.objects.create(user=user)
    # Send email to the new user
    reset_link.send_message()
    return user


def clean_old_anonymous_customers():
    from django.utils.timezone import now
    from datetime import timedelta

    limit_date = now() - timedelta(days=14)

    customers = Customer.objects.filter(
        user=None,
        changed__lt=limit_date,
    )
    customers.delete()
