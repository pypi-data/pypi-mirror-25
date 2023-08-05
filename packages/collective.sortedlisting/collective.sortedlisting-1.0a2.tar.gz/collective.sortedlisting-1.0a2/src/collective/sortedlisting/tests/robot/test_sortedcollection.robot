# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.sortedlisting -t test_sortedcollection.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.sortedlisting.testing.COLLECTIVE_SORTEDLISTING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_sortedcollection.robot
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

** Variables ***

${BROWSER}   Chrome


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a SortableCollection
  Given a logged-in site administrator
    and an add sortedcollection form
   When I type 'My SortableCollection' into the title field
    and I submit the form
   Then a sortedcollection with the title 'My SortableCollection' has been created

Scenario: As a site administrator I can view a SortableCollection
  Given a logged-in site administrator
    and a sortedcollection 'My SortableCollection'
   When I go to the sortedcollection view
   Then I can see the sortedcollection title 'My SortableCollection'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add sortedcollection form
  Go To  ${PLONE_URL}/++add++SortableCollection

a sortedcollection 'My SortableCollection'
  Create content  type=SortableCollection  id=my-sortedcollection  title=My SortableCollection


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the sortedcollection view
  Go To  ${PLONE_URL}/my-sortedcollection
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a sortedcollection with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the sortedcollection title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
