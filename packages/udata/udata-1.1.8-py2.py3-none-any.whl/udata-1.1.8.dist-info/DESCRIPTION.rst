uData
=====





.. image:: https://readthedocs.org/projects/udata/badge/?version=v1.1.8
    :target: https://udata.readthedocs.io/en/v1.1.8/
    :alt: Read the documentation

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/opendatateam/udata
    :alt: Join the chat at https://gitter.im/opendatateam/udata


Customizable and skinnable social platform dedicated to (open)data.

The `full documentation <https://udata.readthedocs.io/en/v1.1.8/>`_ is hosted on Read the Docs.

.. _circleci-url: https://circleci.com/gh/opendatateam/udata
.. _circleci-badge: https://circleci.com/gh/opendatateam/udata.svg?style=shield
.. _requires-io-url: https://requires.io/github/opendatateam/udata/requirements/?branch=dev
.. _requires-io-badge: https://requires.io/github/opendatateam/udata/requirements.svg?branch=dev
.. _david-dm-url: https://david-dm.org/opendatateam/udata
.. _david-dm-badge: https://img.shields.io/david/opendatateam/udata/status.svg
.. _david-dm-dev-url: https://david-dm.org/opendatateam/udata#type=dev
.. _david-dm-dev-badge: https://david-dm.org/opendatateam/udata/dev-status.svg
.. _gitter-badge: https://badges.gitter.im/Join%20Chat.svg
.. _gitter-url: https://gitter.im/opendatateam/udata
.. _readthedocs-badge: https://readthedocs.org/projects/udata/badge/?version=v1.1.8
.. _readthedocs-url: https://udata.readthedocs.io/en/v1.1.8/

Changelog
=========

1.1.8 (2017-09-28)
------------------

- Display membership modal actions buttons for site administrators and on membership display. `#1176 <https://github.com/opendatateam/udata/pull/1176>`__
- Fix organization avatar in admin profile `#1175 <https://github.com/opendatateam/udata/issues/1175>`__

1.1.7 (2017-09-25)
------------------

- Prevent a random territory from being displayed when query doesn't match `#1124 <https://github.com/opendatateam/udata/pull/1124>`__
- Display avatar when the community resource owner is an organization `#1125 <https://github.com/opendatateam/udata/pull/1125>`__
- Refactor the "publish as" screen to make it more obvious that an user is publishing under its own name `#1122 <https://github.com/opendatateam/udata/pull/1122>`__
- Make the "find your organization" screen cards clickable (send to the organization page) `#1129 <https://github.com/opendatateam/udata/pull/1129>`__
- Fix "Center the full picture" on user avatar upload `#1130 <https://github.com/opendatateam/udata/issues/1130>`__
- Hide issue modal forbidden actions `#1128 <https://github.com/opendatateam/udata/pull/1128>`__
- Ensure spatial coverage zones are resolved when submitted from the API or when querying oembed API. `#1140 <https://github.com/opendatateam/udata/pull/1140>`__
- Prevent user metrics computation when the object owner is an organization (and vice versa) `#1152 <https://github.com/opendatateam/udata/pull/1152>`__

1.1.6 (2017-09-11)
------------------

- Fix CircleCI automated publication on release tags
  `#1120 <https://github.com/opendatateam/udata/pull/1120>`__

1.1.5 (2017-09-11)
------------------

- Fix the organization members grid in admin
  `#934 <https://github.com/opendatateam/udata/issues/934>`__
- Fix and tune harvest admin loading state and payload size
  `#1113 <https://github.com/opendatateam/udata/issues/1113>`__
- Automatically schedule validated harvesters and allow to (re)schedule them
  `#1114 <https://github.com/opendatateam/udata/pull/1114>`__
- Raise the minimum `raven` version to ensure sentry is filtering legit HTTP exceptions
  `#774 <https://github.com/opendatateam/udata/issues/774>`__
- Pin GeoJSON version to avoid breaking changes
  `#1118 <https://github.com/opendatateam/udata/pull/1118>`__
- Deduplicate organization members
  `#1111 <https://github.com/opendatateam/udata/issues/1111>`__

1.1.4 (2017-09-05)
------------------

- Fix packaging

1.1.3 (2017-09-05)
------------------

- Make the spatial search levels exclusion list configurable through `SPATIAL_SEARCH_EXCLUDE_LEVELS`.
  `#1101 <https://github.com/opendatateam/udata/pull/1101>`__
- Fix facets labelizer with html handling
  `#1102 <https://github.com/opendatateam/udata/issues/1102>`__
- Ensure territories pages have image defined in metadatas
  `#1103 <https://github.com/opendatateam/udata/issues/1103>`__
- Strip tags in autocomplete results
  `#1104 <https://github.com/opendatateam/udata/pull/1104>`__
- Transmit link checker status to frontend
  `#1048 <https://github.com/opendatateam/udata/issues/1048>`__
- Remove plus signs from search query
  `#1048 <https://github.com/opendatateam/udata/issues/987>`__

1.1.2 (2017-09-04)
------------------

- Handle territory URLs generation without validity
  `#1068 <https://github.com/opendatateam/udata/issues/1068>`__
- Added a contact button to trigger discussions
  `#1076 <https://github.com/opendatateam/udata/pull/1076>`__
- Improve harvest error handling
  `#1078 <https://github.com/opendatateam/udata/pull/1078>`__
- Improve elasticsearch configurability
  `#1096 <https://github.com/opendatateam/udata/pull/1096>`__
- Lots of fixes admin files upload
  `1094 <https://github.com/opendatateam/udata/pull/1094>`__
- Prevent the "Bad request error" happening on search but only on some servers
  `#1097 <https://github.com/opendatateam/udata/pull/1097>`__
- Migrate spatial granularities to new identifiers
- Migrate remaining legacy spatial identifiers
  `#1080 <https://github.com/opendatateam/udata/pull/1080>`__
- Fix the discussion API documention
  `#1093 <https://github.com/opendatateam/udata/pull/1093>`__

1.1.1 (2017-07-31)
------------------

- Fix an issue preventing reuse edition:
  `#1027 <https://github.com/opendatateam/udata/issues/1027>`__
- Fix an issue preventing user display and edit in admin:
  `#1030 <https://github.com/opendatateam/udata/issues/1030>`__
- Fix an error when a membership request is accepted:
  `#1028 <https://github.com/opendatateam/udata/issues/1028>`__
- Fix issue modal on a reuse:
  `#1026 <https://github.com/opendatateam/udata/issues/1026>`__
- Fix sort by date on admin users list:
  `#1029 <https://github.com/opendatateam/udata/issues/1029>`__
- Improve the `purge` command
  `#1039 <https://github.com/opendatateam/udata/pull/1039>`__
- Ensure search does not fail when a deleted object has not been
  unindexed yet
  `#1063 <https://github.com/opendatateam/udata/issues/1063>`__
- Start using Celery queues to handle task priorities
  `#1067 <https://github.com/opendatateam/udata/pull/1067>`__
- Updated translations

1.1.0 (2017-07-05)
------------------

New features and improvements
*****************************

- Added a `DCAT <https://www.w3.org/TR/vocab-dcat/>`__ harvester
  and expose metadata as RDF/DCAT.
  `#966 <https://github.com/opendatateam/udata/pull/966>`__
  See the dedicated documentions:

  - `RDF <https://udata.readthedocs.io/en/stable/rdf/>`__
  - `Harvesting <https://udata.readthedocs.io/en/stable/harvesting/>`__

- Images are now optimized and you can force rerendering using the `udata images render` command.
- Allowed files extensions are now configurable via the `ALLOWED_RESOURCES_EXTENSIONS` setting
  and both admin and API will have the same behavior
  `#833 <https://github.com/opendatateam/udata/pull/833>`__.
- Improve and fix notifications:
  `#928 <https://github.com/opendatateam/udata/issues/928>`__

  - Changed notification style to toast
  - Fix notifications that weren't displayed on form submission
- Add a toggle indicator on dataset quality blocks that are collapsible
  `#915 <https://github.com/opendatateam/udata/issues/915>`__
- Integrating latest versions of GeoZones and GeoLogos for territories.
  Especially using history of towns, counties and regions from GeoHisto.
  `#499 <https://github.com/opendatateam/udata/issues/499>`__

Breaking Changes
****************

- Themes are now entrypoint-based `#829 <https://github.com/opendatateam/udata/pull/829>`__.
  There is also a new `theming documention <https://udata.readthedocs.io/en/stable/creating-theme/>`__.
- Images placeholders are now entirely provided by themes
  `#707 <https://github.com/opendatateam/udata/issues/707>`__
  `#1006 <https://github.com/opendatateam/udata/issues/1006>`__
- Harvester declaration is now entrypoint-based
  `#1004 <https://github.com/opendatateam/udata/pull/1004>`__

Fixes
*****

- Ensure URLs are stripped `#823 <https://github.com/opendatateam/udata/pull/823>`__
- Lot of fixes and improvements on Harvest admin UI
  `#817 <https://github.com/opendatateam/udata/pull/817>`__:

  - harvester edition fixed (and missing API added)
  - harvester deletion fixed
  - harvester listing is now paginated
  - more detailed harvesters widgets
  - ensure harvest source are owned by a user or an organization, not both [migration]

- Pure Vue.js search facets
  `#880 <https://github.com/opendatateam/udata/pull/880>`__.
  Improve and fix the datepicker:

  - Proper sizing and positionning in dropdowns
  - Fix initial value not being displayed
  - Make it usable on keyboard
  - Allows to define `min` and `max` values to disable some dates
  - Keyboard input is reflected into the calendar
    `#615 <https://github.com/opendatateam/udata/issues/615>`__
- Disable `next` button when no file has been uploaded
  `#930 <https://github.com/opendatateam/udata/issues/930>`__
- Fix badges notification mails
  `#894 <https://github.com/opendatateam/udata/issues/894>`__
- Fix the `udata search reindex` command
  `#1009 <https://github.com/opendatateam/udata/issues/1009>`__
- Reindex datasets when their parent organization is purged
  `#1008 <https://github.com/opendatateam/udata/issues/1008>`__

Miscellaneous / Internal
************************

- Upgrade to Flask-Mongoengine 0.9.3, Flask-WTF 0.14.2, mongoengine 0.13.0.
  `#812 <https://github.com/opendatateam/udata/pull/812>`__
  `#871 <https://github.com/opendatateam/udata/pull/871>`__
  `#903 <https://github.com/opendatateam/udata/pull/903>`__
- Upgrade to Flask-Login 0.4.0 and switch from Flask-Security to the latest
  `Flask-Security-Fork <https://pypi.python.org/pypi/Flask-Security-Fork>`__
  `#813 <https://github.com/opendatateam/udata/pull/813>`__
- Migrated remaining widgets to Vue.js `#828 <https://github.com/opendatateam/udata/pull/828>`__:

  - bug fixes on migrated widgets (Issues button/modal, integrate popover, coverage map)
  - more coherent JS environment for developpers
  - lighter assets
  - drop Handlebars dependency

- bleach and html5lib have been updated leading to more secure html/markdown cleanup
  and `better performances <http://bluesock.org/~willkg/blog/dev/bleach_2_0.html>`__
  `#838 <https://github.com/opendatateam/udata/pull/838>`__
- Drop `jquery-slimscroll` and fix admin menu scrolling
  `#851 <https://github.com/opendatateam/udata/pull/851>`__
- drop jquery.dotdotdot for a lighter css-only solution (less memory consumption)
  `#853 <https://github.com/opendatateam/udata/pull/853>`__
- Lighter style `#869 <https://github.com/opendatateam/udata/pull/869>`__:

  - Drop glyphicons and use only Font-Awesome (more coherence, less fonts)
  - lighter bootstrap style by importing only what's needed
  - make use of bootstrap and admin-lte variables (easier for theming)
  - proper separation between front and admin style
- Drop `ExtractTextPlugin` on Vue components style:

  - faster (re)compilation time
  - resolves most compilation and missing style issues
    `#555 <https://github.com/opendatateam/udata/issues/555>`__
    `#710 <https://github.com/opendatateam/udata/issues/710>`__
  - allows use of hot components reloading.
- Pure Vue.js modals. Fix the default membership role. Added contribute modal.
  `#873 <https://github.com/opendatateam/udata/pull/873>`__
- Easier Vue.js development/debugging:

  - Drop `Vue.config.replace = false`: compatible with Vue.js 1/2 and no more style guessing
    `#760 <https://github.com/opendatateam/udata/pull/760>`__
  - `name` on all components: no more `Anonymous Component` in Vue debugger
  - No more `Fragments`
  - More ES6 everywhere
- Make metrics deactivable for tests
  `#905 <https://github.com/opendatateam/udata/pull/905>`__

1.0.11 (2017-05-25)
-------------------

- Fix presubmit form errors handling
  `#909 <https://github.com/opendatateam/udata/pull/909>`__
- Fix producer sidebar image sizing
  `#913 <https://github.com/opendatateam/udata/issues/913>`__
- Fix js `Model.save()` not updating in some cases
  `#910 <https://github.com/opendatateam/udata/pull/910>`__

1.0.10 (2017-05-11)
-------------------

- Fix bad stored (community) resources URLs [migration]
  `#882 <https://github.com/opendatateam/udata/issues/882>`__
- Proper producer logo display on dataset pages
- Fix CKAN harvester empty notes and `metadata` file type handling
- Remove (temporary) badges metrics
  `#885 <https://github.com/opendatateam/udata/issues/885>`__
- Test and fix topic search
  `#892 <https://github.com/opendatateam/udata/pull/892>`__

1.0.9 (2017-04-23)
------------------

- Fix broken post view
  `#877 <https://github.com/opendatateam/udata/pull/877>`__
- Fix new issue submission
  `#874 <https://github.com/opendatateam/udata/issues/874>`__
- Display full images/logo/avatars URL in references too
  `#824 <https://github.com/opendatateam/udata/issues/824>`__

1.0.8 (2017-04-14)
------------------

- Allow more headers in cors preflight headers
  `#857 <https://github.com/opendatateam/udata/pull/857>`__
  `#860 <https://github.com/opendatateam/udata/pull/860>`__
- Fix editorialization admin
  `#863 <https://github.com/opendatateam/udata/pull/863>`__
- Fix missing completer images and ensure completion API is usable on a different domain
  `#864 <https://github.com/opendatateam/udata/pull/864>`__

1.0.7 (2017-04-07)
------------------

- Fix display for zone completer existing values
  `#845 <https://github.com/opendatateam/udata/issues/845>`__
- Proper badge display on dataset and organization page
  `#849 <https://github.com/opendatateam/udata/issues/849>`__
- Remove useless `discussions` from views contexts.
  `#850 <https://github.com/opendatateam/udata/pull/850>`__
- Fix the inline resource edit button not redirecting to admin
  `#852 <https://github.com/opendatateam/udata/pull/852>`__
- Fix broken checksum component
  `#846 <https://github.com/opendatateam/udata/issues/846>`__

1.0.6 (2017-04-01)
------------------

- Default values are properly displayed on dataset form
  `#745 <https://github.com/opendatateam/udata/issues/745>`__
- Prevent a redirect on discussion fetch
  `#795 <https://github.com/opendatateam/udata/issues/795>`__
- API exposes both original and biggest thumbnail for organization logo, reuse image and user avatar
  `#824 <https://github.com/opendatateam/udata/issues/824>`__
- Restore the broken URL check feature
  `#840 <https://github.com/opendatateam/udata/issues/840>`__
- Temporarily ignore INSPIRE in ODS harvester
  `#837 <https://github.com/opendatateam/udata/pull/837>`__
- Allow `X-API-KEY` and `X-Fields` in cors preflight headers
  `#841 <https://github.com/opendatateam/udata/pull/841>`__

1.0.5 (2017-03-27)
------------------

- Fixes error display in forms `#830 <https://github.com/opendatateam/udata/pull/830>`__
- Fixes date range picker dates validation `#830 <https://github.com/opendatateam/udata/pull/830>`__
- Fix badges entries not showing in admin `#825 <https://github.com/opendatateam/udata/pull/825>`__

1.0.4 (2017-03-01)
------------------

- Fix badges trying to use API too early
  `#799 <https://github.com/opendatateam/udata/pull/799>`__
- Some minor tuning on generic references
  `#801 <https://github.com/opendatateam/udata/pull/801>`__
- Cleanup factories
  `#808 <https://github.com/opendatateam/udata/pull/808>`__
- Fix user default metrics not being set [migration]
  `#809 <https://github.com/opendatateam/udata/pull/809>`__
- Fix metric update after transfer
  `#810 <https://github.com/opendatateam/udata/pull/810>`__
- Improve spatial completion ponderation (spatial zones reindexation required)
  `#811 <https://github.com/opendatateam/udata/pull/811>`__

1.0.3 (2017-02-21)
------------------

- Fix JavaScript locales handling `#786 <https://github.com/opendatateam/udata/pull/786>`__
- Optimize images sizes for territory placeholders `#788 <https://github.com/opendatateam/udata/issues/788>`__
- Restore placeholders in search suggestions, fix `#790 <https://github.com/opendatateam/udata/issues/790>`__
- Fix share popover in production build `#793 <https://github.com/opendatateam/udata/pull/793>`__

1.0.2 (2017-02-20)
------------------

- Fix assets packaging for production `#763 <https://github.com/opendatateam/udata/pull/763>`__ `#765 <https://github.com/opendatateam/udata/pull/765>`__
- Transform `udata_version` jinja global into a reusable (by themes) `package_version` `#768 <https://github.com/opendatateam/udata/pull/768>`__
- Ensure topics datasets and reuses can display event with a topic parameter `#769 <https://github.com/opendatateam/udata/pull/769>`__
- Raise a `400 Bad Request` when a bad `class` attribute is provided to the API
  (for entry point not using forms). `#772 <https://github.com/opendatateam/udata/issues/772>`__
- Fix datasets with spatial coverage not being indexed `#778 <https://github.com/opendatateam/udata/issues/778>`__
- Ensure theme assets cache is versionned (and flushed when necessary)
  `#781 <https://github.com/opendatateam/udata/pull/781>`__
- Raise maximum tag length to 96 in order to at least support
  `official INSPIRE tags <http://inspire.ec.europa.eu/theme>`__
  `#782 <https://github.com/opendatateam/udata/pull/782>`__
- Properly raise 400 error on transfer API in case of bad subject or recipient
  `#784 <https://github.com/opendatateam/udata/pull/784>`__
- Fix broken OEmbed rendering `#783 <https://github.com/opendatateam/udata/issues/783>`__
- Improve crawlers behavior by adding some `meta[name=robots]` on pages requiring it
  `#777 <https://github.com/opendatateam/udata/pull/777>`__

1.0.1 (2017-02-16)
------------------

- Pin PyMongo version (only compatible with PyMongo 3+)

1.0.0 (2017-02-16)
------------------

Breaking Changes
****************

* 2016-05-11: Upgrade of ElasticSearch from 1.7 to 2.3 `#449 <https://github.com/opendatateam/udata/pull/449>`__

You have to re-initialize the index from scratch, not just use the `reindex` command given that ElasticSearch 2+ doesn't provide a way to `delete mappings <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-delete-mapping.html>`__ anymore. The command is `udata search init` and may take some time given the amount of data you are dealing with.

* 2017-01-18: User search and listing has been removed (privacy concern)

New & Improved
**************

* 2017-01-06: Add some dataset ponderation factor: temporal coverage, spatial coverage,
  certified provenance and more weight for featured ones. Need reindexation to be taken into account.

* 2016-12-20: Use all the `Dublin Core Frequencies <http://dublincore.org/groups/collections/frequency/>`__
  plus some extra frequencies.

* 2016-12-01: Add the possibility for a user to delete its account in the admin interface

In some configurations, this feature should be deactivated, typically when
there is an SSO in front of udata which may cause some inconsistencies. In
that case, the configuration parameter DELETE_ME should be set to False (True
by default).

* 2016-05-12: Add fields masks to reduce API payloads `#451 <https://github.com/opendatateam/udata/pull/451>`__

The addition of `fields masks <http://flask-restplus.readthedocs.io/en/stable/mask.html>`__ in Flask-RESTPlus allows us to reduce the retrieved payload within the admin — especially for datasets — and results in a performances boost.

Fixes
*****

* 2016-11-29: Mark active users as confirmed `#619 <https://github.com/opendatateam/udata/pull/618>`__
* 2016-11-28: Merge duplicate users `#617 <https://github.com/opendatateam/udata/pull/617>`__
  (A reindexation is necessary after this migration)

Deprecation
***********

Theses are deprecated and support will be removed in some feature release.
See `Deprecation Policy <https://udata.readthedocs.io/en/stable/versionning/#deprecation-policy>`__.

* Theses frequencies are deprecated for their Dublin Core counter part:
    * `fortnighly` ⇨ `biweekly`
    * `biannual` ⇨ `semiannual`
    * `realtime` ⇨ `continuous`


0.9.0 (2017-01-10)
------------------

- First published version



