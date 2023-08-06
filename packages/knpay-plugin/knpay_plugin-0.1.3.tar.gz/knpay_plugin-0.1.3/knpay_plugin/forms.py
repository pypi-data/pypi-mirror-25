# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import base64
import logging
import re
import uuid
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.template.defaultfilters import striptags
from knpay_plugin.conf import config
from knpay_plugin.models import PaymentTransaction
import requests


logger = logging.getLogger(__name__)


def uuid_url64(payment_transaction=None):
    """
    Returns a unique, 16 byte, URL safe ID by combining UUID and Base64
    https://gist.github.com/mattupstate/8714628
    """
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


class PaymentForm(forms.Form):
    """
    Basic payment form which handles only required
    fields for KNPay transactions. Inherit this form
    to handle more complex situations.
    """
    if len(config.GATEWAY_CHOICES) > 1:
        gateway_code = forms.ChoiceField(label=_("Gateway"), choices=config.GATEWAY_CHOICES)
    else:
        gateway_code = forms.CharField(initial=config.GATEWAY_CHOICES[0][0],
                                       required=False,
                                       widget=forms.HiddenInput())
    amount = forms.CharField(label=_("Amount"))
    language = forms.ChoiceField(label=_("Language"), choices=PaymentTransaction.LANGUAGE_CHOICES)
    currency_code = forms.CharField(label=_("Currency code"))
    customer_first_name = forms.CharField(label=_("First name"))
    customer_last_name = forms.CharField(label=_("Last name"))
    customer_email = forms.CharField(label=_("Email"))
    customer_phone = forms.CharField(label=_("Phone"))
    customer_address_line1 = forms.CharField(label=_("Address line 1"), widget=forms.Textarea())
    customer_address_line2 = forms.CharField(label=_("Address line 1"), widget=forms.Textarea())
    customer_address_city = forms.CharField(label=_("City"))
    customer_address_state = forms.CharField(label=_("State"))
    customer_address_country = forms.ChoiceField(label=_("Country"), choices=PaymentTransaction.COUNTRY_CHOICES)
    customer_address_postal_code = forms.CharField(label=_("Postal code"))

    def __init__(self, request=None, extra=None, *args, **kwargs):
        if request is not None:
            self.request = request
        else:
            self.site = Site.objects.get_current()
        self.extra = extra or {}
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = field in config.MANDATORY_FORM_FIELDS
            if field not in config.VISIBLE_FORM_FIELDS:
                self.fields[field].widget = forms.HiddenInput()

    def _get_response_url(self, view_name, order_no):
        path = reverse(view_name, args=(order_no,))
        if hasattr(self, 'request'):
            return self.request.build_absolute_uri(path)
        else:
            return "%(protocol)s://%(domain)s%(path)s" % {
                'protocol': config.PROTOCOL,
                'domain': self.site.domain,
                'path': path
            }

    def _get_data(self):
        order_no = config.generate_order_no()
        data = {
            'order_no': order_no,
            'disclosure_url': self._get_response_url(config.DISCLOSURE_VIEW_NAME, order_no),
            'redirect_url': self._get_response_url(config.REDIRECTED_VIEW_NAME, order_no),
            'extra': self.extra
        }
        for field in self.fields:
            val = self.cleaned_data.get(field, '')
            if val:
                data.update({field: val})
        if not config.RENDER_FORM and len(config.GATEWAY_CHOICES) == 1:
            data['gateway_code'] = self.fields['gateway_code'].initial
        return data

    @property
    def errors_as_dict(self):
        errors = {}
        for error in self.errors.iteritems():
            errors[error[0]] = unicode(striptags(error[1]))
        return errors

    def connect(self):
        data = self._get_data()
        try:
            response = requests.post(config.get_knpay_url(), json=data, timeout=35, verify=False)
        except Exception as e:
            self._errors = {'__all__': str(e)}
            logger.error("Error occurred while connecting to knpay %s" % e)
            return
        if response.status_code == requests.codes.ok:
            del data['disclosure_url']
            del data['redirect_url']
            data['payment_url'] = response.json()['url']
            self.instance = PaymentTransaction.objects.create(**data)
            return self.instance.payment_url
        else:
            self._errors = {key: ' '.join(val) for key, val in response.json().items()}
            logger.error("Following error %s returned by knpay" % response.content.decode('utf-8'))
