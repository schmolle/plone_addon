# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from grp3.types.testing import GRP3_TYPES_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that grp3.types is properly installed."""

    layer = GRP3_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if grp3.types is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'grp3.types'))

    def test_browserlayer(self):
        """Test that IGrp3TypesLayer is registered."""
        from grp3.types.interfaces import (
            IGrp3TypesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IGrp3TypesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = GRP3_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['grp3.types'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if grp3.types is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'grp3.types'))

    def test_browserlayer_removed(self):
        """Test that IGrp3TypesLayer is removed."""
        from grp3.types.interfaces import \
            IGrp3TypesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IGrp3TypesLayer,
            utils.registered_layers())
