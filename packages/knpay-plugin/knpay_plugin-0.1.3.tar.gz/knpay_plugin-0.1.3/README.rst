============
KNPay Plugin
============

Connects KNPay into your project

Quick start
-----------

Installation
------------

1. Using pip:

.. code-block:: bash

    $ pip install knpay_plugin


2. Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'knpay_plugin.apps.KnpayPluginConfig',
        ...
    )


3. Add KNPay Plugin's URL patterns:

.. code-block:: python

    from knpay_plugin import urls as knpay_plugin_urls


    urlpatterns = [
        ...
        url(r'^payment/', include(knpay_plugin_urls)),
        ...
    ]


4. Sync database (``./manage.py migrate``).


Demo
----

Let's say we have a django app called `checkout` and the below files.

**checkout/views.py**

.. code-block:: python

    from django.views.generic import FormView
    from knpay_plugin.views import CreatePaymentMixin, BaseCompletedView
    from knpay_plugin.forms import PaymentForm


    class CreatePaymentView(CreatePaymentMixin, FormView):
        template_name = 'knpay_plugin/payment_method.html'

        def get_initial(self):
            initial = super(CreatePaymentView, self).get_initial()
            initial.update({
                'amount': '123.000',
                # and rest of the model fields can be filled here
            })
            return initial


    class CompletedView(BaseCompletedView):
        template_name = 'checkout/payment_details.html'

        def handle_successful_payment(self, request, *args, **kwargs):
            # this method will be called only once
            # place order
            # add success message
            # return to get method
            return self.get(request, *args, **kwargs)

        def handle_canceled_payment(self, request, *args, **kwargs):
            # this method will be called only once
            # payment failed to various reasons
            # add error message
            # return to get
            return self.get(request, *args, **kwargs)

**checkout/urls.py**

.. code-block:: python

    from knpay_plugin.conf import config

    urlpatterns = [
        url(r'^choose-method/$', views.CreatePaymentView.as_view(), name='choose_method'),
        url(r'^completed/%s/$' % config.COMPLETE_VIEWS_REGEX,
            views.CompletedView.as_view(), name='complete'),
        # ...
    ]


**settings.py**

.. code-block:: python

    KNPAY_REDIRECTED_VIEW_NAME = 'checkout:complete'


**knpay_plugin/payment_method.html**

.. code-block:: html

    {% load knpay_tags %}

    <form id="payment-form" action="{% url 'checkout:choose_method' %}" method="post">
        {% csrf_token %}

        {% show_gateway_choices %}

        <button type="submit" id="submit-payment-form">Submit</button>
    </form>


**checkout/payment_details.html**

.. code-block:: html

    {% load knpay_tags %}

        <h2>{% trans 'Status' %}: {{ object.get_status_display }}</h2>
        {% prepare_payload object as payload %}
        <ul>
            {% for key, value in payload.iteritems %}
                <li>{{ key }}: {{ value }}</li>
            {% endfor %}
        </ul>


API
---

If PaymentForm and CreatePaymentMixin is a hassle for your needs, you can
use a function to create the payment url.

.. code-block:: python

    from knpay_plugin.api import create_payment_url

    result, created = create_payment_url('123.000', gateway_code='knet')
    if created:
        # result is http://knpay3.mykuwaitnet.net/gw/dispatch/2kbEIQo1Z2hDll8/
        return JsonResponse(dict(redirect_url=result), status=200)
    else:
        return JsonResponse(dict(errors=result), status=400)

    result, created = create_payment_url('123.000')
    # result is {'gateway_code': 'This field is required.'}


Still, creating direct payment urls can be controlled even more

.. code-block:: python

    result, created = create_payment_url('12',
                                         gateway_code='knet',
                                         request=None,
                                         currency_code='USD',
                                         extra={'booking_id': 'foo_bar'},
                                         language='ar',
                                         customer_email='foo@example.com',
                                         customer_address_country='QA'
                                         )



Additional information
----------------------

**Gateway choices display**

Template which resides in `knpay_plugin/gateway_choices.html` must be overriden in
your installation in order to reflect the style you need.


CONFIG
------

Prepend KNPAY_ for any variable which will be overriden.


+----------------------------+-------------------------------------------------------------+------------------------------------+
|          Variable          |                         Description                         |            Default value           |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| DEFAULT_CURRENCY           | Default currency code to be sent to KNPay when creating     | KWD                                |
|                            | the payment request. Define it if your website uses single  |                                    |
|                            | currency for checkout process.                              |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| GATEWAY_CHOICES            | List of tuples containing gateway choices. First item of    | knet / Knet                        |
|                            | the tuple must match the codes defined in KNPay and the     |                                    |
+                            + second the name to be displayed in the template.            +------------------------------------+
|                            | REQUIRED.                                                   | cybersource / Credit Card          |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| BASE_URL                   | KNPay base URL. For test, can be used the default value.    | http://knpay3.mykuwaitnet.net/     |
|                            | For production, custom url has to be provided. Make sure    |                                    |
|                            | it's ssl url.                                               |                                    |
|                            | REQUIRED.                                                   |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| ADMIN_SHOW_OPTIONAL_FIELDS | Show payment transaction customer optional fields           | False                              |
|                            | in admin interface.                                         |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| ADMIN_SHOW_EXTRA_FIELD     | Show payment transaction extra field in admin interface.    | False                              |
|                            | IE: basket_id: 34                                           |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| DISCLOSURE_VIEW_NAME       | Name of the view which shall process the silent POST        | kp_disclosure                      |
|                            | from KNPay. In 99.99% of the cases you don't need to        |                                    |
|                            | override this.                                              |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| REDIRECTED_VIEW_NAME       | Name of view where customer will be redirected after        | kp_complete                        |
|                            | payment stage completes. Can be namespace:view_name         |                                    |
|                            | or just view_name. In 99.99% of the cases needs to be       |                                    |
|                            | overriden.                                                  |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| PROTOCOL                   | Http protocol be used for URI generation if HttpRequest     | http                               |
|                            | is not passed when PaymentForm is instantiated.             |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| MANDATORY_FORM_FIELDS      | Mandatory form fields for the payment form.                 | (amount, currency_code)            |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| VISIBLE_FORM_FIELDS        | Form fields which shall be visible in the template.         | []                                 |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| RENDER_FORM                | If payment form will be rendered on the page and            | False                              |
|                            | submitted via POST. If payment values are manually          |                                    |
|                            | entered by the customer, you need this                      |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| GENERATE_ORDER_FUNC        | A unique order id has to be assigned to each request to     | knpay_plugin.forms.uuid_url64      |
|                            | KNPay. If the default format of the generated order id      |                                    |
|                            | does not match your needs, define the path to the custom    |                                    |
|                            | function which generates a order id and returns it          |                                    |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| VAR_MAPPING                | Defines how the raw parameters from PSP shall be            | result / Result                    |
+                            + displayed in the payment details page.                      +------------------------------------+
|                            |                                                             | trackid / Track ID                 |
+                            +                                                             +------------------------------------+
|                            |                                                             | postdate / Post Date               |
+                            +                                                             +------------------------------------+
|                            |                                                             | tranid / Tran ID                   |
+                            +                                                             +------------------------------------+
|                            |                                                             | paymentid / Payment ID             |
+                            +                                                             +------------------------------------+
|                            |                                                             | auth / Auth ID                     |
+                            +                                                             +------------------------------------+
|                            |                                                             | ref / Reference ID                 |
+                            +                                                             +------------------------------------+
|                            |                                                             | decision / Decision                |
+                            +                                                             +------------------------------------+
|                            |                                                             | transaction_id / Transaction ID    |
+                            +                                                             +------------------------------------+
|                            |                                                             | vpc_Message / Message              |
+                            +                                                             +------------------------------------+
|                            |                                                             | vpc_ReceiptNo / Receipt No         |
+                            +                                                             +------------------------------------+
|                            |                                                             | vpc_TransactionNo / Transaction No |
+----------------------------+-------------------------------------------------------------+------------------------------------+
| GATEWAY_NAMES              | Name of the gateways as defined inside KNPay. For sure,     | migs / MiGS                        |
+                            + you'll never need to override the keys of this dict.        +------------------------------------+
|                            | However, override the values for changing what to display   | knet / Knet                        |
+                            + in the template.                                            +------------------------------------+
|                            |                                                             | mpgs / MPGS                        |
+                            +                                                             +------------------------------------+
|                            |                                                             | paypal / PayPal                    |
+                            +                                                             +------------------------------------+
|                            |                                                             | cybersource / CyberSource          |
+----------------------------+-------------------------------------------------------------+------------------------------------+