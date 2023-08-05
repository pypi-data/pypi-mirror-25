#!/usr/bin/env python3

"""Dependency downloader for open_fortran_parser."""

import pathlib
import urllib

if __name__ == '__main__':
    try:
        from .dev_dependencies import DEV_DEPENDENCIES, ensure_dependencies
    except ImportError:
        from dev_dependencies import DEV_DEPENDENCIES, ensure_dependencies
else:
    from .dev_dependencies import DEV_DEPENDENCIES, ensure_dependencies

DEPENDENCIES = DEV_DEPENDENCIES.copy()

DEPENDENCIES.update({
    'Open Fortran Parser XML 0.2.0': (
        urllib.parse.urlparse(
            'https://github.com/mbdevpl/open-fortran-parser-xml/releases/download/v0.2.0/'),
        pathlib.Path('OpenFortranParserXML-0.2.0.jar'))})


if __name__ == '__main__':
    ensure_dependencies(DEPENDENCIES)
