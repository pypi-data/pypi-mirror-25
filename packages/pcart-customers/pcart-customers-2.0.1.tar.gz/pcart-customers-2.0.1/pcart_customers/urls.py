from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm
from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'customers/logout.html'},
        name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(
        r'^password-change/$',
        auth_views.password_change,
        {
            'template_name': 'customers/password_change_form.html',
            'post_change_redirect': 'pcart_customers:password-change-done',
        },
        name='password-change'),
    url(
        r'^password-change/done/$',
        auth_views.password_change_done,
        {'template_name': 'customers/password_change_done.html'},
        name='password-change-done'),
    url(r'^password-reset/$', views.reset_request, name='password-reset'),
    url(r'^password-reset/done/$', views.reset_request_done, name='password-reset-done'),
    url(r'^password-reset/(?P<slug>.+)/confirm/$', views.reset_confirm, name='password-reset-confirm'),
    url(r'^personal-information/$', views.personal_information, name='personal-information'),
    url(r'^personal-information/edit/$', views.personal_information_edit, name='personal-information-edit'),
    url(r'^customer-toolbar/$', views.customer_toolbar, name='customer-toolbar'),
    url(r'^(?P<slug>[\w\d-]+)/$', views.profile_section, name='customer-profile-section'),
    url(
        r'^(?P<slug>[\w\d-]+)/(?P<sub_slug>[\w\d-]+)/$',
        views.profile_section, name='customer-profile-section-subsection'),
]
