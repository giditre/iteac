import ctypes
import pathlib

from datetime import datetime

libname = pathlib.Path().absolute() / "lib7seg.so"
c_lib = ctypes.CDLL(libname)
c_lib.display_digits.restype = ctypes.c_int

# digits = [1, 2, 3, 4, 5, 6, 7, 8]
digits = [ int(c) for c in f"{datetime.now():%H%M}" ]

duration = 3

c_lib.display_digits((ctypes.c_int * len(digits))(*digits), ctypes.c_int(len(digits)), ctypes.c_int(duration))
