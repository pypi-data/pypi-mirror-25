django-varlet
=============

:author: Keryn Knight
:version: 0.2.2

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-varlet.svg?branch=0.2.2
  :target: https://travis-ci.org/kezabelle/django-varlet

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-varlet.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-varlet

==============  ======
Release         Status
==============  ======
stable (0.2.2)  |travis_stable|
master          |travis_master|
==============  ======

An implementation of models, views etc. that can act as **pages**, though they
have no content fields to speak of. Bring Your Own Content.

Pages consist only of a URL and a way to render a template at that URL. The
default model implementation uses `django-templateselector`_ to provide template
selection from HTML files within ``<templatedir>/varlet/pages/layouts``

The application uses `swapper`_ to theoretically allow for using a different
model.

If the application is mounted at the project root ``/``, Pages may not have
URLs which collide with those of another application in the urlconf.

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
.. _django-templateselector: https://github.com/kezabelle/django-template-selector
.. _swapper: https://github.com/wq/django-swappable-models


----

Copyright (c) 2017, Keryn Knight
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

Change history for django-varlet
-------------------------------------------------------------

0.2.2
^^^^^^
* Fixed tests which broke via continuous integration, but didn't with my local
  requirements, because I'd introduced further validation in ``django-templateselector``

0.2.1
^^^^^^
* Added typeahead/autocomplete to the URL field for a page.

0.2.0
^^^^^^
* Initial release


