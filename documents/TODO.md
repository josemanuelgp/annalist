# Annalist TODO

   - proposed activity
   > in progress
   / completed
   x rejected
   * additional note

NOTE: information in this document is being migrated to [Github issues](https://github.com/gklyne/annalist/issues) and a [roadmap document](roadmap.md).


## Initial web application outline plan

Initially guided by mockups per https://github.com/gklyne/annalist/tree/develop/mockup

1.  Front page/initial display
    * [x] form elements to create new collection
    * [x] form elements to delete collection
    * [x] include supporting logic in Collection module
    * [x] rework authentication/authorization to allow unauthenticated access for public data 
    * [x] test cases for site, site views; refactor tests to separate directory, modules
    * [x] adopt responsive CSS framework (Foundation)
2.  Collection display
    * [x] refactor metadata field access to common superclass
    * [x] types
        * [x] implement skeleton RecordType module
        * [x] create test cases for types in collection
        * [x] implement type methods
    * [x] views
        * [x] implement skeleton RecordView module
        * [x] create test cases for views in collection
        * [x] implement view methods
    * [x] lists
        * [x] implement skeleton RecordList module
        * [x] create test cases for lists in collection
        * [x] implement list methods
    * [x] UI test cases
    * [x] form elements to add/delete types/views/lists/...
    * [x] Add CollectionActionView test cases (handled with entity managed)
3. Record type display
    * [x] template
    * [x] view: edit form display
    * [x] view test cases
    * [x] refactor redirect_info, redirect_error in generic view to takle URI rather than view name parameter, and add new method to handle URI generation from view name + params.
    * [x] model
    * [x] model test cases
    * [x] view edit form response handling
    * [x] refactor code locally
    * [x] more refactoring; try to abstract common logic for RecordList, RecordView
    * [x] review generic view base functions - should some be inlined now?
    * [x] Move types/views/lists data into _annalist_collection directory
4. Default record view/edit display (code to be refactored later)
    * [x] form generation
    * [x] form display test cases
    * [x] provision for data access fallback to site data (for types, views, fields, etc.)
    * [x] form response handler
    * [x] test cases
    * [x] refactor URI and test data support for test cases to separate module; use reverse for URI generation; 
    * [x] refactor DefaultEdit form display
    - [x] WONTDO: isolate directory generation for tests.
    * [x] change <site>/collections/ to <site>/c/ or <site>/coll/ throughout.
    - [x] WONTDO: Similar for /d/ and /data/?
    * [x] include path values in entities.
    - [x] WONTDO: include base and reference values in entities. (later: requires use of @context)
    * [x] create data view display based on generic render logic
    * [x] editing recordtype: returns "already exists" error; display operation (new, copy, edit, etc) in edit form
    * [x] function to create initial development site data (based on test code)
    - [x] WONTDO: entity should carry its own RecordType id (where it's kept within a collection).  Have implemented alternative mechanism through bound_field that allows the entity to be less self-aware, hence more easily ported.
    * [x] menu dropdown on small display not working: need JS from Zurb site? (fixed by update to 5.2.1)
5. Default record list display
    * [x] form generation
    * [x] form display test cases (initial for default and all)
    * [x] include sitedata lists in drop-down
    * [x] form response handler (delete and others todo)
    * [x] entity list view: add selection fields (and classes)
    * [x] form response test cases
    * [x] customize response handler
    * [x] new entity from list-all display; changing type of entity
        * [x] Create default type in site data
        * [x] Create field render type for drop-down (render_utils and field template)
        * [x] Add field to default display
        * [x] Add type list data to display context
        * [x] Add original type as hidden field in edit form
        * [x] Add logic to form submission handler
        * [x] add test cases for changing type id (new and edit)
        - [x] WONTDO: remove recordtypedata access from entityeditbase.get_coll_type_data to POST handler (for recordtype, etc., the collection object is supplied as parent, so this is not so simple.)
        * [x] remove return_value from field definitions - this is now handled differently
        * [x] new record from list all: use default type, not random selection
        * [x] new record, change type, error doesn't redisplay types
        * [x] error loses continuation URI in edit form
        * [x] remove message header that appears on return from form edit (appears to be resolved?)
        * [x] review skipped tests - can any be enabled now?
        * [x] delete entity continues to wrong page
    * [x] add entity links to list views
        * [x] Update bound_field to provide access to entity URI
        * [x] Create field render type for entity ref
        * [x] Update field in default list displays
    * [x] connect site display to default display of entities, not customize
    * [x] connect list display to record view display
    * [x] build entity selector logic into list view
6. Generic entity edit view
    * [x] extract/generalize relevant logic from `defaultedit.py`
    * [x] parameterize view-id on extra URI field
    * [x] create new URI mapping entries
    * [x] create new test suite for generic edit view
    * [x] refactor defaultedit.py as special case (subclass?)
    * [x] fix urls.py error and re-test
7. Generic record list display and editing
    * [x] extract/generalize relevant logic from `defaultlist.py`
    * [x] refactor defaultlist.py as special case (subclass?)
    * [x] parameterize view-id on extra URI field
    * [x] create new URI mapping entries
    * [x] create new test suite for generic list view
        * [x] choose test scenario: Field definitions: http://localhost:8000/annalist/c/coll1/d/_field/ 
        * [x] list field descriptions?  Need to create list description (4 fields?).  http://localhost:8000/annalist/c/coll1/l/Fields_list/_field/
        * [x] also choose / define default view for list (Create field view?)
        * [x] need to rationalize entity display structure to encompass data, collection level metadata and site-level metadata.
        * [x] check list display in dev app
        * [x] define test suite test_genericentitylist based loosely on test_entitydefaultlist
        * [x] create test case for creating/editing site metadata entities (currently fail in dev system) e.g. create test_entitymetadataedit based on entitygenericedit.
        * [x] create edit view tests for all the main entity classes (type, view, list, data), along the lines of test_entityfieldedit, moving support code out of entity_testutils.
            * [x] copy/refactor test_recordtype to use same pattern as test_entityfieldedit
            * [x] see if old record type view class can be deleted
            * [x] incorporate model tests in test_entityfieldedit (cf. test_recordtype)
            * [x] rename test_entityfieldedit -> test_recordfield? (cf. test_recordtype)
        * [x] resolve overloading of "entity_uri" in context.
    * [x] entity_uri appears in entity view context as name (same as annal:uri) but also in bound field as locator.  Change name used in bound field to `entity_ref`.
    * [x] refactor delete confirm code to generic module, with type-specific messages.  Note that type, view and list deletes are triggered from the collection edit view, with different form variables, and also have specific remove functions in the collection class, so need separate implementations (for now?).
    * [x] update render template/logic for RecordView_view
    * [x] update template to include delete field options; finalize form response data
    * [x] implement tests for add/delete fields
    * [x] implement handlers for add/delete fields
    * [x] edit form response should update, not replace, any data from the original (so data from multiple views is not discarded).
    * [x] implement delete confirm view for views and lists.
    * [x] review missing tests: implement or delete?
    * [x] fix up view links from list display
    * [x] define View-list and List-list
    * [x] view button handler from list display + test
    * [x] continuation handling: replace by more generic parameter handling based on dictionary; move handling of escape logic, etc.
    * [x] search button handler from list display
    * [x] consider that 'Find' and 'View' buttons could be combined
    * [x] don't include continuation-uri param when URI is blank
    * [x] implement some version of entity selection logic
    * [x] decide how to handle presentation of field types (where?): (a) use simple text string, not CURIE; (b) use CURIE, but use render type to extract ID; but will need to map back when form is submitted?
        * [x] it all rather depends on the anticipated extensibility model for field types.  Option (a) is simplest for now.
    * [x] default_view response handler (needs generic view to make sense)
    * [x] implement view- and list- edit from collection customization page
    * [x] implement per-type default list and view
        * [x] already works for list view; e.g. http://localhost:8000/annalist/c/coll1/d/_type/
        * [x] but not yet for entity view; e.g. http://localhost:8000/annalist/c/coll1/d/_type/type1/
        * [x] return list_info structure rather than saving values in object. 
    * [x] consider replicating list_seup logic for view_setup.
    * [x] find and eliminate other references to get_coll_data, etc.
    * [x] don't return placeholder text in a form as field value; use HTML5 placeholder attribute
    * [x] refactor fields package as subpackage of views
    * [x] fix entity links to use default view URI (/d/...)
    * [x] List type + "View" selection uses // for type field - select based on list or suppress
    * [x] customize > edit record view > add field > cancel -- returns to wrong place.
    * [x] need test case for remove field with no field selected
    * [x] factor out add-field logic used by current add-field code
    * [x] test case for POST with 'add_view_field'
    * [x] provide option to invoke add-field logic during initial form rendering
    * [x] add_field button on entity edit displays; need way to control its inclusion
    * [x] new entity initialization vector through typeinfo, AND/OR provide mechanism to associate initial values for each entity type.
    * [x] "Add field" when creating new entity results in multiple entities created (use !edit for continuation URI?)  Add test case.
    * [x] tests
        * [x] skipped '@@TODO defaultlist default-view button handler'
        * [x] skipped '@@TODO defaultlist search button handler'
        * [x] skipped '@@TODO genericlist default-view button handler'
        * [x] skipped '@@TODO genericlist search button handler'
            * [x] annalist.tests.test_entitygenericlist.EntityGenericListViewTest
        * [x] skipped '@@TODO genericlist default list button'
            * [x] annalist.tests.test_entitygenericlist.EntityGenericListViewTest
8. initial application testing
    * [x] review and simplify bound_field logic for accessing field_value
    * [x] Create new type - appears twice in default_list_all display.  Delete one deletes both appearances, so this looks like display problem.  I thought this had been fixed.  Confirmed to be knock-on from incorrect creation of _type data (see next).
    * [x] New entry save as _type does not create new type in collection
    * [x] field view has size/position field; use as default when adding to view.
    * [x] viewing new entity with custom type generates "keyerror annal:value_type" @ fielddescription.py line 55.
    * [x] update field view description to display all relevant fields; ???
    * [x] when defining a field, the render type selected also implies a field value type; handle this in "FieldDescription constructor?"  Later, maybe.  For now, add value type field.
    * [x] make FieldDescription constructor more resilient to missing data.
    * [x] Changing type to built-in type in entity edit display does not save to correct location
    * [x] List editing view formatting is messed up (small-6?)
    * [x] Click on local type in default_list, then cancel, returns to Type_list display.  No continuation_uri in links.
    * [x] Click on local record in Default_list, cancel, returns to default data display (/d/ rather than /l/).  In default display, types don't appear.
    * [x] grey out set_default button on collection default display (/d/, /l/)
    * [x] When creating new collection, there's no obvious way to create a new record type (or view).
    * [x] Handle bare /l/ URI and redirect to default view for collection
    * [x] Remove precalculated list_ids and view_ids from view context
    * [x] Script to refresh sitedata in devel site
    * [x] In view editing, provide field id drodown
    * [x] In list displays, hyperlink entity type to view/edit form
    * [x] No easy way to create field description while editing view details; include new-field button
        * [x] update form template
        * [x] implement handler for 'new_field' response
        * [x] implement test case for 'new_field' response
        * [x] list description view not showing types or views in dropdowns
        * [x] introduce Default_field type
    * [x] When defining field, missing placement is silently ignored; field is not saved; (still)
    * [x] Authorization of field editing is not handled consistently:  allows config when no delete authz (no login)
    * [x] Display of remove-field checkbox based on "delete" permission. 
    * [x] Save entity edit is not requiring login - should check from POST?
    * [x] Entityedit add test cases for unauthorized config requests (and more?)
    * [x] From type display, want easy retreat to default display for collection
    * [x] View_type display should suppress add-field option.  Similar for View_list and View_field?
    * [x] suppress _initial_values as option when selecting type/view/list
    - [x] WONTDO: Add field allows new view type to be created, but how to make this default for displayed type?
    * [x] Generic field renderer for entityref as selection among available entity ids.  Use for field selection.  Options should be reworked using this form of enumeration, handled on the fly as required, using type information from the field definition.
    * [x] Type view should have dropdowns for default view and list
    * [x] List view selector syntax isn't working: need to nail down how type selection can work.  In saved data, I'm seeing '"annal:type": "annal:EntityData"', which isn't realy helpful.
        * [x] change all references to annal:type to @type, in sitedata and code (i.e. URIs/CURIE values).  E.g. annal:Type, annal:View, annal:EntityData, etc.
        * [x] for annal:type, assign local type_id value.  Consider renaming as annal:type_id.
        * [x] annal:type is retained for URI/CURIE of entity class (is this helpful?)
        * [x] list type selectors then use local type_id values.
    - [x] WONTDO: @type list selector - allow selection by type substring - e.g. coll/type
    * [x] When not logged in, should still have option to select a different view
    * [x] From list view, continuation URI for new, copy, etc should exclude message parameters.  In particular, links in rendered fields have the extra stuff.  (But do include ?search param)
    * [x] Customize > delete record > confirm : returns to wrong place
    * [x] Generalized enumeration types
        * [x] Define new RecordEnum class with type_id parameter on constructor; dynamically created directory paths; dynamic class creation?
        * [x] Test cases for RecordEnum
        - [x] WONTDO: Add optional type_id to all entity constructors (ignore on existing)
        * [x] Update entitytypeinfo to support enum types
        * [x] More test cases?
        * [x] Review, rationalize type naming and type ids.  Update sitedata.
        * [x] Update list type field definition
        * [x] Update tests using list type field definition
        * [x] Create type records for enumeration types, used for:
            - locating the default view and/or list id for records of that type
            - getting entity @type URI/CURIE values while editing
            - getting a view/edit link to type record
            - See notes in models.typeinfo
    * [x] Enumeration type for list types (list/grid: default list)
        * [x] Update field definition
        * [x] Create type record
        * [x] Update/add tests cases
    * [x] Enumeration type for field render types (text, testarea, etc...); use in fields display
        * [x] Create enumeration data
        * [x] Update field definition
        * [x] Create type records
        * [x] Update/add tests cases
        * [x] development test site is broken - why?  Isolate problem in test before fixing.
    * [x] allow '//' comments in JSON files - strip out before parsing JSON (but leave blank lines)
    * [x] Don't show Bib_* fields for non-biblio record types 
        - [x] WONTDO: Move Bib_* fields to separate "built-in" collection
        - [x] WONTDO: Can enumeration-like logic be used to support sub-areas in site data?
        * Long term is to move Bib_ field types out of site data, and provide easy way to incorporate library fragments into new collections, but for now they are part of the test environment.  See below.
        * Alternative might be value-scoped enumerations
        * [x] Update EntityFinder logic to support tests comparing with enclosing view fields
        * [x] Update entity selector call site (just one)
        * [x] Update selector syntax and sitedata
        * [x] Use EntityFinder logic in enumeration selection (FieldDescription.py)
        * [x] Add view context to FieldDescription
        * [x] Introduce biblio record type
        * [x] Introduce biblio record list
        * [x] Update test cases
        * [x] Field name updates (field_render, value_type)
        * [x] Update test cases
        * [x] Add fields to restrict bib_* fields to BibEntry views
            - [x] WONTDO: Declare additional/multiple types for entity?
        * [x] Update field selector view
        * [x] Use field selector in FieldDescription
        * [x] Update test cases
9. Prepare for release 0.1
    * [x] feature freeze
    * [x] version identifier in system
    * [x] remove dead code
    * [x] test with Django 1.7
    * [x] installation package
    * [x] test installation on non-development system
        * [x] sorting of enumeration lists
        * [x] sorting of entity lists (by typeid then entityid)
        * [x] sorting of entity lists enumerated in tests
        * There could be more test cases that need hardening, but so far all pass on a Linux deployment
    * [x] check python version in setup
    * [x] __init__.py in annalist_root dir causes test failure on Ubuntu 14.04; cf. https://code.djangoproject.com/ticket/22280.   Removing it solves the test case problem, but it was included originally to get the setup.py script to work as intended.  Try removing it and see if we can get kit builder to work.
    * [x] Login page - link to local Django login & admin pages
    * [x] Fix profile display with local credentials
    * [x] Logged-in username should appear in top menu; e.g. xxxx profile or xxxx: profile logout
    * [x] root URI - redirect to /annalist/site/
    * [x] utility/script for running tests
    * [x] utility/script for site creation
    * [x] utility/script for running server
    * [x] online help text (initial)
    - [x] WONTDO: Test installation on Windows (De-prioritized for now. Tests pass, but having problems accessing the settings when running the server. Change directory?)
    * [x] Documentation
        * [x] release notes/introduction;  link from README (about this release); key missing features/issues
        * [x] installation - link from README
        * [x] getting started - reference installation then walk through demo sequence; link from README (getting started);
        - [>] demo script (needs cleaning up)
        * [x] using Annalist - flesh out; link from README
        * [x] flesh out introduction/overview
        * [x] how to setup OpenIDConnect providers - move to separate document; link from installation doc
        * [x] tidy up README
        * [x] Move remaining TODOs to Roadmap and issues
        * [x] Flesh out roadmap
    * [x] Create mailing list -- see https://groups.google.com/forum/#!forum/annalist-discuss
    - [>] Demo deployment
    * [x] Demo screencast -- see http://annalist.net
    - [ ] Add TODO list to release notes, and reset
    - [ ] Bump version and update history
    - [ ] Final updates to master
    * [x] Post kit download
    - [ ] Upload to PyPI
    - [ ] Post announcement to Google Group, and elsewhere
