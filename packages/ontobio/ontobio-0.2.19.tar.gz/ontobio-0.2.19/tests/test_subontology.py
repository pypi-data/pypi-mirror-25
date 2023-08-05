from ontobio.io.gafparser import GafParser
from ontobio.io.ontol_renderers import GraphRenderer
from ontobio.assoc_factory import AssociationSetFactory

POMBASE = "tests/resources/truncated-pombase.gaf"
CELL_PART = 'GO:0044464'

def test_subont_remote():
    """
    Test creation of a sub-ontology using a set of associations as seed
    """
    from ontobio.ontol_factory import OntologyFactory
    ofa = OntologyFactory()
    ont = ofa.create('go')
    f = AssociationSetFactory()
    aset = f.create(ontology=ont, file=POMBASE, fmt='gaf')

    ont = aset.subontology(minimal=False)
    
    print("ONT = {} N={}".format(ont, len(ont.nodes())))

    # Note: if this class is removed from ontology,
    # this test will fail
    CHROMREG = 'GO:0098687'
    id = CHROMREG
    assert ont.label(id) == 'chromosomal region'
    assert ont.text_definition(id).val is not None
    assert ont.synonyms(id) != []

    id = CELL_PART
    assert ont.label(id) == 'cell part'
    assert ont.text_definition(id).val is not None
    assert ont.synonyms(id) != []
    assert 'NIF_Subcellular:sao628508602' in ont.xrefs(id)
    
    w = GraphRenderer.create('obo')
    print(w.render(ont))

    

def test_subont_local():
    """
    Test creation of a sub-ontology using a set of associations as seed
    """
    from ontobio.ontol_factory import OntologyFactory
    ofa = OntologyFactory()
    ont = ofa.create('tests/resources/nucleus.json')
    assert 'NIF_Subcellular:sao628508602' in ont.xrefs(CELL_PART)    
    f = AssociationSetFactory()
    aset = f.create(ontology=ont, file=POMBASE, fmt='gaf')

    ont = aset.subontology(minimal=False)
    
    print("ONT = {} N={}".format(ont, len(ont.nodes())))
    assert len(ont.nodes()) == 10

    # ensure sub-ontology has preserved xrefs
    assert 'NIF_Subcellular:sao628508602' in ont.xrefs(CELL_PART)    
    
    w = GraphRenderer.create('obo')
    print(w.render(ont))

    # Note: if this class is removed from ontology,
    # this test will fail
    IMBO = 'GO:0043231'
    id = IMBO
    assert ont.label(id) == 'intracellular membrane-bounded organelle'
    assert ont.text_definition(id).val is not None
    assert ont.synonyms(id) != []

    w = GraphRenderer.create('obog')
    print(w.render(ont))

    
    
