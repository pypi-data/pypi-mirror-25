denv
####

usage:

.. code-block:: bash
    denv COMMAND [ARGS]


Expects a `.env` file in current directory of format:

.. code-block:: bash
    KEY=VALUE
    KEY=host=foo user=bar


Example
-------

.. code-block:: bash

    $ cat .env
    CONNECTION_STRING=host=foo user=bar password=baz

    $ denv env | grep CONNECTION_STRING
    host=foo user=bar password=baz


WHY?
====

so many dotenv repos exist out there but none of them (AFAIK) can read connection string formatted values like `connection_string=host=foo user=bar password=baz`.

So here is a very simple cli script to do just that! :-)
