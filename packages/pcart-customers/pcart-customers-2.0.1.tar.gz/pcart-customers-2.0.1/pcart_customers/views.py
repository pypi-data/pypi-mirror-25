from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseForbidden, Http404, HttpResponseRedirect
from django.utils.module_loading import import_string
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import (
    Customer,
    PasswordResetLink,
)
from .utils import get_customer


RESET_LINK_EXPIRATION = 60


@login_required(login_url=reverse_lazy('pcart_customers:login'))
def personal_information(request, template_name='customers/personal_information.html'):
    user = request.user
    customer = get_customer(request)
    context = {
        'user': user,
        'customer': customer,
        'customer_menu': settings.PCART_CUSTOMER_PROFILE_SECTIONS,
    }
    return render(request, template_name, context)


@login_required(login_url=reverse_lazy('pcart_customers:login'))
def personal_information_edit(request, template_name='customers/customer_edit.html'):
    from .forms import EditCustomerForm
    user = request.user
    customer = get_customer(request)

    if request.method == 'POST':
        form = EditCustomerForm(instance=customer, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('pcart_customers:personal-information'))
    else:
        form = EditCustomerForm(instance=customer)

    context = {
        'user': user,
        'customer': customer,
        'customer_menu': settings.PCART_CUSTOMER_PROFILE_SECTIONS,
        'form': form,
    }
    return render(request, template_name, context)


@csrf_exempt
def profile_section(request, slug, sub_slug=None):
    for section in settings.PCART_CUSTOMER_PROFILE_SECTIONS:
        if slug == section['slug']:
            if request.user.is_anonymous() and not section.get('allowed_for_anonymous', False):
                return HttpResponseRedirect(
                    '%s?next=%s' % (
                        reverse('pcart_customers:login'),
                        request.path,
                    ))
            view = import_string(section['view'])
            kwargs = section.get('kwargs', dict())
            if sub_slug is not None:
                kwargs['subsection'] = sub_slug
            return view(request, **kwargs)
    return HttpResponseNotFound('Unknown profile section')


def customer_toolbar(request, template_name='customers/includes/_customer_toolbar_content.html'):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, template_name, context)


def reset_request(request, template_name='customers/password_reset.html'):
    from datetime import timedelta
    from .models import User
    from .forms import UserPasswordResetRequestForm

    if request.user.is_authenticated():
        return HttpResponseForbidden('Access denied.')

    if request.method == 'POST':
        form = UserPasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            _user = User.objects.get(email=email)
            now = timezone.now()
            expiration_date = now + timedelta(minutes=RESET_LINK_EXPIRATION)
            reset_link = PasswordResetLink.objects.create(user=_user, expiration_date=expiration_date)
            reset_link.send_message()
            return redirect(reverse('pcart_customers:password-reset-done'))
    else:
        form = UserPasswordResetRequestForm()

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def reset_request_done(request, template_name='customers/password_reset_done.html'):
    context = {
        'link_expiration': RESET_LINK_EXPIRATION,
    }
    return render(request, template_name, context)


def reset_confirm(request, slug, template_name='customers/password_reset_confirm.html'):
    from .forms import UserPasswordSetupForm
    if request.user.is_authenticated():
        return HttpResponseForbidden('Access denied.')
    try:
        now = timezone.now()
        reset_link = PasswordResetLink.objects.get(slug=slug, active=True, expiration_date__gte=now)

        if request.method == 'POST':
            form = UserPasswordSetupForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password2']
                _user = reset_link.user
                _user.set_password(new_password)
                _user.save()

                reset_link.active = False
                reset_link.save()

                login(request, _user)
                return redirect(reverse('pcart_customers:personal-information'))
        else:
            form = UserPasswordSetupForm()

        context = {
            'reset_link': reset_link,
            'user': request.user,
            'form': form,
        }
        return render(request, template_name, context)
    except PasswordResetLink.DoesNotExist:
        return HttpResponseNotFound('Invalid token.')


def login_view(request, template_name='customers/login.html'):
    from .forms import UserAuthForm
    from pcart_cart.utils import get_or_create_cart
    from django.core.exceptions import ObjectDoesNotExist

    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    current_site = get_current_site(request)

    move_cart = 'move-cart' in request.GET

    if request.user.is_authenticated:
        if redirect_to == request.path:
            raise ValueError('Redirection loop for authenticated user detected.')
        return redirect(reverse('pcart_customers:personal-information'))
    elif request.method == 'POST':
        form = UserAuthForm(request, data=request.POST)
        if form.is_valid():
            old_customer = get_customer(request, create=False)
            login(request, form.get_user())
            # If old customer already have a cart than link to the user
            if move_cart and old_customer is not None:
                try:
                    old_cart = old_customer.carts.get(site=current_site)
                    new_customer = get_customer(request)
                    new_cart = get_or_create_cart(current_site, new_customer)
                    new_cart.copy_from(old_cart)
                except ObjectDoesNotExist:
                    pass
            if redirect_to == '':
                redirect_to = reverse('pcart_customers:personal-information')
            return redirect(redirect_to)
    else:
        form = UserAuthForm(request)

    context = {
        'form': form,
        'next': redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    return render(request, template_name, context)


def register(request, template_name='customers/register.html'):
    from .forms import UserRegistrationForm
    if request.user.is_authenticated():
        return redirect(reverse('pcart_customers:personal-information'))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = get_customer(request, create=False)
            if customer:
                customer.user = user
                customer.save()
            else:
                customer = Customer(user=user)
                customer.save()
            login(request, user)
            return redirect(reverse('pcart_customers:personal-information'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, template_name, context)
