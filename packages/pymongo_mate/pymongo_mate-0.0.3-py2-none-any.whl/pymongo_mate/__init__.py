#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.3"
__short_description__ = "A library extend pymongo module, makes CRUD easier, and more."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from .crud.insert import *
    from .crud.select import *
    from .crud.update import *
    from .query_builder import *
except:  # pragma: no cover
    pass
