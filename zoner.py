#!/usr/bin/env python

from xml.etree import ElementTree as etree

TEI = 'http://www.tei-c.org/ns/1.0'
MITH = 'http://mith.umd.edu/sc/ns1#'

class Surface():

    def __init__(self, path):
        self.path = path
        self.doc = etree.parse(path)
        self.root = self.doc.getroot()
        self.ulx = int(self.root.get('ulx'))
        self.uly = int(self.root.get('uly'))
        self.lrx = int(self.root.get('lrx'))
        self.lry = int(self.root.get('lry'))
        self.zones = self.root.findall('.//{%s}zone' % TEI)
        self._calculate_coordinates()

    def save(self, filename=None):
        f = filename if filename else self.path
        etree.register_namespace('', TEI)
        etree.register_namespace('mith', MITH)
        self.doc.write(f, xml_declaration=True, encoding='utf-8', method='xml')

    def _calculate_coordinates(self):

        # sample type counts from looking at the Frankenstein data
        #
        # main: 1005
        # left_margin: 381
        # pagination: 360
        # library: 175

        main = None
        left_margin = []

        for z in self.zones:
            z_type = z.get('type')
            if z_type == "main":
                main = z
            if z_type == "left_margin":
                left_margin.append(z)

        # determine x of left margin if we have zones in the left margin
        left_margin_x = 0 
        if len(left_margin) > 0:
            left_margin_x = int(self.lrx * .20)
        
        # set coordinates of main zone
        s(main, 'ulx', left_margin_x)
        s(main, 'uly', self.uly)
        s(main, 'lrx', self.lrx)
        s(main, 'lry', self.lry)

        # set coordinates of left margin zones
        y = 0
        margin_height = int(float(self.lry) / len(left_margin))
        for z in left_margin:
            s(z, 'ulx', 0)
            s(z, 'uly', y)
            s(z, 'lrx', left_margin_x)
            s(z, 'lry', y + margin_height)
            y += margin_height

        # set lower-right-y for last zone to the lry of the canvas
        if len(left_margin) > 0:
            s(left_margin[-1], 'lry', self.lry, overwrite=True)


def s(o, prop, val, overwrite=False):
    """
    helper to set a coordinate attribute if it isn't already defined, 
    unless we really want to.
    """
    if overwrite or o.get(prop) is None:
        o.set(prop, str(val))

