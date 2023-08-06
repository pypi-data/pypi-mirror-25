"""
``openfile`` is a trivial Python module that implements a single convenience
function ``openfile(filename, mode="rt", **kwargs)`` wich delegates the real
work to ``gzip.open()``, ``bz2.open()``, ``lzma.open()`` or ``open()``,
depending on the filename suffix.
"""

import bz2
import gzip
import lzma
import os.path
import sys


__version__ = "0.0.3"


def openfile(filename, mode="rt", *args, expanduser=False, **kwargs):
    """Open filename and return a corresponding file object."""
    if filename in ("-", None):
        return sys.stdin if "r" in mode else sys.stdout
    if expanduser:
        filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        _open = gzip.open
    elif filename.endswith(".bz2"):
        _open = bz2.open
    elif filename.endswith(".xz") or filename.endswith(".lzma"):
        _open = lzma.open
    else:
        _open = open
    return _open(filename, mode, *args, **kwargs)


__all__ = ["openfile"]
