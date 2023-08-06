
# -*- coding: utf-8 -*-
'''
    flask_adfs
    -----------
    This module provides adfs authentication for flask
    :copyright: (c) 2017 John Pickerill.
    :license: MIT/X11, see LICENSE for more details.
'''
from .__about__ import __version__
from .initialise import adfs_init, get_access, set_access
from .decorators import role_required
from .model import User
from .adfs import adfs_bp


__all__ = [
    __version__,
    adfs_bp,
    adfs_init,
    User,
    role_required,
    set_access,
    get_access
]
