import pytest
import tempfile

from teizone import Surface, TEI
from xml.etree import ElementTree as etree


def test_left_margin():
    f1 = 'test-data/ox-ms_abinger_c56/ox-ms_abinger_c56-0039.xml'
    assert_no_coordinates(f1)

    # create and save the surface

    s = Surface(f1)
    assert len(s.zones) == 8
    fh, f2 = tempfile.mkstemp()
    s.guess_coordinates()
    s.save(f2)
    doc = etree.parse(f2)

    assert s.ulx == 0
    assert s.uly == 0
    assert s.lrx == 5364
    assert s.lry == 7104

    # check pagination zone

    pag = doc.find('{%s}zone[@type="pagination"]' % TEI)
    assert pag is not None
    assert pag.get('ulx') == '4291'
    assert pag.get('uly') == '0'
    assert pag.get('lrx') == '4827'
    assert pag.get('lry') == '355'

    # check main zone

    main = doc.find('{%s}zone[@type="main"]' % TEI)
    assert main is not None
    assert main.get('ulx') == '1341'
    assert main.get('uly') == '355'
    assert main.get('lrx') == '5364'
    assert main.get('lry') == '6748'

    # check left margin zones

    left = doc.findall('{%s}zone[@type="left_margin"]' % TEI)
    assert len(left) == 5

    assert left[0].get('ulx') == '0'
    assert left[0].get('uly') == '355'
    assert left[0].get('lrx') == '1341'
    assert left[0].get('lry') == '1633'

    assert left[1].get('ulx') == '0'
    assert left[1].get('uly') == '1633'
    assert left[1].get('lrx') == '1341'
    assert left[1].get('lry') == '2911'

    assert left[2].get('ulx') == '0'
    assert left[2].get('uly') == '2911'
    assert left[2].get('lrx') == '1341'
    assert left[2].get('lry') == '4189'

    assert left[3].get('ulx') == '0'
    assert left[3].get('uly') == '4189'
    assert left[3].get('lrx') == '1341'
    assert left[3].get('lry') == '5467'

    assert left[4].get('ulx') == '0'
    assert left[4].get('uly') == '5467'
    assert left[4].get('lrx') == '1341'
    assert left[4].get('lry') == '6745'

    # check library

    library = doc.findall('{%s}zone[@type="library"]' % TEI)
    assert len(library) == 1

    assert library[0].get('ulx') == '4827'
    assert library[0].get('uly') == '0'
    assert library[0].get('lrx') == '5364'
    assert library[0].get('lry') == '355'

def test_no_margin():
    f1 = 'test-data/ox-ms_abinger_c56/ox-ms_abinger_c56-0005.xml'
    assert_no_coordinates(f1)

    # create and save the surface

    s = Surface(f1)
    assert len(s.zones) == 2
    fh, f2 = tempfile.mkstemp()
    s.guess_coordinates()
    s.save(f2)
    doc = etree.parse(f2)

    main = doc.find('{%s}zone[@type="main"]' % TEI)
    assert main is not None
    assert main.get('ulx') == '636'
    assert main.get('uly') == '354'
    assert main.get('lrx') == '5088'
    assert main.get('lry') == '6727'

def test_no_main():
    f1 = 'test-data/ox-ms_abinger_c56/ox-ms_abinger_c56-0133.xml'
    assert_no_coordinates(f1)

    # create and save the surface

    s = Surface(f1)
    assert len(s.zones) == 1
    fh, f2 = tempfile.mkstemp()
    s.guess_coordinates()
    s.save(f2)

def assert_no_coordinates(path):
    "make sure zone has no coordinates"
    doc = etree.parse(path)
    for zone in doc.findall('.//{%s}zone' % TEI):
        assert zone.get('ulx') == None
        assert zone.get('uly') == None
        assert zone.get('lrx') == None
        assert zone.get('lry') == None
