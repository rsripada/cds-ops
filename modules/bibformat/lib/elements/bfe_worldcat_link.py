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
"""BibFormat element - Creates a link to world cat isbn search.
"""
__revision__ = "$Id$"

from invenio.urlutils import create_html_link

def format_element(bfo,  link_prefix='This book in a ', separator=' OR ', label='library next to me'):
    """
    Creates an HTML link to world cat isbn search.
    @param label Link label
    """
    out = ""
    book = bfo.field('690C_a')
    isbn = separator.join(bfo.fields('020__a'))
    if 'BOOK' in book and isbn != "":
        out = link_prefix + create_html_link('http://www.worldcat.org/search?q=%s&qt=owc_search' % isbn, {}, link_label=label)

    return out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0

