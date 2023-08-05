# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import importlib
from urlparse import urljoin
from appconf import AppConf
from django.utils.translation import ugettext_lazy as _


class KnpayPluginConf(AppConf):
    # currency
    DEFAULT_CURRENCY = 'KWD'

    # gateway (override at your own choice)
    GATEWAY_CHOICES = (
        ('knet', _('Knet')),
        ('cybersource', _('Credit Card')),
        ('migs', _('Credit Card')),
        ('paypal', _('Paypal')),
        ('mpgs', _('Credit Card')),
    )

    # knpay url
    BASE_URL = 'http://knpay3.mykuwaitnet.net/'

    def get_knpay_url(self):
        return urljoin(self.BASE_URL, '/pos/crt/')

    # admin
    ADMIN_SHOW_OPTIONAL_FIELDS = False
    ADMIN_SHOW_EXTRA_FIELD = False

    # urls
    DISCLOSURE_VIEW_NAME = 'kp_disclosure'
    REDIRECTED_VIEW_NAME = 'kp_complete'
    PROTOCOL = 'http'
    COMPLETE_VIEWS_REGEX = '(?P<order_no>[0-9A-Za-z_\-]+)'

    # form
    MANDATORY_FORM_FIELDS = ('amount', 'currency_code')
    VISIBLE_FORM_FIELDS = []

    # define if the payment form shall be rendered on the page
    RENDER_FORM = False

    # order generator function
    # make sure the function returns url safe order
    # and it's unique for each request to knpay
    GENERATE_ORDER_FUNC = 'knpay_plugin.forms.uuid_url64'

    def generate_order_no(self, payment_transaction=None):
        mod_name, func_name = self.GENERATE_ORDER_FUNC.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return func(payment_transaction=payment_transaction)

    # template
    VAR_MAPPING = [
        # knet
        ('result', _("Result")),
        ('trackid', _("Track ID")),
        ('postdate', _("Post Date")),
        ('tranid', _("Transaction ID")),
        ('paymentid', _("Payment ID")),
        ('auth', _("Auth ID")),
        ('ref', _("Reference ID")),

        # CS
        ('decision', _("Decision")),
        ('transaction_id', _("Transaction ID")),

        # MiGS
        ('vpc_Message', _("Message")),
        ('vpc_ReceiptNo', _("Receipt No")),
        ('vpc_TransactionNo', _("Transaction No")),
    ]

    GATEWAY_NAMES = {
        'migs': _("MiGS"),
        'knet': _("Knet"),
        'mpgs': _("MPGS"),
        'paypal': _("PayPal"),
        'cybersource': _("CyberSource")
    }

    class Meta:
        prefix = 'KNPAY'
        proxy = False
        required = [
            'GATEWAY_CHOICES',
            'BASE_URL'
        ]


config = KnpayPluginConf()
