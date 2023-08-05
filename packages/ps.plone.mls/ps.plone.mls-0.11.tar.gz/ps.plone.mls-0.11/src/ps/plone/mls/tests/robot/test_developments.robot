*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to activate the development collection
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}
    ...  title=A folder
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}
    ...  Click to activate the Development Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_development_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_development_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-development-collection-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_development_collection.png
    ...  ${CONTENT}

    Click link  ${DEVELOPMENT_COLLECTION_CONFIG_TAB_FILTER}

    Capture and crop page screenshot
    ...  configure_development_collection_filter.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}
    ...  Click to deactivate the Development Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_development_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_development_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}
