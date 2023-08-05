import platform
import pkg_resources

from cffi import FFI


if platform.system() == 'Linux' and platform.architecture()[0] == '64bit':
    LIB_NAME = 'libdenis.x86_64.so'
elif platform.system() == 'Darwin':
    LIB_NAME = 'libdenis.macos.dylib'
else:
    raise Exception('Unsuported system')


ffi = FFI()
ffi.cdef("""
    double haversine(double, double, double, double);
""")

LIB_PATH = pkg_resources.resource_filename('denis', LIB_NAME)

lib = ffi.dlopen(LIB_PATH)

def haversine(lat_lng1, lat_lng2):
    return lib.haversine(
        lat_lng1[0],
        lat_lng1[1],
        lat_lng2[0],
        lat_lng2[1],
    )
