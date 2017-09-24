import unittest
from instruments.instrument_catalog import InstrumentCatalog
from tonalmodel.interval import Interval, IntervalType
import logging


class TestInstrumentCatalog(unittest.TestCase):

    logging.basicConfig(level=logging.DEBUG)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        c1 = InstrumentCatalog.instance()
        c2 = InstrumentCatalog.instance()
        
        assert c1 == c2
        
    def test_inst_maps(self):
        c = InstrumentCatalog.instance()
        
        inst = c.get_instrument("vIOlin")
        assert inst is not None
        assert inst.name.startswith('Violin')
        
        instf = c.get_instruments("vIOLin")
        assert instf is not None
        assert len(instf) >= 1
        assert instf[0].name.startswith('Violin')
        
        instf = c.get_instruments("Clarinet")
        assert instf is not None
        assert len(instf) > 1
        assert instf[0].name.startswith('Clarinet')

    def test_transpose(self):
        c = InstrumentCatalog.instance()
        instf = c.get_instruments("Clarinet")
        bflatclarinet = None
        for inst in instf:
            if inst.key == 'Bb':
                bflatclarinet = inst
                break
        assert bflatclarinet is not None
        interval = Interval.create_interval(bflatclarinet.sounding_high, bflatclarinet.written_high)
        assert interval.interval_type.value == IntervalType.Major
        assert interval.diatonic_distance == 1
        
    def test_articulations(self):
        c = InstrumentCatalog.instance()
        inst = c.get_instrument("vIOlin")
        
        articulations = inst.get_articulations()
        for artic in articulations:
            print(artic.name)
        assert 'Arco' in [a.name for a in articulations]
        assert 'Legato' in [a.name for a in articulations]
        
    def test_print_catalog(self):
        c = InstrumentCatalog.instance()
        c.print_catalog()


if __name__ == "__main__":
    unittest.main()
