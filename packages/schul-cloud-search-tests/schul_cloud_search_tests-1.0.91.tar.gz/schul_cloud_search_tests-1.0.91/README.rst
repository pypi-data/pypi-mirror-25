schul_cloud_search_tests
========================

.. image:: https://travis-ci.org/schul-cloud/schul_cloud_search_tests.svg?branch=master
   :target: https://travis-ci.org/schul-cloud/schul_cloud_search_tests
   :alt: Build Status

.. image:: https://badge.fury.io/py/schul-cloud-search-tests.svg
   :target: https://pypi.python.org/pypi/schul-cloud-search-tests
   :alt: Python Package Index

.. image:: https://img.shields.io/docker/build/schulcloud/schul_cloud_search_tests.svg
   :target: https://hub.docker.com/r/schulcloud/schul_cloud_search_tests/builds/
   :alt: Dockerhub Automated Build Status

.. image:: http://firsttimers.quelltext.eu/repository/schul-cloud/schul_cloud_search_tests.svg
   :target: http://firsttimers.quelltext.eu/repository/schul-cloud/schul_cloud_search_tests.html
   :alt: First Timers

These are the tests for the `Schul-Cloud search API
<https://github.com/schul-cloud/resources-api-v1/#search-api>`__.
You can read `motivation blog post`_ about

- common tests for all search engines
- testing during live deployment

Installation
------------

You can install the tests by installing Python_ version 3 and ``pip``.
Then, you run the installation from the command line:

.. code:: shell

    pip install --user schul-cloud-search-tests

Installation for Development
----------------------------

If you would like to contribute code to this repository, you can clone it first.

.. code:: shell

    git clone https://github.com/schul-cloud/schul_cloud_search_tests.git
    cd schul_cloud_search_tests

Install the required packages for Python_:

.. code:: shell

    pip3 install --user -r requirements.txt pip-tools==1.6.5

Note that if you would like to change the requirements, please edit the
``requirements.in`` file and run this command to update the dependencies:

.. code:: shell

    pip-compile --output-file requirements.txt requirements.in

Specification
-------------

The idea is that these tests run in between your search client and your
search engine or search adapter.
You use the test interface instead of your search engine interface to 
run checks on every request the client makes:

- Is the client request formulated correctly?
- Is the server response folmulated correctly?

These cases can be defined and are defined:

- When the client issues a successful request and the server responds correctly,
  the request is forwarded, optionally including a note that the tests passed.
- When the client issues a malformed request, HTTP error ``400`` is returned
  including the information which tests did not pass.
  The request is forwarded to the server and the response is expected to be ``400``, too.
- When the client issues a correct request, and the server response is malformed,
  then HTTP error ``409`` is returned including a list of error descriptions
  of the mistakes made by the server.

To make the decisions transparent, the client request and the server response are included in the error reponses.

Usage as Proxy
--------------

Suppose you have a server running on http://localhost:1234/v1/search/.
You can tun the search engine tests as a proxy on port 8080 like this:

.. code:: shell

    python3 -m schul_cloud_search_tests.proxy http://localhost:1234/v1/search 8080 /endpoint/

Now, all your requests to http://localhost:8080/endpoint/ will be forwarded to 
http://localhost:1234/v1/search.

When you are done, you can visit http://localhost:8080/stop to stop the server
or run this command:

.. code:: shell

    python3 -m schul_cloud_search_tests.stop 8080

The return code is zero (success) if all tests of all requests passed.
If one test fails, it is a number greater than zero.

Note that the defaults are as follows.
The command in each line is the same.

.. code:: shell

    python3 -m schul_cloud_search_tests.proxy http://localhost:8080/v1/search 8081 /v1/search
    python3 -m schul_cloud_search_tests.proxy http://localhost:8080/v1/search 8081
    python3 -m schul_cloud_search_tests.proxy http://localhost:8080/v1/search
    python3 -m schul_cloud_search_tests.proxy

Usage as Tests
--------------

In case you have a search engine which should be tested at the URL, you can run tests against it with the following command

.. code:: shell

    python3 -m schul_cloud_search_tests.search http://localhost:8080/v1/search \
               --query "Q=einstein" --query "Q=test&page[offset]=20"

The tests test the following:

- There is a search engine running at http://localhost:8080/v1/search
- These queries ``Q=einstein`` and ``Q=test&page[offset]=20`` are handled correctly.
- Additional tests are run wich test correct and malformed queries,
  see `Issue 6 <https://github.com/schul-cloud/schul_cloud_search_tests/issues/6>`__.

The return status of the tests is zero if all tests passed, otherwise a positive number.

Development Process
-------------------

The idea is stated in the `motivation blog post`_.
We can use the tests to test the search engines.
However, the tests can become complex and must be tested themselves.
Therefore, the following development process is proposed.

1. Have a look at the specification:

   - The `Search API`_ describes how to request a search.
   - The `Response Schema`_ describes what to expect as a response.
   - The `Error Schema`_  describes what an error should look like.
   
   The specification is the most important document.
   It determines what needs to be tested.

2. Implement tests according to examples of the specification.
   These tests are located in the `schul_cloud_search_tests/tests`_ folder.
   They test how you would like to have the search proxy respond to the
   different valid and invalid requests.

3. Make the tests run.

   - If it is a new condition under which a proxy request succeeds or fails,
     you should implement these as tests in the `schul_cloud_search_tests/search_tests`_
     folder.
     These tests are executed when a search request goes through the proxy.
   
   - If this is a communication feature of the proxy, it must be described in
     the `Specification`_ section.
     The code in the `schul_cloud_search_tests/proxy.py`_ should be touched.

Further Reading
---------------

- `Readme Driven Development`_

------------------------------

You can edit this document `on Github
<https://github.com/schul-cloud/schul_cloud_search_tests/blob/master/README.rst#readme>`__
and check it with `this editor <http://rst.ninjs.org/>`__.

.. _Readme Driven Development: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
.. _motivation blog post: https://schul-cloud.github.io/blog/2017-06-08/search-api-specification
.. _Python: https://python.org
.. _Search API: https://github.com/schul-cloud/resources-api-v1#search-api
.. _Response Schema: https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/search-response#readme
.. _Error Schema: https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/error#readme
.. _schul_cloud_search_tests/proxy.py: https://github.com/schul-cloud/schul_cloud_search_tests/tree/master/schul_cloud_search_tests/proxy.py
.. _schul_cloud_search_tests/search_tests: https://github.com/schul-cloud/schul_cloud_search_tests/tree/master/schul_cloud_search_tests/search_tests
.. _schul_cloud_search_tests/tests: https://github.com/schul-cloud/schul_cloud_search_tests/tree/master/schul_cloud_search_tests/tests
