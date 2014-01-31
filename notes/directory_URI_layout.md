
Annalist directory layout
-------------------------

See settings.py

Questions:

* Primary type or multiple types for each entity?
* How to represent groups within a collection?  Just use multiple associations in a record?


Annalist URI structure
----------------------

@@NOTE: needs review in light of code; or just fold into code and delete this.

*   $ANNALIST_ROOT/
 
    Presents list of collections and option to create new.  Formats: HTML (form) or JSON-LD.  POST form-data (or JSON-LD?) to create new collection.

    *   $COLLECTION_ID/

        Presents default view for collection, based on defaults)  Formats HTML (form) or JSON-LD.  POST form-data (or JSON-LD?) to change defaults.

        *   _annalist_config/
            * (collection config)
            * records/
                * record-type
                *  :
            * views/
                * view-type
                *  :
            * lists/
                * list-type
                *  :
        * record-type/
            * record-id
            *  :
        *  :
    *    : (repeat for each collection)