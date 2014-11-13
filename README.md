teizone 
=======

[![Build Status](https://travis-ci.org/umd-mith/teizone.svg)](http://travis-ci.org/umd-mith/teizone)

teizone will automatically assign coordinates to [TEI zone elements](http://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-zone.html). The coordinates are essentially guesses based on the types of zones. It currently works with [Shelley-Godwin TEI](http://github.com/umd-mith/sga/) (which is also available on GitHub). If there's interest it could be a bit more general purpose...maybe.

A surface can have a main zone, a pagination zone and 0 or more left margin zones. teizone will assign coordinates to the zones using the coordinates of the enclosing surface and this kind of model:

    +--------------------------+
    |                  | PAG | |
    | +------+ +-------------+ |
    | |      | |             | |
    | |  LM  | |             | |
    | |      | |             | |
    | +------+ |             | |
    | +------+ |             | |
    | |      | |             | |
    | |  LM  | |    MAIN     | |
    | |      | |             | |
    | +------+ |             | |
    | +------+ |             | |
    | |      | |             | |
    | |  LM  | |             | |
    | |      | |             | |
    | +------+ +-------------+ |
    +--------------------------+

If you are wondering why we would want to make guesses about the positioning of these zones it's because we are bootstrapping more precise coordinates for use in our [IIIF Presentation](http://iiif.io/api/presentation/2.0/) viewer, which is under development.

## Usage

```python

import teizone

s = teizone.Surface('/path/to/tei/file.xml')
s.guess_coordinates()
s.save()
```

Or if you'd rather not overwrite the old file:

```python
s.save('/path/to/some/other/file.xml')
```


