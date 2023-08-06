==========
 openfile
==========

``openfile`` is a trivial Python module that implements a single convenience
function ``openfile(filename, mode="rt", **kwargs)`` wich delegates the real
work to one of the following standard library functions:

``gzip.open(filename, mode, **kwargs)``
    if the file ends with suffix ``.gz``;
``bz2.open(filename, mode, **kwargs)``
    if the file ends with suffix ``.bz2``;
``lzma.open(filename, mode, **kwargs)``
    if the file ends with suffix ``.xz`` or ``.lzma``;
``open(filename, mode, **kwargs)``
    if the file does not end with any suffix mentioned above.

If the ``filename`` is a single dash ``-`` then ``sys.stdin`` or ``sys.stdout``
is returned, depending on ``mode`` being ``r`` or ``w``, respectively.
