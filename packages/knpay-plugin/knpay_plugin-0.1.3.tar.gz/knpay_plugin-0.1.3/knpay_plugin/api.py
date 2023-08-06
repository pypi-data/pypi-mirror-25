# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal
from knpay_plugin.forms import PaymentForm
from knpay_plugin.conf import config


def create_payment_url(amount, gateway_code=None, request=None, extra=None, **data):
    """
    :param amount: str, float or Decimal
    :param gateway_code: str
    :param request: HttpRequest instance
    :param extra: dict with keys required to be sent extra to knpay and
                  saved in extra field of PaymentTransaction {'basket_id': '12', 'food': 'chinese'}
    :param data: dict with fields existing on PaymentTransaction {'currency_code': 'KWD', 'language': 'en',}
    :return: bool, dict OR PaymentTransaction instance
    """
    if isinstance(amount, Decimal):
        amount = str(amount)

    data.update({
        'amount': amount,
        'currency_code': data.get('currency_code', config.DEFAULT_CURRENCY)
    })
    if gateway_code is not None:
        data.update({
            'gateway_code': gateway_code,
        })
    form = PaymentForm(request=request, extra=extra, data=data)
    if form.is_valid():
        url = form.connect()
        if url is not None:
            return url, True
        return form.errors, False
    return form.errors_as_dict, False
