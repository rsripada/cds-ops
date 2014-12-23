# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Creates a link to CERN Library Copies if 964 field not empty
"""
__revision__ = "$Id$"

from invenio.config import CFG_SITE_URL
from invenio.urlutils import create_html_link
from invenio.bibcirculation_dblayer import has_copies
from invenio.bibcirculation_utils import record_edoc_link

def format_element(bfo, label="CERN Library copies"):
    """
    Creates an HTML link to CERN Library copies if 964 field not
    empty, and if collection is not '41'
    @param label Link label
    """
    out = ""
    coll = bfo.field('960__a')
    if coll != "41":
        if has_copies(bfo.recID) or record_edoc_link(bfo.recID):
            out = create_html_link(CFG_SITE_URL + '/record/%i/holdings' % bfo.recID,
                                   urlargd={'ln': bfo.lang},
                                   link_label=label)

    return out


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0

