# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-categories."""

#from webhelpers import date, feedgenerator, html, number, misc, text
from markupsafe import Markup

def bold(text):
    return Markup('<strong>%s</strong>' % text)


# waiting for a new version of tgext.pluggable
try:
    from tgext.pluggable.utils import instance_primary_key
except ImportError:  # when tgext.pluggable is not updated
    def instance_primary_key(instance, as_string=False):
        """Returns the value of the primary key of the instance"""
        from tgext.pluggable.utils import primary_key
        p = getattr(instance, primary_key(instance.__class__).name)
        return p if not as_string else str(p)
