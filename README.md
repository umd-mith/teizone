zoner 
=====

[![Build Status](https://travis-ci.org/umd-mith/zoner.svg)](http://travis-ci.org/umd-mith/zoner)

Automatically assign coordinates to TEI zone elements. The coordinates are
guesses based on the types of zones. It currently works with 
[Shelley-Godwin TEI](http://github.com/umd-mith/sga/) (which is also available 
on GitHub). If there's interest it could be a bit more general purpose...maybe.

```python

import zoner

s = zoner.Surface('/path/to/tei/file.xml')
s.guess_coordinates()
s.save()
```

Or if you'd rather not overwrite the old file:

```python
s.save('/path/to/some/other/file.xml')
```

If you are wondering why we would want to do such thing it's because 
we are bootstrapping more precise coordinates for use in our 
[IIIF Presentation](http://iiif.io/api/presentation/2.0/) viewer.

