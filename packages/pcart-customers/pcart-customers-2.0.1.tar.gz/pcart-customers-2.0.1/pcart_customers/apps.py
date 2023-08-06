from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PCartCustomersConfig(AppConfig):
    name = 'pcart_customers'
    verbose_name = _('Customers')
