*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to activate the listing collection
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-1
    ...  title=A Listing Collection
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-1

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_COLLECTION_ACTIVATE_LINK}
    ...  Click to activate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_COLLECTION_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_listing_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_COLLECTION_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_listing_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-listing-collection-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_listing_collection.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-1
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_COLLECTION_DEACTIVATE_LINK}
    ...  Click to deactivate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_COLLECTION_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_listing_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_COLLECTION_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_listing_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}


Show how to activate the recent listings
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-2
    ...  title=Recent Listings
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-2

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_ACTIVATE_LINK}
    ...  Click to activate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_recent_listings.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_recent_listings_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-recent-listings-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_recent_listings.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-2
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_DEACTIVATE_LINK}
    ...  Click to deactivate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_recent_listings.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_recent_listings_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}


Show how to activate the listing search
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-3
    ...  title=A Listing Search
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-3

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_SEARCH_ACTIVATE_LINK}
    ...  Click to activate the Listing Search
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_SEARCH_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_listing_search.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_SEARCH_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_listing_search_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-listing-search-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_listing_search.png
    ...  ${CONTENT}

    Click button  css=#form-config-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-3
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_SEARCH_DEACTIVATE_LINK}
    ...  Click to deactivate the Listing Search
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_SEARCH_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_listing_search.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_SEARCH_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_listing_search_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}
