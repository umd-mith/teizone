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

        # determine x of left margin if we have zones in the left margin
        left_margin_x = 0 
        if len(left_margin) > 0:
            left_margin_x = int(self.lrx * .20)

        # set coordinates of pagination
        if pagination is not None:
            ulx = self.lrx - int(self.lrx * .33)
            lry = y + int(self.lry * .05)
            s(pagination, 'ulx', ulx, overwrite)
            s(pagination, 'uly', y, overwrite)
            s(pagination, 'lrx', self.lrx, overwrite)
            s(pagination, 'lry', lry , overwrite)
            y = lry

        # TODO: where do we place library zone?
        if library is not None:
            pass 

        # set coordinates for main
        if main is not None:
            s(main, 'ulx', left_margin_x, overwrite)
            s(main, 'uly', y, overwrite)
            s(main, 'lrx', self.lrx, overwrite)
            s(main, 'lry', self.lry, overwrite)

        # set coordinates of left margin zones
        if len(left_margin) > 0:
            margin_height = int((float(self.lry) - y) / len(left_margin))
            for z in left_margin:
                s(z, 'ulx', 0, overwrite)
                s(z, 'uly', y, overwrite)
                s(z, 'lrx', left_margin_x, overwrite)
                s(z, 'lry', y + margin_height, overwrite)
                y += margin_height

            # set lower-right-y for last zone to the lry of the canvas
            s(left_margin[-1], 'lry', self.lry, overwrite=True)


def s(o, prop, val, overwrite=False):
    """
    helper to set a coordinate attribute if it isn't already defined, 
    unless we really want to.
    """
    if overwrite or o.get(prop) is None:
        o.set(prop, str(val))
