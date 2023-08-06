========
boolrule
========

.. image:: https://img.shields.io/pypi/v/boolrule.svg
        :target: https://pypi.python.org/pypi/boolrule

.. image:: https://img.shields.io/travis/tailsdotcom/boolrule.svg
        :target: https://travis-ci.org/tailsdotcom/boolrule

.. image:: https://readthedocs.org/projects/boolrule/badge/?version=latest
        :target: https://boolrule.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tailsdotcom/boolrule/shield.svg
     :target: https://pyup.io/repos/github/tailsdotcom/boolrule/
     :alt: Updates


Simple boolean expression evaluation engine.

* Free software: MIT license
* Documentation: https://boolrule.readthedocs.io.


Features
========

Compare simple boolean statements::

 >>> rule = BoolRule('5 > 3')
 >>> rule.test()
 True
 >>> rule = BoolRule('5 < 3')
 >>> rule.test()
 False


Evaluate boolean statements against a context dict::

 >>> can_buy_beer = BoolRule('user.age_years >= 18')
 >>> can_buy_beer.test({'user':{'age_years': 12}})
 False
 >>> can_buy_beer.test({'user':{'age_years': 20}})
 True

Combine conditions with and and or operators to produce complex expressions::

 >>> is_hipster = BoolRule('address.postcode.outcode in ("E1","E2") or user.has_beard = true')
 >>> address = {
 >>>   'postcode': {
 >>>      'outcode': 'E1'
 >>>   }
 >>> }
 >>> is_hipster.test({'has_beard': False, 'address': address})
 True


Credits
=======

Made possible by the excellent pyparsing_ library.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _pyparsing: http://pyparsing.wikispaces.com/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.2.0 (2016-10-27)
------------------

* Fixed error caused by refactor from internal codebase that was preventing deep context level values from being
  referenced in a substitution value

0.1.2 (2016-09-30)
------------------

* Improved documentation


0.1.1 (2016-09-30)
------------------

* Made ``context`` optional
* Improved documentation


0.1.0 (2016-09-30)
------------------

* First release on PyPI.


