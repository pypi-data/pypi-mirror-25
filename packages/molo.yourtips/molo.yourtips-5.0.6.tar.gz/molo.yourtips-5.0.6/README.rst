molo.yourtips
#############
.. image:: https://travis-ci.org/praekeltfoundation/molo.yourtips.svg
    :target: https://travis-ci.org/praekeltfoundation/molo.yourtips
.. image:: https://img.shields.io/pypi/v/molo.yourtips.svg
    :target: https://pypi.python.org/pypi/molo.yourtips
.. image:: https://coveralls.io/repos/github/praekeltfoundation/molo.yourtips/badge.svg
    :target: https://coveralls.io/github/praekeltfoundation/molo.yourtips

**This feature enables youth to share short tips with one another.**

.. contents:: Table of Contents
   :depth: 1

Requirements
============

#. django >= 1.8

#. molo.core >= 5.5.0

#. django-secretballot >= 0.7.0

#. django-likes >= 1.11

Prerequisite
============
#. Install or add ``django-likes`` to your Python path.

#. Configure ``django-secretballot`` as described `here <http://pypi.python.org/pypi/django-secretballot/>`_.

#. Add ``likes`` to your ``INSTALLED_APPS`` setting.

#. Add likes url include to your project's ``urls.py`` file::

    url(r'^likes/',
        include('likes.urls',
                namespace='likes',
                app_name='likes')),

#. Add ``likes.middleware.SecretBallotUserIpUseragentMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting, i.e.::

    MIDDLEWARE_CLASSES = (
        ...other middleware classes...
        "likes.middleware.SecretBallotUserIpUseragentMiddleware",
    )

#. Add ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS`` setting, i.e.::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...other context processors...
        "django.core.context_processors.request",
    )

Installation
============

#. pip install molo.yourtips

#. Add ``molo.yourtips`` to your ``INSTALLED_APPS`` settings.

#. Add yourtips url include to your project's ``urls.py`` file::

    url(r'^yourtips/', include('molo.yourtips.urls',
                               namespace='molo.yourtips')),

#. Create and publish a YourTips page on the CMS. By adding the YourTips page the

Feature List
============

#. This feature enables youth to share short (twitter length - 140 characters) tips on the platform with one another.
#. User submitted tips are curated by content managers and published on the platform.
#. Users can interact with published tips by liking each others tips or sharing (requires consent from author) on facebook or twitter.

YourTips Settings
=================

Homepage Banner Copy
--------------------

#. By default the homepage banner copy is ``Do you have advice you can share with other youth on relationships?``.
#. The homepage banner copy by adding the copy the yourtips settings.

