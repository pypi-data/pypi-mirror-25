==============
django-paypal2
==============

提供paypal支付相关的view和方法

Quick start
-----------
1. Install::

    pip install django_paypal2


2. Add "paypal" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'paypal',
    ]

3. Add paypal config to settings.py::

    PAYPAL = {
        "SERVER_URL": "http://localhost:8000", # current site host and port
        "sandbox": False,  # True or False
        "client_id": "xxx",
        "client_secret": "", # you can get id and secret from paypal
    }

4. Include the polls URLconf in your project urls.py like this::

    url(r'^paypal/', include('paypal.urls')),

5. Migrate db


6. Create transaction and redirect to paypal ::

    from paypal.models import PaypalTransaction

    tx = PaypalTransaction(description="sample pay")
    tx.add_item("sample", 'USD', float(amount))
    tx.reference_id = "your reference id"
    tx.save()
    return redirect('paypal_redirect', uid=tx.uid)

