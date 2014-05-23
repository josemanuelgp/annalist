"""
Record field data functions to support entity data testing
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os
import urlparse

import logging
log = logging.getLogger(__name__)

from django.conf                    import settings
from django.http                    import QueryDict
from django.utils.http              import urlquote, urlunquote
from django.core.urlresolvers       import resolve, reverse

from annalist.util                  import valid_id
from annalist.identifiers           import RDF, RDFS, ANNAL
from annalist                       import layout
from annalist.fields.render_utils   import get_placement_classes

from tests                          import (
    TestHost, TestHostUri, TestBasePath, TestBaseUri, TestBaseDir
    )
from entity_testutils               import (
    collection_dir, 
    site_title
    )
from entity_testentitydata          import (
    entitydata_list_type_uri
    )

#   -----------------------------------------------------------------------------
#
#   Directory generating functions
#
#   -----------------------------------------------------------------------------

def recordfield_dir(coll_id="testcoll", field_id="testfield"):
    return collection_dir(coll_id) + layout.COLL_FIELD_PATH%{'id': field_id} + "/"

#   -----------------------------------------------------------------------------
#
#   URI generating functions
#
#   -----------------------------------------------------------------------------

#   These use the Django `reverse` function so they correspond to
#   the declared URI patterns.

def recordfield_site_uri(site, field_id="testfield"):
    return site._entityuri + layout.SITE_FIELD_PATH%{'id': field_id} + "/"

def recordfield_coll_uri(site, coll_id="testcoll", field_id="testfield"):
    return site._entityuri + layout.SITE_COLL_PATH%{'id': coll_id} + "/" + layout.COLL_FIELD_PATH%{'id': field_id} + "/"

def recordfield_uri(coll_id, field_id):
    """
    URI for record field description data; also view using default entity view
    """
    viewname = "AnnalistEntityAccessView"
    kwargs   = {'coll_id': coll_id, "type_id": "_field"}
    if valid_id(field_id):
        kwargs.update({'entity_id': field_id})
    else:
        kwargs.update({'entity_id': "___"})
    return reverse(viewname, kwargs=kwargs)

def recordfield_edit_uri(action=None, coll_id=None, field_id=None):
    """
    URI for record field description editing view
    """
    viewname = ( 
        'AnnalistEntityDataView'        if action == "view"   else
        'AnnalistEntityNewView'         if action == "new"    else
        'AnnalistEntityEditView'        if action == "copy"   else
        'AnnalistEntityEditView'        if action == "edit"   else
        'AnnalistRecordFieldDeleteView' if action == "delete" else
        'unknown'
        )
    kwargs = {'coll_id': coll_id, 'type_id': "_field", 'view_id': "Field_view"}
    if action != "delete":
        kwargs.update({'action': action})
    if field_id:
        if valid_id(field_id):
            kwargs.update({'entity_id': field_id})
        else:
            kwargs.update({'entity_id': "___"})
    return reverse(viewname, kwargs=kwargs)

#   -----------------------------------------------------------------------------
#
#   ----- RecordField data
#
#   -----------------------------------------------------------------------------

def recordfield_init_keys():
    return set(
        [ 'annal:id', 'annal:type'
        , 'annal:uri'
        , 'rdfs:label', 'rdfs:comment'
        ])

def recordfield_value_keys():
    return (recordfield_init_keys() |
        { 'annal:property_uri'
        , 'annal:value_type'
        , 'annal:field_render'
        , 'annal:placeholder'
        })

def recordfield_load_keys():
    return recordfield_value_keys() | {"@id"}

def recordfield_create_values(coll_id="testcoll", field_id="testfield", update="Field"):
    """
    Entity values used when creating a record type entity
    """
    return (
        { 'rdfs:label':     "%s %s/_field/%s"%(update, coll_id, field_id)
        , 'rdfs:comment':   "%s help for %s in collection %s"%(update, field_id, coll_id)
        })

def recordfield_values(
        coll_id="testcoll", field_id="testfield",
        update="Field", hosturi=TestHostUri):
    d = recordfield_create_values(coll_id, field_id, update=update).copy()
    d.update(
        { 'annal:id':       field_id
        , 'annal:type':     "annal:RecordField"
        , 'annal:uri':      hosturi + recordfield_uri(coll_id, field_id)
        })
    return d

def recordfield_read_values(
        coll_id="testcoll", field_id="testfield",
        update="Field", hosturi=TestHostUri):
    d = recordfield_values(coll_id, field_id, update=update, hosturi=hosturi).copy()
    d.update(
        { '@id':            "./"
        })
    return d

#   -----------------------------------------------------------------------------
#
#   ----- Entity data in recordfield view
#
#   -----------------------------------------------------------------------------

def recordfield_entity_view_context_data(
        field_id=None, orig_id=None, type_ids=[],
        action=None, update="Field"
    ):
    context_dict = (
        { 'title':              site_title()
        , 'coll_id':            'testcoll'
        , 'type_id':            '_field'
        , 'orig_id':            'orig_field_id'
        , 'fields':
          [ { 'field_label':        'Id'
            , 'field_id':           'Field_id'
            , 'field_name':         'entity_id'
            , 'field_render_view':  'field/annalist_view_entityref.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12;medium:0,6')
            , 'field_value_type':   'annal:Slug'
            # , 'field_value':      (Supplied separately)
            , 'options':            []
            }
          , { 'field_label':        'Field value type'
            , 'field_id':           'Field_type'
            , 'field_name':         'Field_type'
            , 'field_render_view':  'field/annalist_view_entityref.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12;medium:6,6right')
            , 'field_value_type':   'annal:RenderType'
            , 'field_value':        '(field value type)'
            , 'options':            []
            }
          , { 'field_label':        'Label'
            , 'field_id':           'Field_label'
            , 'field_name':         'Field_label'
            , 'field_render_view':  'field/annalist_view_text.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12')
            , 'field_value_type':   'annal:Text'
            , 'field_value':        '%s data ... (testcoll/_field)'%(update)
            , 'options':            []
            }
          , { 'field_label':        'Help'
            , 'field_id':           'Field_comment'
            , 'field_name':         'Field_comment'
            , 'field_render_view':  'field/annalist_view_textarea.html'
            , 'field_render_edit':  'field/annalist_edit_textarea.html'
            , 'field_placement':    get_placement_classes('small:0,12')
            , 'field_value_type':   'annal:Longtext'
            , 'field_value':        '%s description ... (testcoll/_field)'%(update)
            , 'options':            []
            }
          , { 'field_label':        'Placeholder'
            , 'field_id':           'Field_placeholder'
            , 'field_name':         'Field_placeholder'
            , 'field_render_view':  'field/annalist_view_text.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12')
            , 'field_value_type':   'annal:Text'
            , 'field_value':        '(placeholder text)'
            , 'options':            []
            }
          , { 'field_label':        'Property'
            , 'field_id':           'Field_property'
            , 'field_name':         'Field_property'
            , 'field_render_view':  'field/annalist_view_entityref.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12')
            , 'field_value_type':   'annal:Identifier'
            , 'field_value':        "(property URI or CURIE)"
            , 'options':            []
            }
          , { 'field_label':        'Size/position'
            , 'field_id':           'Field_placement'
            , 'field_name':         'Field_placement'
            , 'field_render_view':  'field/annalist_view_text.html'
            , 'field_render_edit':  'field/annalist_edit_text.html'
            , 'field_placement':    get_placement_classes('small:0,12')
            , 'field_value_type':   'annal:Placement'
            , 'field_value':        '(field display size and placement details)'
            , 'options':            []
            }
          ]
        , 'continuation_uri':   entitydata_list_type_uri("testcoll", "_field")
        })
    if field_id:
        context_dict['fields'][0]['field_value'] = field_id
        context_dict['fields'][2]['field_value'] = '%s testcoll/_field/%s'%(update,field_id)
        context_dict['fields'][3]['field_value'] = '%s help for %s in collection testcoll'%(update,field_id)
        # context_dict['fields'][5]['field_value'] = TestBaseUri + "/c/%s/d/%s/%s/"%("testcoll", "_field", field_id)
        context_dict['orig_id']     = field_id
    if orig_id:
        context_dict['orig_id']     = orig_id
    if action:  
        context_dict['action']      = action
    return context_dict

def recordfield_entity_view_form_data(
        field_id=None, orig_id=None, 
        coll_id="testcoll", 
        action=None, cancel=None, update="Field"):
    # log.info("recordfield_entity_view_form_data: field_id %s"%(field_id))
    form_data_dict = (
        { 'Field_label':        '%s data ... (%s/%s)'%(update, coll_id, "_field")
        , 'Field_comment':      '%s description ... (%s/%s)'%(update, coll_id, "_field")
        , 'orig_id':            'orig_field_id'
        , 'continuation_uri':   entitydata_list_type_uri(coll_id, "_field")
        })
    if field_id:
        form_data_dict['entity_id']     = field_id
        form_data_dict['Field_label']   = '%s %s/%s/%s'%(update, coll_id, "_field", field_id)
        form_data_dict['Field_comment'] = '%s help for %s in collection %s'%(update, field_id, coll_id)
        form_data_dict['Field_uri']     = TestBaseUri + "/c/%s/d/%s/%s/"%(coll_id, "_field", field_id)
        form_data_dict['orig_id']       = field_id
        form_data_dict['orig_type']     = "_field"
    if orig_id:
        form_data_dict['orig_id']       = orig_id
    if action:
        form_data_dict['action']        = action
    if cancel:
        form_data_dict['cancel']        = "Cancel"
    else:
        form_data_dict['save']          = 'Save'
    return form_data_dict

# End.
