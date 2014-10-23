Automatically assign coordinates to TEI zone elements. The coordinates are
guesses based on the types of zones. It currently works with 
[Shelley-Godwin TEI](http://github.com/umd-mith/sga/) (which is also available 
on GitHub). If there's interest it could be a bit more general purpose...maybe.

```python

import zoner

s = zoner.Surface('/path/to/tei/file.xml')
s.save()
```

Or if you'd rather not overwrite the old file:

```python
s.save(/path/to/some/other/file.xml')
```
