# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import grp3.types


class Grp3TypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=grp3.types)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'grp3.types:default')


GRP3_TYPES_FIXTURE = Grp3TypesLayer()


GRP3_TYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GRP3_TYPES_FIXTURE,),
    name='Grp3TypesLayer:IntegrationTesting',
)


GRP3_TYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GRP3_TYPES_FIXTURE,),
    name='Grp3TypesLayer:FunctionalTesting',
)


GRP3_TYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        GRP3_TYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='Grp3TypesLayer:AcceptanceTesting',
)
