======
Htttea
======

.. image:: https://travis-ci.org/narusemotoki/htttea.svg?branch=master
    :target: https://travis-ci.org/narusemotoki/htttea

I’m **not** a tea pot. Provide a web server for testing.

`CHANGELOG <https://github.com/narusemotoki/htttes/blob/master/CHANGELOG.rst>`_


Usage
=====

.. code-block:: python

   response_body = b"Hello World"
   with htttea.Htttea() as t3:
       t3.response = htttea.Response(body=response_body)
       response = requests.post(t3.url, data=data)

       assert t3.request.data == data
       assert response.text == response_body.decode()

Htttea makes a real web server when it is called with :code:`with` statement. You can get a web server URL from :code:`url` property.
