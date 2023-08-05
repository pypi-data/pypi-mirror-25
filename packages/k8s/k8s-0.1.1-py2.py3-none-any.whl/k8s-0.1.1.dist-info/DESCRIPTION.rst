k8s - Python client library for the Kubernetes API
--------------------------------------------------

|Build Status| |Codacy Quality Badge| |Codacy Coverage Badge|

.. |Build Status| image:: https://semaphoreci.com/api/v1/fiaas/k8s/branches/master/badge.svg
    :target: https://semaphoreci.com/fiaas/k8s
.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&utm_medium=referral&utm_content=fiaas/k8s&utm_campaign=badger
.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fiaas/k8s&amp;utm_campaign=Badge_Coverage

Documentation
    https://k8s.readthedocs.io
Code
    https://github.com/fiaas/k8s

k8s is a python client library for Kubernetes developed as part of the FiaaS project at FINN.no, Norway's leading classifieds site. The library tries to provide an intuitive developer experience, rather than modelling the REST API directly. Our approach does not allow us to use Swagger to auto-generate a library that covers the entire API, but the parts we have implemented are (in our opinion) easier to work with than the client you get when using Swagger.

Check out the tutorial_ to find out how to use the library, or the `developer guide`_ to learn how to extend the library to cover parts of the API we haven't gotten around to yet.

.. _tutorial: http://k8s.readthedocs.io/en/latest/tutorial.html
.. _developer guide: http://k8s.readthedocs.io/en/latest/developer.html


Changes since last version
--------------------------

* `60e302d`_: DOCD-1185 - Write a tiny bit in the README. (`#17`_)
* `4235c30`_: DOCD-1185 - Write first draft of developer documentation (`#16`_)
* `ed3bd10`_: Fix test name
* `b5b5e9f`_: Fix whitespace
* `271dca1`_: Add test for configmap
* `52fa5b3`_: Move common fixtures to conftest.py
* `ae549c9`_: Add ConfigMap model
* `0990294`_: Move docs dependencies to setup.py (`#14`_)
* `4c54415`_: DOCD-1186 - Add/update some metadata (`#13`_)
* `e319705`_: DOCD-1186 - Make get_github_release work in py3

.. _#13: https://github.com/fiaas/k8s/issues/13
.. _52fa5b3: https://github.com/fiaas/k8s/commit/52fa5b3
.. _60e302d: https://github.com/fiaas/k8s/commit/60e302d
.. _#17: https://github.com/fiaas/k8s/issues/17
.. _#14: https://github.com/fiaas/k8s/issues/14
.. _4235c30: https://github.com/fiaas/k8s/commit/4235c30
.. _ed3bd10: https://github.com/fiaas/k8s/commit/ed3bd10
.. _b5b5e9f: https://github.com/fiaas/k8s/commit/b5b5e9f
.. _#16: https://github.com/fiaas/k8s/issues/16
.. _e319705: https://github.com/fiaas/k8s/commit/e319705
.. _4c54415: https://github.com/fiaas/k8s/commit/4c54415
.. _271dca1: https://github.com/fiaas/k8s/commit/271dca1
.. _0990294: https://github.com/fiaas/k8s/commit/0990294
.. _ae549c9: https://github.com/fiaas/k8s/commit/ae549c9

