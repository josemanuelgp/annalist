"""
Tests for collection module
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import unittest

import logging
log = logging.getLogger(__name__)

from django.conf                import settings
from django.db                  import models
from django.http                import QueryDict
from django.contrib.auth.models import User
from django.test                import TestCase # cf. https://docs.djangoproject.com/en/dev/topics/testing/tools/#assertions
from django.test.client         import Client

from bs4                        import BeautifulSoup

from miscutils.MockHttpResources import MockHttpFileResources, MockHttpDictResources

from annalist.identifiers       import ANNAL
from annalist                   import layout
from annalist.site              import Site
from annalist.collection        import Collection # , CollectionView

from tests                      import TestBaseUri, TestBaseDir, dict_to_str, init_annalist_test_site
from AnnalistTestCase           import AnnalistTestCase

# Test assertion summary from http://docs.python.org/2/library/unittest.html#test-cases
#
# Method                    Checks that             New in
# assertEqual(a, b)         a == b   
# assertNotEqual(a, b)      a != b   
# assertTrue(x)             bool(x) is True  
# assertFalse(x)            bool(x) is False     
# assertIs(a, b)            a is b                  2.7
# assertIsNot(a, b)         a is not b              2.7
# assertIsNone(x)           x is None               2.7
# assertIsNotNone(x)        x is not None           2.7
# assertIn(a, b)            a in b                  2.7
# assertNotIn(a, b)         a not in b              2.7
# assertIsInstance(a, b)    isinstance(a, b)        2.7
# assertNotIsInstance(a, b) not isinstance(a, b)    2.7

class CollectionTest(TestCase):
    """
    Tests for Site object interface
    """

    def setUp(self):
        init_annalist_test_site()
        self.testsite = Site(TestBaseUri, TestBaseDir)
        self.testcoll = Collection(self.testsite, "testcoll")
        self.coll1 = (
            { '@id': '../'
            , 'id': 'coll1'
            , 'type': 'annal:Collection'
            , 'title': 'Name collection coll1'
            , 'uri': 'http://example.com/testsite/coll1/'
            , 'annal:id': 'coll1'
            , 'annal:type': 'annal:Collection'
            , 'rdfs:comment': 'Annalist collection metadata.'
            , 'rdfs:label': 'Name collection coll1'
            })
        self.testcoll_add = (
            { 'rdfs:comment': 'Annalist collection metadata.'
            , 'rdfs:label': 'Name collection testcoll'
            })
        self.type1_add = (
            { 'rdfs:comment': 'Annalist collection1 recordtype1'
            , 'rdfs:label': 'Type testcoll/type1'
            })      
        self.type1 = (
            { '@id': './'
            , 'id': 'type1'
            , 'type': 'annal:RecordType'
            , 'title': 'Type testcoll/type1'
            , 'uri': 'http://example.com/testsite/testcoll/types/type1/'
            , 'annal:id': 'type1'
            , 'annal:type': 'annal:RecordType'
            , 'rdfs:comment': 'Annalist collection1 recordtype1'
            , 'rdfs:label': 'Type testcoll/type1'
            })      
        self.type2_add = (
            { 'rdfs:comment': 'Annalist collection1 recordtype2'
            , 'rdfs:label': 'Type testcoll/type2'
            })      
        self.type2 = (
            { '@id': './'
            , 'id': 'type2'
            , 'type': 'annal:RecordType'
            , 'title': 'Type testcoll/type2'
            , 'uri': 'http://example.com/testsite/testcoll/types/type2/'
            , 'annal:id': 'type2'
            , 'annal:type': 'annal:RecordType'
            , 'rdfs:comment': 'Annalist collection1 recordtype2'
            , 'rdfs:label': 'Type testcoll/type2'
            })      
        return

    def tearDown(self):
        return

    def test_CollectionTest(self):
        self.assertEqual(Collection.__name__, "Collection", "Check Collection class name")
        return

    def test_collection_init(self):
        s = Site(TestBaseUri, TestBaseDir)
        self.assertEqual(s._entitytype,     ANNAL.CURIE.Site)
        self.assertEqual(s._entityfile,     layout.SITE_META_FILE)
        self.assertEqual(s._entityref,      layout.META_SITE_REF)
        self.assertEqual(s._entityid,       None)
        self.assertEqual(s._entityuri,      TestBaseUri+"/")
        self.assertEqual(s._entitydir,      TestBaseDir+"/")
        self.assertEqual(s._values,         None)
        return

    def test_collection_data(self):
        sd = self.testsite.site_data()
        self.assertEquals(set(sd.keys()),set(('rdfs:label', 'rdfs:comment', 'collections', 'title')))
        self.assertEquals(sd["title"],        "Annalist data journal test site")
        self.assertEquals(sd["rdfs:label"],   "Annalist data journal test site")
        self.assertEquals(sd["rdfs:comment"], "Annalist site metadata.")
        self.assertEquals(sd["collections"].keys(),  ["coll1","coll2","coll3"])
        self.assertEquals(set(sd["collections"]["coll1"].keys()),  set(self.coll1.keys()))
        self.assertEquals(dict_to_str(sd["collections"]["coll1"]),  self.coll1)
        return

    # def test_collections_dict(self):
    #     colls = self.testsite.collections_dict()
    #     self.assertEquals(colls.keys(),["coll1","coll2","coll3"])
    #     self.assertEquals(dict_to_str(colls["coll1"]),  self.coll1)
    #     return

    def test_add_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        typenames = { t.get_id() for t in self.testcoll.types() }
        self.assertEqual(typenames, set())
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        typenames = { t.get_id() for t in self.testcoll.types() }
        self.assertEqual(typenames, {"type1", "type2"})
        return

    def test_get_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        self.assertEqual(self.testcoll.get_type("type1").get_values(), self.type1)
        self.assertEqual(self.testcoll.get_type("type2").get_values(), self.type2)
        return

    def test_remove_type(self):
        self.testsite.add_collection("testcoll", self.testcoll_add)
        t1 = self.testcoll.add_type("type1", self.type1_add)
        t2 = self.testcoll.add_type("type2", self.type2_add)
        typenames =  set([ t.get_id() for t in self.testcoll.types()])
        self.assertEqual(typenames, {"type1", "type2"})
        self.testcoll.remove_type("type1")
        typenames =  set([ t.get_id() for t in self.testcoll.types()])
        self.assertEqual(typenames, {"type2"})
        return

    # @@TODO:
    #   views
    #   lists

# class CollectionViewTest(AnnalistTestCase):
#     """
#     Tests for Site views
#     """

#     def setUp(self):
#         init_annalist_test_site()
#         self.testsite = Site("http://example.com/testsite", TestBaseDir)
#         self.user = User.objects.create_user('testuser', 'user@test.example.com', 'testpassword')
#         self.user.save()
#         return

#     def tearDown(self):
#         return

#     def test_CollectionViewTest(self):
#         self.assertEqual(CollectionView.__name__, "CollectionView", "Check CollectionView class name")
#         return

#     def test_get(self):
#         # @@TODO: use reference to self.client, per 
#         # https://docs.djangoproject.com/en/dev/topics/testing/tools/#default-test-client
#         c = Client()
#         r = c.get("/annalist/site/")
#         self.assertEqual(r.status_code,   200)
#         self.assertEqual(r.reason_phrase, "OK")
#         self.assertContains(r, "<title>Annalist data journal test site</title>")
#         return

#     def test_get_no_login(self):
#         c = Client()
#         r = c.get("/annalist/site/")
#         self.assertFalse(r.context["auth_create"])
#         self.assertFalse(r.context["auth_update"])
#         self.assertFalse(r.context["auth_delete"])
#         colls = r.context['collections']
#         self.assertEqual(len(colls), 3)
#         for id in init_collections:
#             self.assertEqual(colls[id]["annal:id"], id)
#             self.assertEqual(colls[id]["uri"],      init_collections[id]["uri"])
#             self.assertEqual(colls[id]["title"],    init_collections[id]["title"])
#         # Check returned HTML (checks template logic)
#         # (Don't need to keep doing this as logic can be tested through context as above)
#         # (See: http://stackoverflow.com/questions/2257958/)
#         s = BeautifulSoup(r.content)
#         self.assertEqual(s.html.title.string, "Annalist data journal test site")
#         homelink = s.find(class_="title-area").find(class_="name").h1.a
#         self.assertEqual(homelink.string,   "Home")
#         self.assertEqual(homelink['href'],  "/annalist/site/")
#         menuitems = s.find(class_="top-bar-section").find(class_="right").find_all("li")
#         self.assertEqual(menuitems[0].a.string,  "Login")
#         self.assertEqual(menuitems[0].a['href'], "/annalist/profile/")
#         # print "*****"
#         # #print s.table.tbody.prettify()
#         # print s.table.tbody.find_all("tr")
#         # print "*****"
#         trows = s.form.find_all("div", class_="row")
#         self.assertEqual(len(trows), 4)
#         self.assertEqual(trows[1].div.p.a.string,  "coll1")
#         self.assertEqual(trows[1].div.p.a['href'], "/annalist/coll1/")
#         self.assertEqual(trows[2].div.p.a.string,  "coll2")
#         self.assertEqual(trows[2].div.p.a['href'], "/annalist/coll2/")
#         self.assertEqual(trows[3].div.p.a.string,  "coll3")
#         self.assertEqual(trows[3].div.p.a['href'], "/annalist/coll3/")
#         return

#     def test_get_with_login(self):
#         c = Client()
#         loggedin = c.login(username="testuser", password="testpassword")
#         self.assertTrue(loggedin)
#         r = c.get("/annalist/site/")
#         # Preferred way to test main view logic
#         self.assertTrue(r.context["auth_create"])
#         self.assertTrue(r.context["auth_update"])
#         self.assertTrue(r.context["auth_delete"])
#         colls = r.context['collections']
#         self.assertEqual(len(colls), 3)
#         for id in init_collections:
#             self.assertEqual(colls[id]["annal:id"], id)
#             self.assertEqual(colls[id]["uri"],      init_collections[id]["uri"])
#             self.assertEqual(colls[id]["title"],    init_collections[id]["title"])
#         # Check returned HTML (checks template logic)
#         # (Don't need to keep doing this as logic can be tested through context as above)
#         # (See: http://stackoverflow.com/questions/2257958/)
#         s = BeautifulSoup(r.content)
#         # title and top menu
#         self.assertEqual(s.html.title.string, "Annalist data journal test site")
#         homelink = s.find(class_="title-area").find(class_="name").h1.a
#         self.assertEqual(homelink.string,   "Home")
#         self.assertEqual(homelink['href'],  "/annalist/site/")
#         menuitems = s.find(class_="top-bar-section").find(class_="right").find_all("li")
#         self.assertEqual(menuitems[0].a.string,  "Profile")
#         self.assertEqual(menuitems[0].a['href'], "/annalist/profile/")
#         self.assertEqual(menuitems[1].a.string,  "Logout")
#         self.assertEqual(menuitems[1].a['href'], "/annalist/logout/")
#         # Displayed colllections and check-buttons
#         trows = s.form.find_all("div", class_="row")
#         self.assertEqual(len(trows), 6)
#         tcols1 = trows[1].find_all("div")
#         self.assertEqual(tcols1[0].a.string,       "coll1")
#         self.assertEqual(tcols1[0].a['href'],      "/annalist/coll1/")
#         self.assertEqual(tcols1[2].input['type'],  "checkbox")
#         self.assertEqual(tcols1[2].input['name'],  "select")
#         self.assertEqual(tcols1[2].input['value'], "coll1")
#         tcols2 = trows[2].find_all("div")
#         self.assertEqual(tcols2[0].a.string,       "coll2")
#         self.assertEqual(tcols2[0].a['href'],      "/annalist/coll2/")
#         self.assertEqual(tcols2[2].input['type'],  "checkbox")
#         self.assertEqual(tcols2[2].input['name'],  "select")
#         self.assertEqual(tcols2[2].input['value'], "coll2")
#         tcols3 = trows[3].find_all("div")
#         self.assertEqual(tcols3[0].a.string,       "coll3")
#         self.assertEqual(tcols3[0].a['href'],      "/annalist/coll3/")
#         self.assertEqual(tcols3[2].input['type'],  "checkbox")
#         self.assertEqual(tcols3[2].input['name'],  "select")
#         self.assertEqual(tcols3[2].input['value'], "coll3")
#         # Remove/new collection buttons
#         btn_remove = trows[4].find("div", class_="right")
#         self.assertEqual(btn_remove.input["type"],  "submit")
#         self.assertEqual(btn_remove.input["name"],  "remove")
#         # print "**********"
#         # print trows[5].prettify()
#         # print "**********"
#         field_id = trows[5].find_all("div")[0]
#         self.assertEqual(field_id.input["type"],  "text")
#         self.assertEqual(field_id.input["name"],  "new_id")
#         field_id = trows[5].find_all("div")[1]
#         self.assertEqual(field_id.input["type"],  "text")
#         self.assertEqual(field_id.input["name"],  "new_label")
#         btn_new = trows[5].find_all("div")[2]
#         self.assertEqual(btn_new.input["type"],  "submit")
#         self.assertEqual(btn_new.input["name"],  "new")
#         return

#     def test_post_add_type(self):
#         c = Client()
#         loggedin = c.login(username="testuser", password="testpassword")
#         self.assertTrue(loggedin)
#         form_data = (
#             { "new":        "New collection"
#             , "new_id":     "testnew"
#             , "new_label":  "Label for new collection"
#             })
#         r = c.post("/annalist/site/", form_data)
#         self.assertEqual(r.status_code,   302)
#         self.assertEqual(r.reason_phrase, "FOUND")
#         self.assertEqual(r.content,       "")
#         self.assertEqual(r['location'],
#             "http://testserver/annalist/site/"+
#             "?info_head=Action%20completed"+
#             "&info_message=Created%20new%20collection:%20'testnew'")
#         # Check site now has new colllection
#         r = c.get("/annalist/site/")
#         new_collections = init_collections.copy()
#         new_collections["testnew"] = (
#             { 'title': 'Label for new collection'
#             , 'uri':   '/annalist/testnew/'
#             })
#         colls = r.context['collections']
#         for id in new_collections:
#             self.assertEqual(colls[id]["annal:id"], id)
#             self.assertEqual(colls[id]["uri"],      new_collections[id]["uri"])
#             self.assertEqual(colls[id]["title"],    new_collections[id]["title"])
#         return

#     def test_post_remove_type(self):
#         c = Client()
#         loggedin = c.login(username="testuser", password="testpassword")
#         self.assertTrue(loggedin)
#         form_data = (
#             { "remove":     "Remove selected"
#             , "new_id":     ""
#             , "new_label":  ""
#             , "select":     ["coll1", "coll3"]
#             })
#         r = c.post("/annalist/site/", form_data)
#         self.assertEqual(r.status_code,   200)
#         self.assertEqual(r.reason_phrase, "OK")
#         self.assertTemplateUsed(r, "annalist_confirm.html")
#         # print "********"
#         # # print repr(r.__dict__)
#         # # print repr(r.context)
#         # print r.content
#         # print "********"
#         # Returns confirmation form: check
#         self.assertContains(r, """<form method="POST" action="/annalist/confirm/">""", status_code=200)
#         self.assertContains(r, """<input type="submit" name="confirm" value="Confirm"/>""", html=True)
#         self.assertContains(r, """<input type="submit" name="cancel" value="Cancel"/>""", html=True)
#         self.assertContains(r, """<input type="hidden" name="complete_action" value="/annalist/site_action/"/>""", html=True)
#         self.assertContains(r, """<input type="hidden" name="action_params"   value="{&quot;new_label&quot;: [&quot;&quot;], &quot;new_id&quot;: [&quot;&quot;], &quot;select&quot;: [&quot;coll1&quot;, &quot;coll3&quot;], &quot;remove&quot;: [&quot;Remove selected&quot;]}"/>""", html=True)
#         self.assertContains(r, """<input type="hidden" name="cancel_action"   value="/annalist/site/"/>""", html=True)
#         return

# class CollectionActionView(AnnalistTestCase):
#     """
#     Tests for Site action views (completion of confirmed actions
#     requested from the site view)
#     """

#     def setUp(self):
#         init_annalist_test_site()
#         self.testsite = Site("http://example.com/testsite", TestBaseDir)
#         self.user = User.objects.create_user('testuser', 'user@test.example.com', 'testpassword')
#         self.user.save()
#         return

#     def tearDown(self):
#         return

#     def test_CollectionActionViewTest(self):
#         self.assertEqual(CollectionActionView.__name__, "CollectionActionView", "Check CollectionActionView class name")
#         return

#     def test_post_confirmed_remove_type(self):
#         c = Client()
#         loggedin = c.login(username="testuser", password="testpassword")
#         self.assertTrue(loggedin)
#         # Submit positive confirmation
#         conf_data = (
#             { "confirm":          "Confirm"
#             , "complete_action":  "/annalist/site_action/"
#             , "action_params":    """{"new_label": [""], "new_id": [""], "select": ["coll1", "coll3"], "remove": ["Remove selected"]}"""
#             , "cancel_action":    "/annalist/site/"
#             })
#         r = c.post("/annalist/confirm/", conf_data)
#         self.assertEqual(r.status_code,     302)
#         self.assertEqual(r.reason_phrase,   "FOUND")
#         self.assertEqual(r.content,         "")
#         self.assertMatch(r['location'],     r"^http://testserver/annalist/site/\?info_head=.*&info_message=.*coll1,.*coll3.*$")
#         # Confirm collections deleted
#         r = c.get("/annalist/site/")
#         colls = r.context['collections']
#         self.assertEqual(len(colls), 1)
#         id = "coll2"
#         self.assertEqual(colls[id]["annal:id"], id)
#         self.assertEqual(colls[id]["uri"],      init_collections[id]["uri"])
#         self.assertEqual(colls[id]["title"],    init_collections[id]["title"])
#         return
 
#     def test_post_cancelled_remove_type(self):
#         c = Client()
#         loggedin = c.login(username="testuser", password="testpassword")
#         self.assertTrue(loggedin)
#         # Cancel in confirmation form response
#         conf_data = (
#             { "cancel":           "Cancel"
#             , "complete_action":  "/annalist/site_action/"
#             , "action_params":    """{"new_label": [""], "new_id": [""], "select": ["coll1", "coll3"], "remove": ["Remove selected"]}"""
#             , "cancel_action":    "/annalist/site/"
#             })
#         r = c.post("/annalist/confirm/", conf_data)
#         self.assertEqual(r.status_code,     302)
#         self.assertEqual(r.reason_phrase,   "FOUND")
#         self.assertEqual(r.content,         "")
#         self.assertEqual(r['location'],     "http://testserver/annalist/site/")
#         # Confirm no collections deleted
#         r = c.get("/annalist/site/")
#         colls = r.context['collections']
#         self.assertEqual(len(colls), 3)
#         for id in init_collections:
#             self.assertEqual(colls[id]["annal:id"], id)
#             self.assertEqual(colls[id]["uri"],      init_collections[id]["uri"])
#             self.assertEqual(colls[id]["title"],    init_collections[id]["title"])
#         return

# End.