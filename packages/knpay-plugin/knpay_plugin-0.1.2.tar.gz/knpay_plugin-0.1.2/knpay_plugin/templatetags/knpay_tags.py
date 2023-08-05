# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict
from django.utils.translation import ugettext as _
from django import template
from knpay_plugin.conf import config


register = template.Library()


@register.simple_tag
def prepare_payload(payment_transaction):
    payload = OrderedDict()
    knpay_payload = payment_transaction.knpay_response
    gateway_payload = payment_transaction.gateway_response

    payload[_("Amount")] = '%s %s' % (payment_transaction.amount, payment_transaction.currency_code)
    payload[_("Order No")] = payment_transaction.order_no
    payload[_("Reference No")] = knpay_payload['reference_number']
    payload[_("Status")] = knpay_payload['result'].upper()
    payload[_("Gateway")] = config.GATEWAY_NAMES[knpay_payload['gateway_name'].lower()]

    for item in config.VAR_MAPPING:
        val = gateway_payload.get(item[0])
        if val:
            payload[item[1]] = val
    return payload


@register.inclusion_tag('knpay_plugin/gateway_choices.html', takes_context=True)
def show_gateway_choices(context):
    context['gateway_choices'] = config.GATEWAY_CHOICES
    return context
