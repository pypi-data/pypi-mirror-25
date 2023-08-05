# -*- coding: utf-8 -*-
from collective.sortedlisting.behavior import SortableCollectionBehavior
from collective.sortedlisting.interfaces import ISortableCollection
from plone.app.contenttypes.content import Collection
from zope.interface import implementer


@implementer(ISortableCollection)
class SortableCollection(Collection):
    """ Content type sortable collection """

    def results(self, **kwargs):
        return SortableCollectionBehavior(self).results(**kwargs)

# EOF
