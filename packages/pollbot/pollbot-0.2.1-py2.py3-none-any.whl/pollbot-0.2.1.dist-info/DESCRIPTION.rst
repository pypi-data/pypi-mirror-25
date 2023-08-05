PollBot
=======

|coc| |travis| |master-coverage|

.. |coc| image:: https://img.shields.io/badge/%E2%9D%A4-code%20of%20conduct-blue.svg
    :target: https://github.com/mozilla/PollBot/blob/master/CODE_OF_CONDUCT.md
    :alt: Code of conduct

.. |travis| image:: https://travis-ci.org/mozilla/PollBot.svg?branch=master
    :target: https://travis-ci.org/mozilla/PollBot

.. |master-coverage| image::
    https://coveralls.io/repos/mozilla/PollBot/badge.svg?branch=master
    :alt: Coverage
    :target: https://coveralls.io/r/mozilla/PollBot

.. |readthedocs| image:: https://readthedocs.org/projects/pollbot/badge/?version=latest
    :target: https://pollbot.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |pypi| image:: https://img.shields.io/pypi/v/pollbot.svg
    :target: https://pypi.python.org/pypi/pollbot

PollBot is an hardworking little robot (microservice) that frees its
human masters from the toilsome task of polling for the state of
things during the Firefox release process.


`Version 1.0 <https://github.com/mozilla/PollBot/projects/1>`_ will
provide, at a minimum, these API resources:

#. build exists on archive.mozilla.org
#. release notes published
#. product-details.mozilla.org JSON contains the release
#. download links are on mozilla.org and they work
#. security advisories are published and links work 

License
-------

MPL v2 (see `LICENSE <https://github.com/mozilla/PollBot/blob/master/LICENSE>`_)


Configuration
-------------

PollBot is a currently a stateless service, which means there are no
database services to configure.

However you can configure the following parameters using environment variables:

+-------------------+--------------------------------------------------+
| **VARIABLE**      | **Description**                                  |
+-------------------+--------------------------------------------------+
| ``PORT``          | The service PORT, by default runs on 9876        |
+-------------------+--------------------------------------------------+
| ``VERSION_FILE``  | The JSON version file, default PWD/version.json  |
+-------------------+--------------------------------------------------+
| ``CACHE_MAX_AGE`` | The Cache-Control max-age value, default to 30   |
|                   | seconds. Set it to 0 to set it to no-cache       |
+-------------------+--------------------------------------------------+


CHANGELOG
=========

0.2.1 (2017-09-06)
------------------

- Fixes archive-l10n checks for nightly with new MAR files.


0.2.0 (2017-09-01)
------------------

- Add a /v1/{product} endpoint (#47)
- Add a /v1/{product}/ongoing-versions endpoint (#52)
- Add a /v1/{product}/{version} that lists all checks (#62)
- Add a nightly specific task and endpoint for latest-date publication (#68)
- Add a nightly specific task and endpoint for latest-date-l10n publication (#68)
- Add more context about what the task have been checking (#58)
- Fix the ESR download links task url (#66)
- Add a task to validate if devedition and beta version matches (#78)
- Redirects URL ending by a / to URL without the / in case of 404. (#54)
- Add Cache-Control headers (#43)
- Handle aiohttp.ClientError as tasks errors (#76)
- Handle Archive CDN errors (#75)


0.1.0 (2017-08-08)
------------------

- Add the /v1/ info page (#10)
- Add the archive.mozilla.org bot (#17)
- Add the bedrock release-notes bot (#16)
- Add the bedrock security-advisories bot (#26)
- Add the bedrock download-page bot (#28)
- Add the product-details bot (#27)
- Expose the Open API Specification (#23)
- Add the contribute.json endpoint (#25)
- Add CORS support (#28)
- Add the /__version__ endpoint (39)
- Add the __heartbeat__ and __lbheartbeat__ endpoints (#38)
- Serve the Swagger documentation (#30)


Contributors
============

* Ethan Glasser-Camp <ethan@betacantrips.com>
* Mathieu Agopian <mathieu@agopian.info>
* Mathieu Leplatre <mathieu@mozilla.com>
* Rémy Hubscher <rhubscher@mozilla.com>


