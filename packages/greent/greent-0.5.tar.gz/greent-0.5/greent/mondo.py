import pronto
from collections import defaultdict

class Mondo(object):
    def __init__(self):
        self.ont = pronto.Ontology ("mondo.obo")
        self.mondo = defaultdict(lambda:[])
        for term in self.ont:
            xref = None
            if 'xref' in term.other:
                for xref in term.other['xref']:
                    if xref.startswith ("MESH:"):
                        print ("doid: {0} -> {1}".format (term.id.upper (), xref))
                        self.mondo[term.id.upper ()].append

m = Mondo ()

