# pypi-rpm

Placeholder package to make the RPM Python API available through PyPI.

Right now, this package just reserves the `rpm` name on PyPI to avoid the
potential for a name conflict with the `python2-rpm` and `python3-rpm`
Python bindings on RPM-based Linux distros.

However, I eventually hope to replace it with a CMake-dependent PEP 517 backend
that runs the full libdnf build process, and then emits a statically linked
completely self-contained extension module as part of a wheel file (together
with the pure Python components of the DNF Python API).
