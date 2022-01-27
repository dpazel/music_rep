"""

File: instrument_catalog.py

Purpose: Defines the lead node of a catalog instrument tree.
         InstrumentCatalogue is a singleton object representing the root of an instrument tree, which is 
         populated by reading an 'instruments.xml' file.

"""
import xml.etree.ElementTree as ET
import os
import logging

from misc.singleton import Singleton
from instruments.instrument_class import InstrumentClass
from instruments.instrument_family import InstrumentFamily
from instruments.Instrument import Instrument
from instruments.articulation import Articulation
from tonalmodel.interval import Interval
from instruments.instrument_base import InstrumentBase


class InstrumentCatalog(InstrumentBase, Singleton):
    """
    InstrumentCatalog is a singleton object that acts as the root node to a set of musical instruments.
    The details of the instruments are found in 'instruments.xml'.  This class reads that file and 
    populates the catalog with appropriate class instances:
      InstrumentClass: representing an instrument genre such as woodwinds, bass, etc
      InstrumentFamily: representing a type of instrument that may have several variants, e.g. clarinet
      Instrument: representing the instrument itself and carries details about that instrument. 
    """
    
    DATA_DIRECTORY = 'data'
    # Name of the file sound in ./data
    INSTRUMENT_FILE = 'instruments.xml'

    def __init__(self, *args,  **kwargs ):
 
        InstrumentBase.__init__(self, '', None)

        xml_file = kwargs.get('xml_file', None)

        if xml_file is None:
            this_dir, this_filename = os.path.split(__file__)
            data_path = os.path.join(this_dir, InstrumentCatalog.DATA_DIRECTORY)
            tree = ET.parse(os.path.join(data_path, InstrumentCatalog.INSTRUMENT_FILE))
        elif isinstance(xml_file, str):
            if len(xml_file) != 0:
                dir, fn = os.path.split(xml_file)
                tree = ET.parse(os.path.join(dir, fn))
        
        self.inst_classes = []
        
        self.articulations = []
        
        # maps instrument name to instrument.
        self.instrument_map = {}
        
        # maps instrument family name to a list of all the instrument members of that family.
        self.instrument_family_map = {}

        if xml_file is None or len(xml_file) != 0:
            root = tree.getroot()
            self._parse_structure(root)
        
            self._build_maps()
        
    def _parse_structure(self, root):
        for child in root:
            if child.tag == "InstrumentClasses":
                self._parse_classes(child)
            elif child.tag == "Articulations":
                self.articulations = InstrumentCatalog._parse_articulations(child)
        
    def _parse_classes(self, class_root):
        for inst_class in class_root:
            logging.info("{0} {1}".format(inst_class.tag, inst_class.get('name')))
            current_inst_class = InstrumentClass(inst_class.get('name'), self)
            self.inst_classes.append(current_inst_class)
            
            for child_attr in inst_class:
                if child_attr.tag == 'InstrumentGroup':             
                    # article is either an InstrumentFamily, or an Instrument
                    for article in child_attr:  
                        logging.info("   {0}, {1}".format(article.tag, article.attrib))
                        current_family = InstrumentFamily(article.get('name'), current_inst_class)
                        current_inst_class.add_family(current_family)
                        if article.tag == 'InstrumentFamily':                   
                            for inst in article:  
                                logging.info("       {0}, {1}".format(inst.tag, inst.attrib)) 
                                current_family.add_instrument(self.create_instrument(inst, current_family))
                        else:
                            current_family.add_instrument(self.create_instrument(article, current_family))
                elif child_attr.tag == 'Articulations':
                    current_inst_class.extend_articulations(InstrumentCatalog._parse_articulations(child_attr))

    @staticmethod
    def _parse_articulations(articulation_root):
        articulation_list = []
        for articulation in articulation_root:
            articulation_list.append(Articulation(articulation.get('name'))) 
        return articulation_list

    @staticmethod
    def create_instrument(inst_node, parent):
        low = high = ''
        up_down = None
        transpose_interval = None
        articulations = []
        for c in inst_node:
            if c.tag == 'Range':
                for lh in c:
                    if lh.tag == 'Low':
                        low = lh.text
                    elif lh.tag == 'High':
                        high = lh.text  
            elif c.tag == 'Transpose':
                updown_txt = c.get('direction') 
                if updown_txt != 'up' and updown_txt != 'down':
                    raise Exception(
                        'Illegal transpose up/down must be \'up\' or \'down\'  now \'{0}\''.format(updown_txt))
                up_down = updown_txt == 'up'
                transpose_interval = Interval.parse(c.get('interval'))
            elif c.tag == 'Articulations':
                articulations = InstrumentCatalog._parse_articulations(c)
                
        instrument = Instrument(inst_node.get('name'), inst_node.get('key'), low, high, up_down,
                                transpose_interval, parent)
        instrument.extend_articulations(articulations)
        return instrument
    
    def _build_maps(self):
        self.instrument_map = {}
        self.instrument_family_map = {}

        for inst_class in self.inst_classes:
            families = inst_class.families
            for family in families:
                instruments = family.instruments
                self.instrument_family_map[family.name.upper()] = instruments
                for instrument in instruments:
                    self.instrument_map[instrument.name.upper()] = instrument
                    
    def get_instrument(self, name):
        return self.instrument_map[name.upper()] if name.upper() in self.instrument_map else None
    
    def get_instruments(self, name):
        return self.instrument_family_map[name.upper()] if name.upper() in self.instrument_map else None
    
    def instrument_classes(self):
        return list(self.inst_classes)

    def add_instrument_class(self, instrument_class):
        self.inst_classes.append(instrument_class)
        self._build_maps()

    def print_catalog(self):
        for inst_class in self.inst_classes:
            print(inst_class)
            for family in inst_class.families:
                print('    ', family)
                for instrument in family.instruments:
                    print('    ', '    ', instrument)
