jQuery(function(jq) {

  if (jq('.mls .development__gallery .thumbnails').length > 0) {
    // Build JS Gallery for development detail view.

    // Load the theme ones more. This is necessary for mobile devices.
    Galleria.loadTheme('++resource++plone.mls.listing.javascript/classic/galleria.classic.min.js');
    jq('.mls .development__gallery .thumbnails').before('<div id="galleria" class="development__galleria"></div>');

    // Hide the thumbnails
    jq('.mls .development__gallery .thumbnails').hide();

    // Initialize Galleria.
    var galleria_obj = jq('#galleria').galleria({
      dataSource: '.thumbnails',
      width: 'auto',
      height: 400,
      preload: 3,
      transition: 'fade',
      transitionSpeed: 1000,
      autoplay: 5000
    });
  }

  jq('.listingsearchbanner input').each(function() {
    var label = jq("label[for='" + jq(this).attr('id') + "']");
    this.placeholder = jq.trim(label.text());
  });

  jq('.listingsearchbanner label').each(function() {
    jq(this).hide();
  });

  // Plone 4:
  jq('.listingsearchbanner .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.portletAgentContact .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.portletQuickSearch .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  jq('.listing-search-tile .z3cformInlineValidation').removeClass('z3cformInlineValidation');
  // Plone 5:
  jq('.listingsearchbanner .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.portletAgentContact .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.portletQuickSearch .pat-inlinevalidation').removeClass('pat-inlinevalidation');
  jq('.listing-search-tile .pat-inlinevalidation').removeClass('pat-inlinevalidation');

  if (jq('.listing__results div.results').length > 0) {
    // Hide the form when search was performed and show the edit form options link.
    jq('div.results form').hide();
    jq('div.results .listing__form-toggle').show();
    jq('div.results .listing__form-toggle a').click(function(event) {
      event.preventDefault();
      jq('div.results form').slideToggle();
    });
  }

});
