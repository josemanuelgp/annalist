"""
Tests for RecordView module and view
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import unittest

import logging
log = logging.getLogger(__name__)

from django.conf                        import settings
from django.db                          import models
from django.http                        import QueryDict
from django.contrib.auth.models         import User
from django.test                        import TestCase # cf. https://docs.djangoproject.com/en/dev/topics/testing/tools/#assertions
from django.test.client                 import Client

from annalist.identifiers               import RDF, RDFS, ANNAL
from annalist                           import layout
from annalist.models.site               import Site
from annalist.models.sitedata           import SiteData
from annalist.models.collection         import Collection
from annalist.models.recordview         import RecordView

from annalist.views.recordviewdelete    import RecordViewDeleteConfirmedView

from tests                              import TestHost, TestHostUri, TestBasePath, TestBaseUri, TestBaseDir
from tests                              import init_annalist_test_site
from AnnalistTestCase                   import AnnalistTestCase
from entity_testutils                   import (
    site_dir, collection_dir,
    site_view_uri, collection_edit_uri, 
    collection_create_values,
    site_title
    )
from entity_testviewdata                import (
    recordview_dir,
    recordview_coll_uri, recordview_site_uri, recordview_uri, recordview_edit_uri,
    recordview_value_keys, recordview_load_keys, 
    recordview_create_values, recordview_values, recordview_read_values,
    recordview_entity_view_context_data, 
    recordview_entity_view_form_data, recordview_delete_confirm_form_data
    )
from entity_testentitydata              import (
    entity_uri, entitydata_edit_uri, entitydata_list_type_uri
    )

#   -----------------------------------------------------------------------------
#
#   RecordView tests
#
#   -----------------------------------------------------------------------------

class RecordViewTest(AnnalistTestCase):
    """
    Tests for RecordView object interface
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.sitedata = SiteData(self.testsite)
        self.testcoll = Collection(self.testsite, "testcoll")
        return

    def tearDown(self):
        return

    def test_RecordViewTest(self):
        self.assertEqual(Collection.__name__, "Collection", "Check Collection class name")
        return

    def test_recordview_init(self):
        t = RecordView(self.testcoll, "testview", self.testsite)
        u = recordview_coll_uri(self.testsite, coll_id="testcoll", view_id="testview")
        self.assertEqual(t._entitytype,     ANNAL.CURIE.RecordView)
        self.assertEqual(t._entityfile,     layout.VIEW_META_FILE)
        self.assertEqual(t._entityref,      layout.META_VIEW_REF)
        self.assertEqual(t._entityid,       "testview")
        self.assertEqual(t._entityuri,      u)
        self.assertEqual(t._entitydir,      recordview_dir(view_id="testview"))
        self.assertEqual(t._values,         None)
        return

    def test_recordview1_data(self):
        t = RecordView(self.testcoll, "view1", self.testsite)
        self.assertEqual(t.get_id(), "view1")
        self.assertEqual(t.get_type_id(), "_view")
        self.assertIn("/c/testcoll/_annalist_collection/views/view1/", t.get_uri())
        self.assertEqual(TestBaseUri + "/c/testcoll/d/_view/view1/", t.get_view_uri())
        t.set_values(recordview_create_values(view_id="view1"))
        td = t.get_values()
        self.assertEqual(set(td.keys()), set(recordview_value_keys()))
        v = recordview_values(view_id="view1")
        self.assertDictionaryMatch(td, v)
        return

    def test_recordview2_data(self):
        t = RecordView(self.testcoll, "view2", self.testsite)
        self.assertEqual(t.get_id(), "view2")
        self.assertEqual(t.get_type_id(), "_view")
        self.assertIn("/c/testcoll/_annalist_collection/views/view2/", t.get_uri())
        self.assertEqual(TestBaseUri + "/c/testcoll/d/_view/view2/", t.get_view_uri())
        t.set_values(recordview_create_values(view_id="view2"))
        td = t.get_values()
        self.assertEqual(set(td.keys()), set(recordview_value_keys()))
        v = recordview_values(view_id="view2")
        self.assertDictionaryMatch(td, v)
        return

    def test_recordview_create_load(self):
        t  = RecordView.create(self.testcoll, "view1", recordview_create_values(view_id="view1"))
        td = RecordView.load(self.testcoll, "view1").get_values()
        v  = recordview_read_values(view_id="view1")
        self.assertKeysMatch(td, v)
        self.assertDictionaryMatch(td, v)
        return

    def test_recordview_default_data(self):
        t = RecordView.load(self.testcoll, "Default_view", altparent=self.testsite)
        self.assertEqual(t.get_id(), "Default_view")
        self.assertIn("/c/testcoll/_annalist_collection/views/Default_view", t.get_uri())
        self.assertEqual(t.get_type_id(), "_view")
        td = t.get_values()
        self.assertEqual(set(td.keys()), set(recordview_load_keys()))
        v = recordview_read_values(view_id="Default_view")
        v.update(
            { 'rdfs:label':     'Default record view'
            , 'rdfs:comment':   'Default record view, applied when no view is specified when creating a record.'
            , 'annal:uri':      'annal:view/Default_view'
            })
        self.assertDictionaryMatch(td, v)
        return

#   -----------------------------------------------------------------------------
#
#   RecordView edit view tests
#
#   -----------------------------------------------------------------------------

class RecordViewEditViewTest(AnnalistTestCase):
    """
    Tests for record view edit views
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.testcoll = Collection.create(self.testsite, "testcoll", collection_create_values("testcoll"))
        self.user     = User.objects.create_user('testuser', 'user@test.example.com', 'testpassword')
        self.user.save()
        self.client   = Client(HTTP_HOST=TestHost)
        loggedin      = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(loggedin)
        self.no_options = ['(no options)']
        self.continuation_uri = TestHostUri + entitydata_list_type_uri(coll_id="testcoll", type_id="_view")
        return

    def tearDown(self):
        return

    #   -----------------------------------------------------------------------------
    #   Helpers
    #   -----------------------------------------------------------------------------

    def _create_record_view(self, view_id):
        "Helper function creates record view entry with supplied view_id"
        t = RecordView.create(self.testcoll, view_id, recordview_create_values(view_id=view_id))
        return t    

    def _check_record_view_values(self, view_id, update="RecordView"):
        "Helper function checks content of record view entry with supplied view_id"
        self.assertTrue(RecordView.exists(self.testcoll, view_id))
        t = RecordView.load(self.testcoll, view_id)
        self.assertEqual(t.get_id(), view_id)
        self.assertEqual(t.get_view_uri(), TestHostUri + recordview_uri("testcoll", view_id))
        v = recordview_values(view_id=view_id, update=update)
        self.assertDictionaryMatch(t.get_values(), v)
        return t

    def _check_context_fields(self, response, 
            view_id="(?view_id)", 
            view_label="(?view_label)",
            view_help="(?view_help)",
            view_uri="(?view_uri)"
            ):
        r = response
        self.assertEqual(len(r.context['fields']), 4)        
        # 1st field - Id
        view_id_help = (
            "A short identifier that distinguishes this view from all other views in the same collection."
            )
        self.assertEqual(r.context['fields'][0]['field_id'], 'View_id')
        self.assertEqual(r.context['fields'][0]['field_name'], 'entity_id')
        self.assertEqual(r.context['fields'][0]['field_label'], 'Id')
        self.assertEqual(r.context['fields'][0]['field_help'], view_id_help)
        self.assertEqual(r.context['fields'][0]['field_placeholder'], "(view id)")
        self.assertEqual(r.context['fields'][0]['field_property_uri'], "annal:id")
        self.assertEqual(r.context['fields'][0]['field_render_view'], "field/annalist_view_entityref.html")
        self.assertEqual(r.context['fields'][0]['field_render_edit'], "field/annalist_edit_text.html")
        self.assertEqual(r.context['fields'][0]['field_placement'].field, "small-12 medium-6 columns")
        self.assertEqual(r.context['fields'][0]['field_value_type'], "annal:Slug")
        self.assertEqual(r.context['fields'][0]['field_value'], view_id)
        self.assertEqual(r.context['fields'][0]['options'], self.no_options)
        # 2nd field - Label
        view_label_help = (
            "Short string used to describe view when displayed"
            )
        self.assertEqual(r.context['fields'][1]['field_id'], 'View_label')
        self.assertEqual(r.context['fields'][1]['field_name'], 'View_label')
        self.assertEqual(r.context['fields'][1]['field_label'], 'Label')
        self.assertEqual(r.context['fields'][1]['field_help'], view_label_help)
        self.assertEqual(r.context['fields'][1]['field_placeholder'], "(view label)")
        self.assertEqual(r.context['fields'][1]['field_property_uri'], "rdfs:label")
        self.assertEqual(r.context['fields'][1]['field_render_view'], "field/annalist_view_text.html")
        self.assertEqual(r.context['fields'][1]['field_render_edit'], "field/annalist_edit_text.html")
        self.assertEqual(r.context['fields'][1]['field_placement'].field, "small-12 columns")
        self.assertEqual(r.context['fields'][1]['field_value_type'], "annal:Text")
        self.assertEqual(r.context['fields'][1]['field_value'], view_label)
        self.assertEqual(r.context['fields'][1]['options'], self.no_options)
        # 3rd field - comment
        view_comment_help = (
            "Descriptive text about the record view.  "+
            "This may be used as help or tooltip text in appropriate contexts."
            )
        view_comment_placeholder = (
            "(description of record view)"
            )
        self.assertEqual(r.context['fields'][2]['field_id'], 'View_comment')
        self.assertEqual(r.context['fields'][2]['field_name'], 'View_comment')
        self.assertEqual(r.context['fields'][2]['field_label'], 'Help')
        self.assertEqual(r.context['fields'][2]['field_help'], view_comment_help)
        self.assertEqual(r.context['fields'][2]['field_placeholder'], view_comment_placeholder)
        self.assertEqual(r.context['fields'][2]['field_property_uri'], "rdfs:comment")
        self.assertEqual(r.context['fields'][2]['field_render_view'],   "field/annalist_view_textarea.html")
        self.assertEqual(r.context['fields'][2]['field_render_edit'],   "field/annalist_edit_textarea.html")
        self.assertEqual(r.context['fields'][2]['field_placement'].field, "small-12 columns")
        self.assertEqual(r.context['fields'][2]['field_value_type'], "annal:Longtext")
        self.assertEqual(r.context['fields'][2]['field_value'], view_help)
        self.assertEqual(r.context['fields'][2]['options'], self.no_options)
        # @@TODO - more...
        return

    #   -----------------------------------------------------------------------------
    #   Form rendering tests
    #   -----------------------------------------------------------------------------

    def test_get_form_rendering(self):
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        r = self.client.get(u+"?continuation_uri=/xyzzy/")
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        # log.info(r.content)
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>'_view' data in collection 'testcoll'</h3>")
        formrow1 = """
            <div class="small-12 medium-6 columns">
                <div class="row">
                    <div class="view_label small-12 medium-4 columns">
                        <p>Id</p>
                    </div>
                    <div class="small-12 medium-8 columns">
                        <input type="text" size="64" name="entity_id" value="00000001"/>
                    </div>
                </div>
            </div>
            """
        formrow2 = """
            <div class="small-12 columns">
                <div class="row">
                    <div class="view_label small-12 medium-2 columns">
                        <p>Label</p>
                    </div>
                    <div class="small-12 medium-10 columns">
                        <input type="text" size="64" name="View_label" 
                               value="Entity &#39;00000001&#39; of type &#39;_view&#39; in collection &#39;testcoll&#39;"/>
                    </div>
                </div>
            </div>
            """
        formrow3 = """
            <div class="small-12 columns">
                <div class="row">
                    <div class="view_label small-12 medium-2 columns">
                        <p>Help</p>
                    </div>
                    <div class="small-12 medium-10 columns">
                                <textarea cols="64" rows="6" name="View_comment" class="small-rows-4 medium-rows-8"></textarea>
                    </div>
                </div>
            </div>
            """
        # @@TODO: more .....
        self.assertContains(r, formrow1, html=True)
        self.assertContains(r, formrow2, html=True)
        self.assertContains(r, formrow3, html=True)
        return

    def test_get_new(self):
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        r = self.client.get(u+"?continuation_uri=/xyzzy/")
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        # Test context
        view_uri = entity_uri(type_id="_view", entity_id="00000001")
        self.assertEqual(r.context['title'],            site_title())
        self.assertEqual(r.context['coll_id'],          "testcoll")
        self.assertEqual(r.context['type_id'],          "_view")
        self.assertEqual(r.context['entity_id'],        "00000001")
        self.assertEqual(r.context['orig_id'],          "00000001")
        self.assertEqual(r.context['entity_uri'],       TestHostUri + view_uri)
        self.assertEqual(r.context['action'],           "new")
        self.assertEqual(r.context['continuation_uri'], "/xyzzy/")
        # Fields
        self._check_context_fields(r, 
            view_id="00000001",
            view_label="Entity '00000001' of type '_view' in collection 'testcoll'",
            view_help="",
            view_uri=TestHostUri + recordview_uri("testcoll", "00000001")
            )
        return

    def test_get_copy(self):
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.get(u)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        # Test context (values read from test data fixture)
        self.assertEqual(r.context['title'],            site_title())
        self.assertEqual(r.context['coll_id'],          "testcoll")
        self.assertEqual(r.context['type_id'],          "_view")
        self.assertEqual(r.context['entity_id'],        "Default_view")
        self.assertEqual(r.context['orig_id'],          "Default_view")
        self.assertEqual(r.context['entity_uri'],       "annal:view/Default_view")
        self.assertEqual(r.context['action'],           "copy")
        self.assertEqual(r.context['continuation_uri'], "")
        # Fields
        self._check_context_fields(r, 
            view_id="Default_view",
            view_label="Default record view",
            view_help="Default record view, applied when no view is specified when creating a record.",
            view_uri="annal:view/Default_view"
            )
        return

    def test_get_copy_not_exists(self):
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="notype", view_id="RecordView_view")
        r = self.client.get(u)
        # log.info(r.content)
        self.assertEqual(r.status_code,   404)
        self.assertEqual(r.reason_phrase, "Not found")
        self.assertContains(r, "<title>Annalist error</title>", status_code=404)
        self.assertContains(r, "<h3>404: Not found</h3>", status_code=404)
        self.assertContains(r, "<p>Entity &#39;notype&#39; of type &#39;_view&#39; in collection &#39;testcoll&#39; does not exist</p>", status_code=404)
        return

    def test_get_edit(self):
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.get(u)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        # Test context (values read from test data fixture)
        self.assertEqual(r.context['title'],            site_title())
        self.assertEqual(r.context['coll_id'],          "testcoll")
        self.assertEqual(r.context['type_id'],          "_view")
        self.assertEqual(r.context['entity_id'],        "Default_view")
        self.assertEqual(r.context['orig_id'],          "Default_view")
        self.assertEqual(r.context['entity_uri'],       "annal:view/Default_view") # @@TODO: is this right?
        self.assertEqual(r.context['action'],           "edit")
        self.assertEqual(r.context['continuation_uri'], "")
        # Fields
        self._check_context_fields(r, 
            view_id="Default_view",
            view_label="Default record view",
            view_help="Default record view, applied when no view is specified when creating a record.",
            view_uri="annal:view/Default_view"
            )
        return

    def test_get_edit_not_exists(self):
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="notype", view_id="RecordView_view")
        r = self.client.get(u)
        # log.info(r.content)
        self.assertEqual(r.status_code,   404)
        self.assertEqual(r.reason_phrase, "Not found")
        self.assertContains(r, "<title>Annalist error</title>", status_code=404)
        self.assertContains(r, "<h3>404: Not found</h3>", status_code=404)
        self.assertContains(r, "<p>Entity &#39;notype&#39; of type &#39;_view&#39; in collection &#39;testcoll&#39; does not exist</p>", status_code=404)
        return

    #   -----------------------------------------------------------------------------
    #   Form response tests
    #   -----------------------------------------------------------------------------

    #   -------- new type --------

    def test_post_new_view(self):
        self.assertFalse(RecordView.exists(self.testcoll, "newtype"))
        f = recordview_entity_view_form_data(view_id="newtype", action="new", update="RecordView")
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        # print r.content
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that new record type exists
        self._check_record_view_values("newtype", update="RecordView")
        return

    def test_post_new_view_cancel(self):
        self.assertFalse(RecordView.exists(self.testcoll, "newtype"))
        f = recordview_entity_view_form_data(
            view_id="newtype", action="new", cancel="Cancel", update="Updated RecordView"
            )
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that new record type still does not exist
        self.assertFalse(RecordView.exists(self.testcoll, "newtype"))
        return

    def test_post_new_view_missing_id(self):
        f = recordview_entity_view_form_data(action="new", update="RecordView")
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        # log.info("u %s, f %r"%(u,f))
        r = self.client.post(u, f)
        # print r.content
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        # Test context
        expect_context = recordview_entity_view_context_data(action="new", update="RecordView")
        self.assertDictionaryMatch(r.context, expect_context)
        return

    def test_post_new_view_invalid_id(self):
        f = recordview_entity_view_form_data(
            view_id="!badtype", orig_id="orig_view_id", action="new", update="RecordView"
            )
        u = entitydata_edit_uri("new", "testcoll", "_view", view_id="RecordView_view")
        # log.info("u %s, f %r"%(u,f))
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        # Test context
        expect_context = recordview_entity_view_context_data(
            view_id="!badtype", orig_id="orig_view_id", action="new", update="RecordView"
            )
        self.assertDictionaryMatch(r.context, expect_context)
        return

    #   -------- copy type --------

    def test_post_copy_view(self):
        self.assertFalse(RecordView.exists(self.testcoll, "copytype"))
        f = recordview_entity_view_form_data(
            view_id="copytype", orig_id="Default_view", action="copy", update="RecordView"
            )
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that new record type exists
        self._check_record_view_values("copytype", update="RecordView")
        return

    def test_post_copy_view_cancel(self):
        self.assertFalse(RecordView.exists(self.testcoll, "copytype"))
        f = recordview_entity_view_form_data(
            view_id="copytype", orig_id="Default_view", action="copy", cancel="Cancel", update="RecordView"
            )
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that target record view still does not exist
        self.assertFalse(RecordView.exists(self.testcoll, "copytype"))
        return

    def test_post_copy_view_missing_id(self):
        f = recordview_entity_view_form_data(
            action="copy", update="Updated RecordView"
            )
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        expect_context = recordview_entity_view_context_data(action="copy", update="Updated RecordView")
        self.assertDictionaryMatch(r.context, expect_context)
        return

    def test_post_copy_view_invalid_id(self):
        f = recordview_entity_view_form_data(
            view_id="!badtype", orig_id="Default_view", action="copy", update="Updated RecordView"
            )
        u = entitydata_edit_uri("copy", "testcoll", "_view", entity_id="Default_view", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        expect_context = recordview_entity_view_context_data(
            view_id="!badtype", orig_id="Default_view", 
            action="copy", update="Updated RecordView"
            )
        self.assertDictionaryMatch(r.context, expect_context)
        return

    #   -------- edit type --------

    def test_post_edit_view(self):
        self._create_record_view("edittype")
        self._check_record_view_values("edittype")
        f = recordview_entity_view_form_data(
            view_id="edittype", orig_id="edittype", 
            action="edit", update="Updated RecordView"
            )
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="edittype", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that new record type exists
        self._check_record_view_values("edittype", update="Updated RecordView")
        return

    def test_post_edit_view_new_id(self):
        self._create_record_view("editview1")
        self._check_record_view_values("editview1")
        f = recordview_entity_view_form_data(
            view_id="editview2", orig_id="editview1", 
            action="edit", update="Updated RecordView"
            )
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="editview1", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that new record type exists and old does not
        self.assertFalse(RecordView.exists(self.testcoll, "editview1"))
        self._check_record_view_values("editview2", update="Updated RecordView")
        return

    def test_post_edit_view_cancel(self):
        self._create_record_view("edittype")
        self._check_record_view_values("edittype")
        f = recordview_entity_view_form_data(
            view_id="edittype", orig_id="edittype", 
            action="edit", cancel="Cancel", update="Updated RecordView"
            )
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="edittype", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   302)
        self.assertEqual(r.reason_phrase, "FOUND")
        self.assertEqual(r.content,       "")
        self.assertEqual(r['location'], self.continuation_uri)
        # Check that target record type still does not exist and unchanged
        self._check_record_view_values("edittype")
        return

    def test_post_edit_view_missing_id(self):
        self._create_record_view("edittype")
        self._check_record_view_values("edittype")
        # Form post with ID missing
        f = recordview_entity_view_form_data(
            action="edit", update="Updated RecordView"
            )
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="edittype", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        # Test context for re-rendered form
        expect_context = recordview_entity_view_context_data(action="edit", update="Updated RecordView")
        self.assertDictionaryMatch(r.context, expect_context)
        # Check original data is unchanged
        self._check_record_view_values("edittype")
        return

    def test_post_edit_view_invalid_id(self):
        self._create_record_view("edittype")
        self._check_record_view_values("edittype")
        # Form post with invalid ID
        f = recordview_entity_view_form_data(
            view_id="!badtype", orig_id="edittype", action="edit", update="Updated RecordView"
            )
        u = entitydata_edit_uri("edit", "testcoll", "_view", entity_id="edittype", view_id="RecordView_view")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,   200)
        self.assertEqual(r.reason_phrase, "OK")
        self.assertContains(r, site_title("<title>%s</title>"))
        self.assertContains(r, "<h3>Problem with record view identifier</h3>")
        # Test context
        expect_context = recordview_entity_view_context_data(
            view_id="!badtype", orig_id="edittype", 
            action="edit", update="Updated RecordView"
            )
        self.assertDictionaryMatch(r.context, expect_context)
        # Check original data is unchanged
        self._check_record_view_values("edittype")
        return

#   -----------------------------------------------------------------------------
#
#   ConfirmRecordViewDeleteTests tests for completion of record deletion
#
#   -----------------------------------------------------------------------------

class ConfirmRecordViewDeleteTests(AnnalistTestCase):
    """
    Tests for record type deletion on response to confirmation form
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.testcoll = Collection.create(self.testsite, "testcoll", collection_create_values("testcoll"))
        self.user = User.objects.create_user('testuser', 'user@test.example.com', 'testpassword')
        self.user.save()
        self.client = Client(HTTP_HOST=TestHost)
        loggedin = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(loggedin)
        return

    def tearDown(self):
        return

    def test_CollectionActionViewTest(self):
        self.assertEqual(RecordViewDeleteConfirmedView.__name__, "RecordViewDeleteConfirmedView", "Check RecordViewDeleteConfirmedView class name")
        return

    # NOTE:  test_collection checks the appropriate response from clicking the delete button, 
    # so here only need to test completion code.
    def test_post_confirmed_remove_view(self):
        t = RecordView.create(self.testcoll, "deleteview", recordview_create_values("deleteview"))
        self.assertTrue(RecordView.exists(self.testcoll, "deleteview"))
        # Submit positive confirmation
        u = TestHostUri + recordview_edit_uri("delete", "testcoll")
        f = recordview_delete_confirm_form_data("deleteview")
        r = self.client.post(u, f)
        self.assertEqual(r.status_code,     302)
        self.assertEqual(r.reason_phrase,   "FOUND")
        self.assertEqual(r.content,         "")
        self.assertMatch(r['location'],    
            "^"+TestHostUri+
            collection_edit_uri("testcoll")+
            r"\?info_head=.*&info_message=.*deleteview.*testcoll.*$"
            )
        # Confirm deletion
        self.assertFalse(RecordView.exists(self.testcoll, "deleteview"))
        return

# End.
