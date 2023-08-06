import json
import os
import unittest
from collections import defaultdict
from pprint import pformat
from pprint import pprint
from greent.client import GraphQL
from collections import namedtuple

class Vocab(object):
    root_kind         = 'http://identifiers.org/doi'
    
    # MESH
    mesh              = 'http://identifiers.org/mesh'
    mesh_disease_name = 'http://identifiers.org/mesh/disease/name'
    mesh_drug_name    = 'http://identifiers.org/mesh/drug/name'
    mesh_disease_id   = 'http://identifiers.org/mesh/disease/id'
    
    # Disease
    doid_curie          = "doid"
    doid                = "http://identifiers.org/doid"
    pharos_disease_name = "http://pharos.nih.gov/identifier/disease/name"
    
    # DRUG
    c2b2r_drug_name   = "http://chem2bio2rdf.org/drugbank/resource/Generic_Name"
    
    # TARGET
    c2b2r_gene        = "http://chem2bio2rdf.org/uniprot/resource/gene"
    
    # PATHWAY
    c2b2r_pathway     = "http://chem2bio2rdf.org/kegg/resource/kegg_pathway"
        
    # Semantic equivalence

    def __init__(self):
        self.equivalence = defaultdict(lambda: [])
        self.equivalence[self.doid_curie] = [ self.doid ]
        
        # https://github.com/prefixcommons/biocontext/blob/master/registry/uber_context.jsonld
        uber_context_path = os.path.join(os.path.dirname(__file__), 'jsonld', 'uber_context.jsonld')
        with open (uber_context_path, 'r') as stream:
            self.equivalence = json.loads (stream.read ())["@context"]
            self.equivalence["MESH"] = self.equivalence ["MESH.2013"]

class Translator(object):

    def __init__(self, core):
        self.core = core
        self.vocab = Vocab ()
        
        # Domain translation
        self.translator_router = defaultdict (lambda: defaultdict (lambda: NoTranslation ()))
        self.translator_router[Vocab.mesh_disease_name] = {
            Vocab.mesh_drug_name : lambda disease: self.chemotext.disease_name_to_drug_name (disease)
        }
        self.translator_router[Vocab.doid][Vocab.mesh_disease_id]             = lambda doid:    self.core.disease_ontology.doid_to_mesh (doid.upper())
        self.translator_router[Vocab.c2b2r_drug_name][Vocab.c2b2r_gene]       = lambda drug:    self.core.chembio_ks.drug_name_to_gene_symbol (drug)
        self.translator_router[Vocab.c2b2r_gene][Vocab.c2b2r_pathway]         = lambda gene:    self.core.chembio_ks.gene_symbol_to_pathway (gene)
        self.translator_router[Vocab.c2b2r_gene][Vocab.pharos_disease_name]   = lambda gene:    self.core.pharos.target_to_disease (gene)
        self.translator_router[Vocab.mesh][Vocab.root_kind]                   = lambda mesh_id: self.core.oxo.mesh_to_other (mesh_id)
        
    def resolve_id (self, an_id, domain):
        if not an_id in domain:
            candidate = an_id
            an_id = None
            for alternative in self.vocab.equivalence[candidate]:
                if alternative in domain:
                    # Postpone the problem of synonymy
                    an_id = alternative
                    logger.debug ("Selected alternative id {0} for input {1}".format (an_id, candidate))
                    break
                # Also, if all candidates turn out not to be in the domain, we could recurse to try synonyms for them
        return an_id
    
    def translate (self, thing, domainA, domainB):
        result = None
        resolvedA = self.resolve_id (domainA, self.translator_router)
        resolvedB = self.resolve_id (domainB, self.translator_router[domainA])
        if resolvedA and resolvedB:
            result = self.translator_router[resolvedA][resolvedB] (thing)
            if isinstance (result, NoTranslation):
                raise NoTranslation ("No translation implemented from domain {0} to domain {1}".format (domainA, domainB))
        return result

class TestTranslator(unittest.TestCase):
    translator = GraphQL ("http://localhost:5000/graphql")    
    Translation = namedtuple ('Translation', [ 'thing', 'domain_a', 'domain_b' ])
    
    translations = [
        Translation ("Imatinib",     "http://chem2bio2rdf.org/drugbank/resource/Generic_Name", "http://chem2bio2rdf.org/uniprot/resource/gene"),      
        Translation ("CDC25A",       "http://chem2bio2rdf.org/uniprot/resource/gene",          "http://chem2bio2rdf.org/kegg/resource/kegg_pathway"), 
        Translation ("CACNA1A",      "http://chem2bio2rdf.org/uniprot/resource/gene",          "http://pharos.nih.gov/identifier/disease/name"),      
        Translation ("Asthma",       "http://identifiers.org/mesh/disease/name",               "http://identifiers.org/mesh/drug/name"),              
        Translation ("DOID:2841",    "http://identifiers.org/doid",                            "http://identifiers.org/mesh/disease/id"),             
        Translation ("MESH:D001249", "http://identifiers.org/mesh",                            "http://identifiers.org/doi")                          
    ]
    def test_translations (self):
        for translation in self.translations:
            result = self.translator.translate (
                thing=translation.thing,
                domain_a=translation.domain_a,
                domain_b=translation.domain_b)
#        pprint ("{0} => {1}".format (translation.thing, pformat (result)))
        print ("{0} => {1}".format (translation.thing, result))
        
if __name__ == '__main__':
    unittest.main()
