==========
 openfile
==========

``openfile`` is a trivial Python module that implements a single convenience
function ``openfile(filename, mode="rt", **kwargs)`` wich delegates the real
work to one of the following standard library functions:

- ``gzip.open(filename, mode, **kwargs)`` if the file ends with suffix ``.gz``;
- ``bz2.open(filename, mode, **kwargs)`` if the file ends with suffix ``.bz2``;
- ``lzma.open(filename, mode, **kwargs)`` if the file ends with suffix ``.xz`` or ``.lzma``;
- ``open(filename, mode, **kwargs)`` if the file does not end with any suffix mentioned above.

If the ``filename`` is a single dash ``-`` then ``sys.stdin`` or ``sys.stdout``
is returned, depending on ``mode`` being ``r`` or ``w``, respectively.

The following keyword arguments are used by openfile:

- ``expanduser=True`` will cause openfile to call ``os.path.expanduser`` for ``filename``.
- ``expandvars=True`` will cause openfile to call ``os.path.expandvars`` for ``filename``.
- ``makedirs=True`` will cause openfile to call ``os.makedirs`` for the parent directory ``os.path.dirname(filename)`` if it does not exist and ``mode`` contains either ``"w"`` or ``"a"``.

All other keyword arguments passed to openfile will be passed down to the open functions listed above.
