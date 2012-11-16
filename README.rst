python-bluefin 1.4
==================

python-bluefin is a Python API client for the Bluefin_ Payment System API.
The only thing this client module does is serialize and pass the data on to
the Bluefin API gateway, it performs little to no validation. Values are passed
into an API function in dict form, and responses come back in a similar
dict format.

.. note:: python-bluefin is not at all endorsed by Bluefin Payment Systems in
    any way. We have published this API module with the hope that it will be
    useful to someone else.

.. _Bluefin: http://www.bluefin.com/

Status
------

python-bluefin has been in use in production for about a year with a high
transaction volume. The directmode client in particular has seen lots of use.

That said, we only use a little sliver of what Bluefin supports (one-off
credit card charges, namely). Given that python-bluefin is a very light
wrapper, other usage cases should still work just fine, even if we (the
maintainers) haven't used them yet.

Installing
----------

To install::

    pip install --upgrade bluefin

A quick example
---------------

Here's a very bare-bones example of how to use the Direct Mode V3Client. We
pass in the required key/values via a Python dict, and get a dict result. All
of these values are documented in the Bluefin API documentation, so look there
for help on just what is being passed in and coming back.

    >>> from bluefin.directmode.clients import V3Client
    >>> api = V3Client()
    >>> result = api.send_request({
        'pay_type': 'C',
        'tran_type': 'A',
        'account_id': 123456789012,
        'amount': 1.0,
        'card_number': 4444333322221111,
        'card_expire': '1212',
        'dynip_sec_code': 'SECURITY_CODE_HERE',
    })
    >>> print result
    {
        'avs_code': 'X', 'auth_msg': 'TEST APPROVED',
        'status_code': 'T', 'ticket_code': 'XXXXXXXXXXXXXXX',
        'auth_date': '2011-06-22 19:04:30', 'settle_currency': 'USD',
        'auth_code': '999999', 'settle_amount': '1', 'cvv2_code': 'M',
        'processor': 'TEST', 'trans_id': '123456789012'
    }


Running Unit Tests
------------------

* Install nose.
* Copy ``tests/api_details.blank.py`` to ``tests/api_details.py``
* Edit ``test/api_details.py`` to reflect your account number and security code.
* From within the ``python-bluefin`` dir, run ``nosetests``
  
License
-------

python-bluefin is licensed under the `BSD License`_.

.. _BSD License: https://github.com/duointeractive/python-bluefin/blob/master/LICENSE
