# -*- coding: utf-8 -*-
##
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


"""BibFormat element - Returns links of related titles of other editions
"""

from invenio.bibformat_elements.bfe_CERN_related_records_links import create_resource_links

def format_element(bfo,
                   tag='775__',
                   edition_subfield_code='b',
                   year_subfield_code='c',
                   note_subfield_code='n',
                   title_subfield_code='p',
                   record_control_number='w',
                   separator=', ',
                   ):

    """
    Return the links of the related resource, defined in 'tag'.
    Display the related resource's title (link_text) as follows:

    Link text =
    tag$edition_subfield_code ( tag$year_subfield_code ) - tag$title_subfield_code

    Link target is found via tag$record_control_number

    e.g., cdsweb: recid: 1346067; title:Aluminium-Taschenbuch
    """

    out = ''

    issues = bfo.fields(tag)

    issues = sorted(issues, key=lambda k: k.get(year_subfield_code, ''))
    for issue in issues:

        #clear out sub-strings otherwise final string will contain previous loop's data
        issue_year_bracketed = ""
        issue_note_dashed = ""
        issue_title_commaed = ""

        year = issue.get(year_subfield_code, '')
        if year:
            issue_year_bracketed = ' (' + year + ')'

        note = issue.get(note_subfield_code, '')
        if note:
            issue_note_dashed = ' - ' + note

        title = issue.get(title_subfield_code, '')
        if title:
            issue_title_commaed = ', ' + title


        # build up the link_text that will be displayed
        link_text = issue.get(edition_subfield_code,'') + \
                    issue_year_bracketed + \
                    issue_note_dashed + \
                    issue_title_commaed


        out += separator.join(create_resource_links(link_text, issue.get(record_control_number, '')))
        out += "<br/>"

    return out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
