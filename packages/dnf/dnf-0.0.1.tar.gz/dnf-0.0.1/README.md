# pypi-dnf

Placeholder package to make the DNF Python API available through PyPI.

A number of DNF's dependencies (notable libdnf and libsolv) are currently
only available as part of Linux distro packages.

Right now, this package just reserves the `dnf` name on PyPI to avoid the
potential for a name conflict with the `python3-dnf` packages on Linux distros
using DNF for RPM dependency management.

However, I eventually hope to replace it with a CMake-dependent PEP 517 backend
that runs the full libdnf build process, and then emits a statically linked
completely self-contained extension module as part of a wheel file (together
with the pure Python components of the DNF Python API).
