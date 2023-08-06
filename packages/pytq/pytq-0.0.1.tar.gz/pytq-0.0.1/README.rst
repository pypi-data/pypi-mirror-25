.. image:: https://travis-ci.org/MacHu-GWU/pytq-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/pytq-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/pytq-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/pytq-project

.. image:: https://img.shields.io/pypi/v/pytq.svg
    :target: https://pypi.python.org/pypi/pytq

.. image:: https://img.shields.io/pypi/l/pytq.svg
    :target: https://pypi.python.org/pypi/pytq

.. image:: https://img.shields.io/pypi/pyversions/pytq.svg
    :target: https://pypi.python.org/pypi/pytq

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pytq-project


Welcome to ``pytq`` Documentation
==============================================================================

``pytq`` (Python Task Queue) is a task scheduler library.

Problem we solve:

1. You have N task to do.
2. each task has ``input_data``, and after been processed, we got ``output_data``.

``pytq`` provide these feature out-of-the-box (And it's all customizable).

1. Save output_data to data-persistence system.
2. Filter out duplicate input data.
3. Built-in Multi thread processor boost the speed.
4. Nice built-in log system.
5. And its easy to define how you gonna:
    - process your input_data
    - integrate with your data persistence system
    - filter duplicates input_data
    - retrive output_data


Example
------------------------------------------------------------------------------

Suppose you have some url to crawl, and you don't want to crawl those url you
successfully crawled, and also you want to save your crawled data in database.

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    """
    This script implement multi-thread safe, a sqlite backed task queue scheduler.
    """

    from pytq import SqliteDictScheduler


    # Define your input_data model
    class UrlRequest(object):
        def __init__(self, url, context_data=None):
            self.url = url # your have url to crawl
            self.context_data = context_data # and maybe some context data to use


    class Scheduler(SqliteDictScheduler):
        # (Required) define how you gonna process your data
        def user_process(self, input_data):
            # you need to implement get_html_from_url yourself
            html = get_html_from_url(input_data.url)

            # you need to implement parse_html yourself
            output_data = parse_html(html)
            return output_data

    s = Scheduler(user_db_path="example.sqlite")

    # let's have some urls
    input_data_queue = [
        UrlRequest(url="https://pypi.python.org/pypi/pytq"),
        UrlRequest(url="https://pypi.python.org/pypi/crawlib"),
        UrlRequest(url="https://pypi.python.org/pypi/loggerFactory"),
    ]

    # execute multi thread process
    s.do(input_data_queue, multiprocess=True)

    # print output
    for id, outpupt_data in s.items():
        ...

Customize:

.. code-block:: python

    class Scheduler(SqliteDictScheduler):
        # (Optional) define the identifier of input_data (for duplicate)
        def user_hash_input(self, input_data):
            return input_data.url

        # (Optional) define how do you save output_data to database
        # Here we just use the default one
        def user_post_process(self, task):
            self._default_post_process(task)

        # (Optional) define how do you skip crawled url
        # Here we just use the default one
        def user_is_duplicate(self, task):
            return self._default_is_duplicate(task)


TODO: more example is coming.


Quick Links
------------------------------------------------------------------------------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: http://www.wbh-doc.com.s3.amazonaws.com/pytq/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: http://www.wbh-doc.com.s3.amazonaws.com/pytq/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/pytq-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/pytq-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/pytq#downloads


.. _install:

Install
------------------------------------------------------------------------------

``pytq`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install pytq

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pytq