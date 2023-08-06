import json
from pprint import pformat
from pprint import pprint
from greent.client import GraphQL
from collections import namedtuple
translator = GraphQL ("http://localhost:5000/graphql")

Translation = namedtuple ('Translation', [ 'thing', 'domain_a', 'domain_b' ])
translations = [
    Translation ("Imatinib",     "http://chem2bio2rdf.org/drugbank/resource/Generic_Name", "http://chem2bio2rdf.org/uniprot/resource/gene"),      # CBR
    Translation ("CDC25A",       "http://chem2bio2rdf.org/uniprot/resource/gene",          "http://chem2bio2rdf.org/kegg/resource/kegg_pathway"), # CBR
    Translation ("CACNA1A",      "http://chem2bio2rdf.org/uniprot/resource/gene",          "http://pharos.nih.gov/identifier/disease/name"),      # Pharos
    Translation ("Asthma",       "http://identifiers.org/mesh/disease/name",               "http://identifiers.org/mesh/drug/name")               # Chemotext

    Translation ("DOID:2841",    "http://identifiers.org/doid",                            "http://identifiers.org/mesh/disease/id"),             # DO
    Translation ("MESH:D001249", "http://identifiers.org/mesh",                            "http://identifiers.org/doi"),                         # OXO
]

for translation in translations:
    result = translator.translate (
        thing=translation.thing,
        domain_a=translation.domain_a,
        domain_b=translation.domain_b)
    pprint ("{0} => {1}".format (translation.thing, pformat (result)))
