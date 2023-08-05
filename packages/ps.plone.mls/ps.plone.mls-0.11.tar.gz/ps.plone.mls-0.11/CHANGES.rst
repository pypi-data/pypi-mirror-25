Changelog
=========


0.11 (2017-09-12)
-----------------

- Remove Archetypes dependency.
- Don't run event handler when add-on is not installed.


0.10 (2017-09-05)
-----------------

- Show banner image for development collection, if enabled and available.
- Show better title for development listings results.
- Make select2 dropdowns take full width for listing search (Plone 5 only).


0.9 (2017-08-21)
----------------

- Rerun GS profiles for Plone 5 when doing upgrade from 4 to 5.
- Update Plone 5 experience for listings and developments.
- Use low level api caching using plone.memoize.ram.


0.8.1 (2017-05-26)
------------------

- Sort available listing pages vocabulary by title.
- I18N updates.


0.8 (2017-05-12)
----------------

- Add configurable listing search banner.
- Update translations.
- Disable inline validation for MLS portlet forms, collective.cover tile forms and listing search banner forms.


0.7 (2017-04-24)
----------------

- Add Plone 5 compatibility.


0.6 (2017-04-12)
----------------

- Use plone.api.portal.send_email to send emails. Fixes utf-8 encoding issues.
- Make development contact email message body translatable.
- Use combination of portal title and development title for email subject.
- Add BCC recipients to development contact email, if available.


0.5.5 (2017-04-04)
------------------

- In development contact form, use sender for email 'from', instead of 'reply-to'.


0.5.4 (2017-02-08)
------------------

- Fix NotFound error for listing details when development has more than 25 listings.


0.5.3 (2016-11-18)
------------------

- Use fixed limit to check for valid development within collection.


0.5.2 (2016-11-07)
------------------

- Use correct limit for development collection traverser.


0.5.1 (2016-11-07)
------------------

- Fix manifest.
- Fix CSS.
- Remove extra colon after labels which is now added via CSS.


0.5 (2016-10-17)
----------------

- Modify the TitleViewlet to create a custom title for ListingDetail views.
- Override the DublinCore viewlet to create custom metatags for ListingDetail and DevelopmentDetail views.
- Bugfix: Developments on second page of a collection (and beyond) cannot be shown.
- Bugfix: Allow print-listing view on listings within a development.
- Check for valid development listings.
- Remove Google Maps API from portal_javascripts.
- Google Maps now uses configured API key.


0.4 (2016-05-20)
----------------

- Add CSS classes to listing summary fields.
- Only show development detail page if development is available in collection.
- Show interior area and living area in listing summary, if available.


0.3 (2016-02-18)
----------------

- Fix canonical links for development detail pages to point to themselves rather than the development collection.


0.2.8 (2016-02-10)
------------------

- Added option switch between short and long urls for development collections.
- Fix robot tests.
- Fix code-analysis errors and warnings.


0.2.7 (2015-08-29)
------------------

- *bugfix:* Development contact form crashed on ascii characters in name or message


0.2.6 (2015-08-11)
------------------

- improved styling for Development header captions


0.2.5 (2015-07-07)
------------------

- No changes yet.


0.2.4 (2015-06-11)
------------------

- prevent pagination error of plone.batching (1.0.4) in *development details*


0.2.3 (2015-06-11)
------------------

- **Develoments Details:** add hover *"title"* for development icons


0.2.2 (2015-06-02)
------------------

- Develoments Summary: get custom css class for prettier results


0.2.1 (2015-06-01)
------------------

- improve Developments Summary View
- improve Developments Detail View: no prettyPhoto Iframe links for phase-listings


0.2 (2015-05-13)
----------------

- Added Developer MLS Embedding.
- Added additional fields to customize the contact information (agency and agent).
- I18N updates.


0.1 (2014-07-15)
----------------

- Initial release.
- Added 'Featured Listings' content type and viewlet.
