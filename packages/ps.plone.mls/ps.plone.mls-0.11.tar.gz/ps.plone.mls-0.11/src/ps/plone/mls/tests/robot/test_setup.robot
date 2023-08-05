*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form
    Page should contain element  xpath=//*[@value='ps.plone.mls']
    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::li
    ...  addons-psplonemls
    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::ul/parent::*/parent::*
    ...  addons-enabled

    Highlight  addons-psplonemls
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  id=addons-enabled


Show how to configure the base MLS settings
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@mls-controlpanel
    ${note1}  Add pointy note  css=#form-widgets-mls_key
    ...  Enter your MLS API-Key
    ...  position=right
    ${note2}  Add pointy note  css=#form-widgets-mls_site
    ...  Enter the URL for the MLS
    ...  position=right
    ${note3}  Add pointy note  css=#form-widgets-agency_id
    ...  Enter your agency id
    ...  position=right
    Capture and crop page screenshot
    ...  configure_base_settings.png
    ...  css=#content
    ...  ${note1}  ${note2}  ${note3}
    Remove elements  ${note1}  ${note2}  ${note3}
