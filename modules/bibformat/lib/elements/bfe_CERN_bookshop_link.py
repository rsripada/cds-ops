# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2011 CERN.
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
#### You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Creates an HTML link to CERN IT Bookshop if 690C_a = ITBOOKSHOP
"""
__revision__ = "$Id$"

from invenio.config import CFG_SITE_URL
from invenio.urlutils import create_html_link

def format_element(bfo, label="Purchase a personal copy", linefeed='<br/>', separator = " - ", extra_info=''):
    """
    Creates an HTML link to CERN IT Bookshop if 697C_a = BOOKSHOP
    @param label Link label
    @param linefeed default linefeed before output, unless defined otherwise
    """

    output = ""
    bookshops = bfo.field('697C_a')
    books = bfo.field('690C_a')

    book_isbn = '' # this will be the ISBN to use for linking
    book_isbns = [] # list of all ISBNs
    # eliminate non-print non-empty ISBNs:
    for isbn in bfo.fields('020'):
        isbn_a, isbn_u  = isbn.get('a', ''), isbn.get('u', '')
        if isbn_a and (isbn_u.startswith('print') or isbn_u == ''):
            if not extra_info:
                book_isbns.append(isbn_a)
            elif extra_info and isbn_u and isbn_u.find(extra_info) > -1:
                book_isbns.append(isbn_a)
    # take first ISBN that starts with 978:
    for isbn in book_isbns:
        if isbn.startswith('978'):
            book_isbn = isbn
            break
    # as a last resort, take whatever ISBN we can:
    if not book_isbn and book_isbns:
        book_isbn = book_isbns[0]

    if 'BOOKSHOP' in bookshops:

        output = linefeed
        if book_isbn:
            output += create_html_link('https://found.cern.ch/java/found/BookshopCatalogRedirectServlet',
                                       urlargd={'isbn': book_isbn,},
                                       link_label=label)
        else:
            # no suitable ISBN detected; Anne says to create a link to EDH Stores anyway:
            output += create_html_link('https://found.cern.ch/java/found/BookshopCatalogRedirectServlet',
                                       link_label=label)
    elif 'BOOK' in books:
        link_label="Purchase a personal copy"
        output += create_html_link(CFG_SITE_URL + '/ill/purchase_request_step1',
                                   urlargd={'ln': bfo.lang, 'recid': bfo.recID},
                                   link_label=link_label)

    if output:
        return output
    else:
        return ""


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
