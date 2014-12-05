#!/usr/bin/env python

from xml.etree import ElementTree as etree

TEI = 'http://www.tei-c.org/ns/1.0'
MITH = 'http://mith.umd.edu/sc/ns1#'

class Surface():
    def __init__(self, path):
        """
        Create a Surface object by giving the constructor a filename for a 
        TEI file.
        """
        self.path = path
        self.doc = etree.parse(path)
        self.root = self.doc.getroot()
        # get canvas dimensions
        self.ulx = int(self.root.get('ulx'))
        self.uly = int(self.root.get('uly'))
        self.lrx = int(self.root.get('lrx'))
        self.lry = int(self.root.get('lry'))
        self.zones = self.root.findall('.//{%s}zone' % TEI)

    def save(self, filename=None):
        """
        Save the possibly modified surface. If you want to save to another
        file pass it in as an argument.
        """
        f = filename if filename else self.path
        etree.register_namespace('', TEI)
        etree.register_namespace('mith', MITH)
        self.doc.write(f, xml_declaration=True, encoding='utf-8', method='xml')

    def guess_coordinates(self, overwrite=False):
        """
        Calculate the coordinates for main, left_margin, pagination and library
        zone types. By default pre-existing coordinates will be preserved. If 
        you want to overwrite pre-existing coordinates set the overwrite 
        parameter to True.
        """

        # TODO: make percentage width of margin and pagination configurable?

        main = None
        library = None
        pagination = None
        left_margin = []
        vertical_margin = 0.05

        for z in self.zones:
            z_type = z.get('type')
            if z_type == "main":
                main = z
            elif z_type == "library":
                library = z
            elif z_type == "pagination":
                pagination = z
            elif z_type == "left_margin":
                left_margin.append(z)

        y = self.uly

        # set coordinates of pagination
        if pagination is not None:
            ulx = int(self.lrx * .8)
            lrx = int(self.lrx * .9)
            lry = y + int(self.lry * .05)

            s(pagination, 'ulx', ulx, overwrite)
            s(pagination, 'uly', 0, overwrite)
            s(pagination, 'lrx', lrx, overwrite)
            s(pagination, 'lry', lry , overwrite)
            y = lry

        # library zone
        if library is not None:
            s(library, 'ulx', int(.9 * self.lrx), overwrite)
            s(library, 'uly', 0, overwrite)
            s(library, 'lrx', self.lrx, overwrite)
            s(library, 'lry', int(.05 * self.lry), overwrite)

        # set coordinates of left margin zones
        if len(left_margin) > 0:
            y = int(.05 * self.lry)
            margin_height = int((.9 / len(left_margin)) * self.lry)
            lrx = int(.25 * self.lrx)
            for z in left_margin:
                s(z, 'ulx', 0, overwrite)
                s(z, 'uly', y, overwrite)
                s(z, 'lrx', lrx, overwrite)
                s(z, 'lry', y + margin_height, overwrite)
                y += margin_height

        # set coordinates for main, which are different if there is a margin
        if main is not None:
            if len(left_margin) == 0:
                left = .125
                right = .875
            else:
                left = .25
                right = .75
            s(main, 'ulx', int(self.lrx * left), overwrite)
            s(main, 'uly', int(self.lry * .05), overwrite)
            s(main, 'lrx', int(self.lrx * right), overwrite)
            s(main, 'lry', int(self.lry * .95), overwrite)

def s(o, prop, val, overwrite=False):
    """
    helper to set a coordinate attribute if it isn't already defined, 
    unless we really want to.
    """
    if overwrite or o.get(prop) is None:
        o.set(prop, str(val))
