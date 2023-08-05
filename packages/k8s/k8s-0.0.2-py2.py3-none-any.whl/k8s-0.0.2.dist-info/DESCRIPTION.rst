k8s - Python client library for the Kubernetes API
--------------------------------------------------

|Build Status| |Codacy Quality Badge| |Codacy Coverage Badge|


.. |Build Status| image:: https://semaphoreci.com/api/v1/fiaas/k8s/branches/master/badge.svg
    :target: https://semaphoreci.com/fiaas/k8s
.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&utm_medium=referral&utm_content=fiaas/k8s&utm_campaign=badger
.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/cb51fc9f95464f22b6084379e88fad77
    :target: https://www.codacy.com/app/mortenlj/k8s?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fiaas/k8s&amp;utm_campaign=Badge_Coverage


Changes since last version
--------------------------

* `67ffd8c`_: DOCD-1186 - Make PyPI release work
* `1a94aba`_: DOCD-1186 - Fixes for github release
* `875ce3f`_: DOCD-1186 - setuptools_scm works in py3, setuptools_git doesn't (`#11`_)
* `d58f5c1`_: Use Apache 2.0 license
* `52d6283`_: Deploy fixes (`#9`_)
* `228d0b0`_: Add example of `get_or_create` usage
* `5a5438d`_: Release scripts (`#7`_)
* `a3eb0c6`_: Add  tutorial
* `fbfe10d`_: Appease codacy
* `ed25823`_: Make maxUnavailable and maxSurge default int with alt_type text
* `f4a72a5`_: Add sphinx auto-generated setup
* `0ea5b47`_: Rewrite test_ingress to not use vcr (`#1`_)
* `8730fda`_: Move specification of codacy dependency to setup.py (`#5`_)
* `dadbce7`_: Minor tweaks to LICENSE to trigger license detection
* `6044e45`_: Add another codacy badge
* `8a29ddb`_: Add Codacy badge
* `4d28c95`_: Prepare to generate/upload coverage as separate job in CI
* `687d92a`_: Replace flake8 with similary configured prospector
* `0cda192`_: Fix support for Python3
* `bf9c968`_: Use tox
* `389dd0d`_: Add build-status badge
* `598336d`_: Add BSD license
* `dc273c0`_: Remove unused fixture
* `8fff9c3`_: Add .gitignore
* `5d3f60a`_: Add setup.py
* `50e40b4`_: Disable debug logging for streaming http requests
* `c1556e2`_: Fix tests after adding tls field to Ingress model
* `ba5a22e`_: Backport k8s client library changes from spinnaker-k8s-helper
* `699be94`_: Generate XML coverage report for Quality Gate
* `c58ca62`_: k8s: allow extra arguement to client.delete function
* `5c68898`_: Give more detailed error messages when k8s responds with an error (`#26`_)
* `b18fdf8`_: DOCD-977 - Report status to a TPR object
* `6053a61`_: DOCD-977 - Add a deployment_id field to app_spec
* `812a7ac`_: Disable SSL-warnings when running with `verify_ssl=False`
* `f98ad11`_: Using closer name to k8s API for Version
* `bad9b2e`_: Version has only the 'name' field
* `7567da2`_: INFRA-1536: Default to keeping 5 replicasets for a deployment instead of all of them. (`#5`_)
* `15e3c99`_: Create TPR when watching it and not present in cluster yet
* `cae83c8`_: DOCD-936 Codestyle
* `d5af29d`_: DOCD-936 Add watch_list on the base k8s client
* `18196b3`_: DOCD-936 Add list operation to get all resources of a given type in a namespace
* `2f6ffc6`_: Bumporama (`#83`_)
* `69da094`_: added horizontalpodautoscaler, default off
* `2545b10`_: INFRA-1282 - Set service type from cluster configuration (`#70`_)
* `47748b3`_: Add support for ConfigMaps in fiaas.yml (`#66`_)
* `d37ac8a`_: INFRA-1217 - Keep nodePort when updating a service (`#61`_)
* `dfb9330`_: INFRA-1086 - Wait for updated replicas before sending success event (`#38`_)
* `71e2ca0`_: INFRA-1009 - Refactoring
* `cb14d2b`_: INFRA-1009 - Delete ingress if app no longer wants it
* `601baa0`_: INFRA-1009 - Fix e2e test for ingress
* `474b089`_: INFRA-1009 - Support exec probes
* `c90f663`_: INFRA-1009 - Implement new model in deployer
* `230df78`_: INFRA-1009 Add ExecAction
* `e74577e`_: INFRA-1009 Add fields to Probe
* `8e87f96`_: INFRA-1009 Add httpHeaders field to HTTPGetAction
* `e05b578`_: INFRA-947 - Test SpecFactory dispatching
* `302e4b7`_: INFRA-947 - Parse v1 fiaas.yml to new model
* `f9eb4b8`_: INFRA-947 - End-to-end test using minikube if installed
* `6a9096a`_: Drop pytest-xdist because of this: https://github.com/pytest-dev/pytest-xdist/issues/41
* `01561fd`_: INFRA-947 - Run tests in parallel, and make newer versions of flake8 work
* `9bc0d55`_: INFRA-923: re-add mistakenly deleted test_ingress vcr
* `9e2e0f7`_: fix tests after rebase
* `9ed67f6`_: fix another rebase-error
* `a71d729`_: INFRA-923: refactor services to use pytest and mock.
* `e56b57e`_: INFRA-923: Capitalize constants, parametarize lb-test
* `f4f09ab`_: INFRA-923: add support for loadbalancer whitelist-flag in GKE.
* `b027a84`_: INFRA-923: refactor services to use pytest and mock.
* `64f947a`_: INFRA-964 - Fail early if name not given when creating ObjectMeta
* `3d53424`_: INFRA-964 - Set name and namespace in metadata, remove from top-level of objects
* `891555b`_: INFRA-923 Add creation of static ip, dns entry for load balancer
* `dff989b`_: Prepere to merge repository.

.. _0cda192: https://github.com/fiaas/k8s/commit/0cda192
.. _601baa0: https://github.com/fiaas/k8s/commit/601baa0
.. _3d53424: https://github.com/fiaas/k8s/commit/3d53424
.. _7567da2: https://github.com/fiaas/k8s/commit/7567da2
.. _6044e45: https://github.com/fiaas/k8s/commit/6044e45
.. _474b089: https://github.com/fiaas/k8s/commit/474b089
.. _5c68898: https://github.com/fiaas/k8s/commit/5c68898
.. _ba5a22e: https://github.com/fiaas/k8s/commit/ba5a22e
.. _#61: https://github.com/fiaas/k8s/issues/61
.. _#9: https://github.com/fiaas/k8s/issues/9
.. _b18fdf8: https://github.com/fiaas/k8s/commit/b18fdf8
.. _dc273c0: https://github.com/fiaas/k8s/commit/dc273c0
.. _9ed67f6: https://github.com/fiaas/k8s/commit/9ed67f6
.. _8e87f96: https://github.com/fiaas/k8s/commit/8e87f96
.. _1a94aba: https://github.com/fiaas/k8s/commit/1a94aba
.. _fbfe10d: https://github.com/fiaas/k8s/commit/fbfe10d
.. _#66: https://github.com/fiaas/k8s/issues/66
.. _#5: https://github.com/fiaas/k8s/issues/5
.. _dff989b: https://github.com/fiaas/k8s/commit/dff989b
.. _18196b3: https://github.com/fiaas/k8s/commit/18196b3
.. _f4a72a5: https://github.com/fiaas/k8s/commit/f4a72a5
.. _ed25823: https://github.com/fiaas/k8s/commit/ed25823
.. _c90f663: https://github.com/fiaas/k8s/commit/c90f663
.. _6a9096a: https://github.com/fiaas/k8s/commit/6a9096a
.. _891555b: https://github.com/fiaas/k8s/commit/891555b
.. _f98ad11: https://github.com/fiaas/k8s/commit/f98ad11
.. _5d3f60a: https://github.com/fiaas/k8s/commit/5d3f60a
.. _302e4b7: https://github.com/fiaas/k8s/commit/302e4b7
.. _e05b578: https://github.com/fiaas/k8s/commit/e05b578
.. _f4f09ab: https://github.com/fiaas/k8s/commit/f4f09ab
.. _#70: https://github.com/fiaas/k8s/issues/70
.. _15e3c99: https://github.com/fiaas/k8s/commit/15e3c99
.. _bad9b2e: https://github.com/fiaas/k8s/commit/bad9b2e
.. _f9eb4b8: https://github.com/fiaas/k8s/commit/f9eb4b8
.. _d58f5c1: https://github.com/fiaas/k8s/commit/d58f5c1
.. _699be94: https://github.com/fiaas/k8s/commit/699be94
.. _a71d729: https://github.com/fiaas/k8s/commit/a71d729
.. _8fff9c3: https://github.com/fiaas/k8s/commit/8fff9c3
.. _50e40b4: https://github.com/fiaas/k8s/commit/50e40b4
.. _875ce3f: https://github.com/fiaas/k8s/commit/875ce3f
.. _47748b3: https://github.com/fiaas/k8s/commit/47748b3
.. _5a5438d: https://github.com/fiaas/k8s/commit/5a5438d
.. _cae83c8: https://github.com/fiaas/k8s/commit/cae83c8
.. _#11: https://github.com/fiaas/k8s/issues/11
.. _0ea5b47: https://github.com/fiaas/k8s/commit/0ea5b47
.. _e56b57e: https://github.com/fiaas/k8s/commit/e56b57e
.. _b027a84: https://github.com/fiaas/k8s/commit/b027a84
.. _8730fda: https://github.com/fiaas/k8s/commit/8730fda
.. _#38: https://github.com/fiaas/k8s/issues/38
.. _#26: https://github.com/fiaas/k8s/issues/26
.. _8a29ddb: https://github.com/fiaas/k8s/commit/8a29ddb
.. _c58ca62: https://github.com/fiaas/k8s/commit/c58ca62
.. _a3eb0c6: https://github.com/fiaas/k8s/commit/a3eb0c6
.. _#83: https://github.com/fiaas/k8s/issues/83
.. _cb14d2b: https://github.com/fiaas/k8s/commit/cb14d2b
.. _9e2e0f7: https://github.com/fiaas/k8s/commit/9e2e0f7
.. _228d0b0: https://github.com/fiaas/k8s/commit/228d0b0
.. _dfb9330: https://github.com/fiaas/k8s/commit/dfb9330
.. _#1: https://github.com/fiaas/k8s/issues/1
.. _d37ac8a: https://github.com/fiaas/k8s/commit/d37ac8a
.. _2f6ffc6: https://github.com/fiaas/k8s/commit/2f6ffc6
.. _bf9c968: https://github.com/fiaas/k8s/commit/bf9c968
.. _e74577e: https://github.com/fiaas/k8s/commit/e74577e
.. _52d6283: https://github.com/fiaas/k8s/commit/52d6283
.. _2545b10: https://github.com/fiaas/k8s/commit/2545b10
.. _9bc0d55: https://github.com/fiaas/k8s/commit/9bc0d55
.. _687d92a: https://github.com/fiaas/k8s/commit/687d92a
.. _64f947a: https://github.com/fiaas/k8s/commit/64f947a
.. _230df78: https://github.com/fiaas/k8s/commit/230df78
.. _389dd0d: https://github.com/fiaas/k8s/commit/389dd0d
.. _dadbce7: https://github.com/fiaas/k8s/commit/dadbce7
.. _67ffd8c: https://github.com/fiaas/k8s/commit/67ffd8c
.. _69da094: https://github.com/fiaas/k8s/commit/69da094
.. _812a7ac: https://github.com/fiaas/k8s/commit/812a7ac
.. _d5af29d: https://github.com/fiaas/k8s/commit/d5af29d
.. _6053a61: https://github.com/fiaas/k8s/commit/6053a61
.. _01561fd: https://github.com/fiaas/k8s/commit/01561fd
.. _4d28c95: https://github.com/fiaas/k8s/commit/4d28c95
.. _c1556e2: https://github.com/fiaas/k8s/commit/c1556e2
.. _71e2ca0: https://github.com/fiaas/k8s/commit/71e2ca0
.. _598336d: https://github.com/fiaas/k8s/commit/598336d
.. _#7: https://github.com/fiaas/k8s/issues/7

