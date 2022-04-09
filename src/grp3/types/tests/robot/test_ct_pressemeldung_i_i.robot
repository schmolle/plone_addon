# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s grp3.types -t test_pressemeldung_i_i.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src grp3.types.testing.GRP3_TYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/grp3/types/tests/robot/test_pressemeldung_i_i.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a PressemeldungII
  Given a logged-in site administrator
    and an add PressemeldungII form
   When I type 'My PressemeldungII' into the title field
    and I submit the form
   Then a PressemeldungII with the title 'My PressemeldungII' has been created

Scenario: As a site administrator I can view a PressemeldungII
  Given a logged-in site administrator
    and a PressemeldungII 'My PressemeldungII'
   When I go to the PressemeldungII view
   Then I can see the PressemeldungII title 'My PressemeldungII'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PressemeldungII form
  Go To  ${PLONE_URL}/++add++PressemeldungII

a PressemeldungII 'My PressemeldungII'
  Create content  type=PressemeldungII  id=my-pressemeldung_i_i  title=My PressemeldungII

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PressemeldungII view
  Go To  ${PLONE_URL}/my-pressemeldung_i_i
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PressemeldungII with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PressemeldungII title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
