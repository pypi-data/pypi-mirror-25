<%inherit file="layout.py"/>
from weboob.tools.backend import Module

from .browser import ${r.classname}Browser

__all__ = ['${r.classname}Module']


class ${r.classname}Module(Module):
    NAME = '${r.name}'
    DESCRIPTION = '${r.name} website'
    MAINTAINER = '${r.author}'
    EMAIL = '${r.email}'
    LICENSE = 'AGPLv3+'
    VERSION = '${r.version}'

    BROWSER = ${r.classname}Browser
