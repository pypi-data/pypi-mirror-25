*** Variables ***

# Default variables used for testing. Customized variables might
# exist for specific Plone versions.

${POSITION_CONTENTMENU_ACTIONS_NOTE}  left

${CONTENTMENU_ACTIONS}  id=contentActionMenus
${LINK_CONTENTMENU_ACTIONS}  css=#plone-contentmenu-actions dt a
${LIST_CONTENTMENU_ACTIONS}  css=#plone-contentmenu-actions dd.actionMenuContent
${CONTENT}  css=#portal-column-content
${STATUS_MESSAGE}  css=dl.portalMessage

# "Listing Collection"
${LISTING_COLLECTION_ACTIVATE_LINK}  css=#plone-contentmenu-actions-listing-collection-activate
${LISTING_COLLECTION_DEACTIVATE_LINK}  css=#plone-contentmenu-actions-listing-collection-deactivate

# "Recent Listings"
${RECENT_LISTINGS_ACTIVATE_LINK}  css=#plone-contentmenu-actions-recent-listings-activate
${RECENT_LISTINGS_DEACTIVATE_LINK}  css=#plone-contentmenu-actions-recent-listings-deactivate

# "Listing Search"
${LISTING_SEARCH_ACTIVATE_LINK}  css=#plone-contentmenu-actions-listing-search-activate
${LISTING_SEARCH_DEACTIVATE_LINK}  css=#plone-contentmenu-actions-listing-search-deactivate

# "Development Collection"
${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}  css=#plone-contentmenu-actions-development-collection-activate
${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}  css=#plone-contentmenu-actions-development-collection-deactivate
${DEVELOPMENT_COLLECTION_CONFIG_TAB_FILTER}  css=#fieldsetlegend-filter
