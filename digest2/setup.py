"""Build configuration for digest2 C extension."""

import platform

from setuptools import Extension, setup

c_sources = [
    "digest2/d2math.c",
    "digest2/d2model.c",
    "digest2/d2modelio.c",
    "digest2/d2mpc.c",
    "digest2/common.c",
    "digest2/d2lib.c",
    "src/digest2/_extension.c",
]

# Define D2_NO_LIBXML and D2_NO_REGEX so the library build
# skips libxml2 and POSIX regex dependencies.
define_macros = [
    ("D2_NO_LIBXML", "1"),
    ("D2_NO_REGEX", "1"),
]

extra_compile_args = []
libraries = []

if platform.system() == "Windows":
    extra_compile_args = ["/std:c11", "/O2"]
else:
    extra_compile_args = ["-std=c99", "-O2"]
    libraries = ["m"]

ext = Extension(
    "digest2._extension",
    sources=c_sources,
    include_dirs=["digest2"],
    libraries=libraries,
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
)

setup(
    ext_modules=[ext],
    package_dir={"": "src"},
    package_data={"digest2": ["data/*"]},
)
