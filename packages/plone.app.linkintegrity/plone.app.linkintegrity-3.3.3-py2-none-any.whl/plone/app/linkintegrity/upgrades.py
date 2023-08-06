# -*- coding: utf-8 -*-
from plone.app.linkintegrity.handlers import referencedRelationship
from plone.app.uuid.utils import uuidToObject
try:
    from Products.Archetypes.config import REFERENCE_CATALOG
except ImportError:
    REFERENCE_CATALOG = "reference_catalog"
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent import modified

import logging
log = logging.getLogger(__name__)


def migrate_linkintegrity_relations(context):
    """Migrate linkintegrity-relation from reference_catalog to zc.relation.
    """
    reference_catalog = getToolByName(context, REFERENCE_CATALOG, None)
    if reference_catalog is not None:
        for brain in catalog_get_all(reference_catalog):
            # only handle linkintegrity-relations ('relatesTo')
            if brain.relationship != referencedRelationship:
                continue
            source_obj = uuidToObject(brain.sourceUID)
            target_obj = uuidToObject(brain.targetUID)
            if source_obj is None or target_obj is None:
                # reference_catalog may be inconsistent
                log.info('Cannot delete relation since the relation_catalog is inconsistent.')   # noqa: E501
                continue
            # Delete old reference
            reference_catalog.deleteReference(
                source_obj, target_obj, relationship=referencedRelationship)

            # Trigger the recreation of linkintegrity-relation in
            # the relation_catalog (zc.relation)
            modified(source_obj)
            modified(target_obj)


def catalog_get_all(catalog, unique_idx='UID'):
    """Get all brains from the catalog.
    TODO: Replace with import from CMFPlone after the zope4-branch of
    CMFPlone is merged.
    """
    res = [
        catalog({
            unique_idx: catalog._catalog.getIndexDataForRID(it)[unique_idx]
        })[0]
        for it in catalog._catalog.data
    ]
    return res
