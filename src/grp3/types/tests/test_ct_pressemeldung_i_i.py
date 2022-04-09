# -*- coding: utf-8 -*-
from grp3.types.testing import GRP3_TYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class PressemeldungIIIntegrationTest(unittest.TestCase):

    layer = GRP3_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_pressemeldung_i_i_schema(self):
        fti = queryUtility(IDexterityFTI, name='PressemeldungII')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('PressemeldungII')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_pressemeldung_i_i_fti(self):
        fti = queryUtility(IDexterityFTI, name='PressemeldungII')
        self.assertTrue(fti)

    def test_ct_pressemeldung_i_i_factory(self):
        fti = queryUtility(IDexterityFTI, name='PressemeldungII')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_pressemeldung_i_i_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='PressemeldungII',
            id='pressemeldung_i_i',
        )


        parent = obj.__parent__
        self.assertIn('pressemeldung_i_i', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('pressemeldung_i_i', parent.objectIds())

    def test_ct_pressemeldung_i_i_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PressemeldungII')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_pressemeldung_i_i_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PressemeldungII')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'pressemeldung_i_i_id',
            title='PressemeldungII container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
