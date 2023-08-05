.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

{{ addon_name_len * '=' }}
{{ addon_name }}
{{ addon_name_len * '=' }}


{{ addon_description }}

Installation
============

Copy the module to the `addons_path` then update the list of the module,

Look for `{{ addon_slug }}` and install it.


Credits
=======

Contributors
------------

* {{ user_name }}{% if user_email %} <{{ user_email }}>{% endif %}

{% if user_company %}
Maintainer
----------

This module is maintained by {{ user_company }}.{% endif %}

