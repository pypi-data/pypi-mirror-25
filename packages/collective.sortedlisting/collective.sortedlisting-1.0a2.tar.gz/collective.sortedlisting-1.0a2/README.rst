.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================
collective.sortablequerystring
==============================

Plone Collection type is a very flexible way to aggregate
content from your site. It supports querying the catalog
together with sorting the results according to an
sortable index (modified date, title, etc.).

Sometimes you need a customized sorting of the results.
Think of a folder with many person content items in it
and you want to display it with sorting A
in one place of your site and with sorting B
in another place of a site.

This is where this addon steps in. It allows to
sort the results of a collection query on the
collection/listing itself. It is done by the editor.


Features
--------

If you install a package it will provide a custom
contenttype (SortableCollection) which has the same
features as the standard Collection type and additionally
allows the sorting of the results in the preview section
with drag&drop.

The contenttype makes use of a behavior (SortableCollection)
which can be used by custom contenttypes.

If you have Mosaic installed the addon provides the
*Sortable Contentlisting* tile which inherits from
the Contentlisting tile from plone.app.standardtiles
with the additional sorting features.

Examples
--------

.. image:: https://img.youtube.com/vi/VNLGuDHVJ_o/0.jpg
	:target: https://www.youtube.com/watch?v=VNLGuDHVJ_o
	:alt: Sortedlisting demo video


Installation
------------

Requirements: Plone 5.1

Install collective.sortedquerystring by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.sortedquerystring


and then running ``bin/buildout``

Development
-----------

.. image:: https://travis-ci.org/collective/collective.sortedlisting.svg?branch=master
    :target: https://travis-ci.org/collective/collective.sortedlisting


.. image:: https://coveralls.io/repos/github/collective/collective.sortedlisting/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.sortedlisting?branch=master


Build mockup (only Plone 5.1b4 and below) ::

  $ bin/plone-compile-resources -s Plone -b plone
  $ bin/plone-compile-resources -s Plone -b plone-logged-in

Build resources ::

  $ bin/plone-compile-resources -s Plone -b sortablequerystring

Contribute
----------

 - Issue Tracker: https://github.com/collective/collective.sortedlisting/issues
 - Source Code: https://github.com/collective/collective.listing
 - Documentation: https://docs.plone.org/foo/bar

License
-------

The project is licensed under the GPLv2.
