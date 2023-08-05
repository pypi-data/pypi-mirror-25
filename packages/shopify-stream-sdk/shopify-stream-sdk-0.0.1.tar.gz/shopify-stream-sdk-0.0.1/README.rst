shopify-stream-sdk
==================

This module wraps the Ayinope Shopify Monitor websockets stream.

Installation
------------

This module is available via pip:

::

    $ pip install shopify-stream-sdk

Basic Usage
-----------

.. code:: py

    from shopifystream import ShopifyStream

    shopify = ShopifyStream()
        
    domain = 'www.example.com' # Optional
    include = ['include', 'these', 'keywords'] # Optional
    exclude = ['exclude', 'some', 'others'] # Optional

    product = shopify.wait_for_product(domain=domain,
                                        include=include,
                                        exclude=exclude)
    print(product)
