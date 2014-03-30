# bib-fieldgen.sh

for fid in              \
    Bib_type            \
    Bib_title           \
    Bib_author          \
    Bib_editor          \
    Bib_month           \
    Bib_year            \
    Bib_url             \
    Bib_journal         \
    Bib_volume          \
    Bib_number          \
    Bib_pages           \
    Bib_booktitle       \
    Bib_chapter         \
    Bib_edition         \
    Bib_publisher       \
    Bib_address         \
    Bib_eprint          \
    Bib_howpublished    \
    Bib_institution     \
    Bib_organization    \
    Bib_school          
do

cat >${fid}.jsonld <<EOF
{ "@id":                "annal:fields/${fid}"
, "annal:id":           "${fid}"
, "annal:type":         "annal:Field"
, "rdfs:label":         "${fid}"
, "rdfs:comment":       "BibJSON(ish) field ${fid}"
, "annal:field_render": "annal:field_render/Text"
, "annal:value_type":   "annal:Text"
, "annal:placeholder":  "(${fid})"
, "annal:property_uri": "bib:${fid}"
}
EOF

done
