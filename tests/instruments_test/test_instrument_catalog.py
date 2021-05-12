import unittest
from instruments.instrument_catalog import InstrumentCatalog, InstrumentClass, InstrumentFamily, Instrument
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
        print(inst)
        
        instf = c.get_instruments("vIOLin")
        assert instf is not None
        assert len(instf) >= 1
        assert instf[0].name.startswith('Violin')
        print('[{0}]'.format(','.join(str(s) for s in instf)))
        
        instf = c.get_instruments("Clarinet")
        assert instf is not None
        assert len(instf) > 1
        assert instf[0].name.startswith('Clarinet')
        print('[{0}]'.format(','.join(str(s) for s in instf)))

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
        assert interval.interval_type == IntervalType.Major
        assert interval.diatonic_distance == 1
        
    def test_articulations(self):
        c = InstrumentCatalog.instance()
        inst = c.get_instrument("vIOlin")
        
        articulations = inst.get_articulations()
        for artic in articulations:
            print(artic.name)
        assert 'Arco' in [a.name for a in articulations]
        assert 'Legato' in [a.name for a in articulations]

    def test_manual_create_catalog(self):
        catalog = InstrumentCatalog(xml_file='')

        inst_class = InstrumentClass("Strings")
        catalog.add_instrument_class(inst_class)

        inst_family = InstrumentFamily("Violins")
        inst_class.add_family(inst_family)

        instrument = Instrument("My Violin", 'C', 'C:3', 'C:7', None, None)
        inst_family.add_instrument(instrument)

        catalog.print_catalog()

    def atest1_open_outside(self):
        catalog = InstrumentCatalog.instance(xml_file='/Users/.../my_instruments.xml')

        c1 = InstrumentCatalog.instance()

        assert c1 == catalog


    def test_print_catalog(self):
        c = InstrumentCatalog.instance()
        c.print_catalog()


if __name__ == "__main__":
    unittest.main()

# test for token checkin
