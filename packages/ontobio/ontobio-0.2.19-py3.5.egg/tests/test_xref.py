from ontobio import OntologyFactory
from ontobio import GraphRenderer
import logging
import ontobio.xref_util as xu

PART_OF = 'BFO:0000050'


NUCLEUS='GO:0005634'
INTRACELLULAR='GO:0005622'
INTRACELLULAR_PART='GO:0044424'
IMBO = 'GO:0043231'
CELL = 'GO:0005623'
CELLULAR_COMPONENT = 'GO:0005575'
WIKIPEDIA_CELL = 'Wikipedia:Cell_(biology)'
NIF_CELL = 'NIF_Subcellular:sao1813327414'
CELL_PART = 'GO:0044464'

def test_xref():
    """
    Load ontology from JSON
    """
    factory = OntologyFactory()
    print("Creating ont")
    ont = factory.create('tests/resources/xref.json')
    g = ont.xref_graph
    for x,y in g.edges_iter():
        print('{} <-> {}'.format(x,y))

    xu.materialize_xrefs_as_edges(ont)
    w = GraphRenderer.create('tree')
    print(w.render(ont))
