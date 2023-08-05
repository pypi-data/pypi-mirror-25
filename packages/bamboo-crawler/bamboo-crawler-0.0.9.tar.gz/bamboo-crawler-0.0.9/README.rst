Bamboo Crawler
==============

|CircleCI Status|

A Hobby Crawler. It is almost under construction.

Usage
=====

Installatino
------------

.. code:: console

    $ pip install bamboo-crawler

Run
---

::

    $ bamboo --recipe recipe.yml

Recipe
------

.. code:: yaml

    mytask:
      input:
        type: ConstantInputter
        options:
          value: http://httpbin.org/robots.txt
      process:
        type: HTTPCrawler
      output:
        type: StdoutOutputter

License
=======

BSD 2-clause "Simplified" License

.. |CircleCI Status| image:: https://circleci.com/gh/kitsuyui/bamboo-crawler.svg?style=shield&circle-token=:circle-token
   :target: https://circleci.com/gh/kitsuyui/bamboo-crawler
