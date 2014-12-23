# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
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
"""BibFormat element - Prints book chapters
"""
__revision__ = "$Id$"

import re

from invenio.search_engine import perform_request_search
from invenio.bibformat_engine import BibFormatObject
from invenio.urlutils import create_html_link
from invenio.config import CFG_SITE_URL

def format_element(bfo, display_search_link_to_chapters='yes', volume_label="Volume "):
    """
    Prints book chapters.

    @param display_search_link_to_chapters: display a link searching for corresponding chapters in CDS, or not.
    """

    output = ''

    # Get recid
    conf = bfo.recID

    record_ids = perform_request_search(p=str(conf), f="962__b", c=['Articles & Preprints'])
    if len(record_ids) > 10000:
        return output

    records = {}
    for record_id in record_ids:
        records[record_id] = BibFormatObject(record_id)

    # Extract page information.
    comparedata = []
    re_page = re.compile('^(\d+)$')
    re_pagerange = re.compile('^(\d+)-(\d+)$')
    re_volume = re.compile('^(\d+)\s*(:(.+))?$')
    for record in records:
        confs = records[record].fields("962__b")
        volume_title = records[record].field("962__s") # Format is "vol_nr: title"
        try:
            volume_number = int(records[record].field("962__v"))
        except:
            volume_number = None

        if not volume_number:
            # Try to extract volume from title
            try:
                volume_matchobj = re_volume.match(volume_title)
                volume_number = volume_matchobj.group(1)
                try:
                    volume_number = int(volume_number)
                except:
                    # volume is not a number
                    pass
            except:
                # Could not understand format. Move at end of
                # the list
                volume_number = None

        pagefield = ''
        try:
            confindex = confs.index(str(conf))
            pagefield = (records[record].fields("962__k"))[confindex]
        except IndexError:
            pass
        mo_pagerange = re_pagerange.match(pagefield)
        if mo_pagerange:
            comparedata.append([record, volume_number, volume_title, pagefield, int(mo_pagerange.group(1)), int(mo_pagerange.group(2))])
        else:
            mo_page = re_page.match(pagefield)
            if mo_page:
                comparedata.append([record, volume_number, volume_title, pagefield, int(mo_page.group(1)), None])
            else:
                comparedata.append([record, volume_number, volume_title, pagefield, None, None])

    # Sort.
    comparedata.sort(compare_records_by_volume_and_page)

    # Print the chapters
    if comparedata: output += '<p class="formatRecordLabel"><b>Chapters in  this volume</b></p><table cellspacing="2" width="100%">'
    last_volume_header = ''
    for record in comparedata:
        recid = record[0]
        volume_number = record[1]
        volume_title = record[2]
        #volume_header = (volume_number or volume_title) and (volume_label + volume_number + ':' volume_title) or ''
        volume_header = ''
        if volume_title:
            volume_header = volume_label + volume_title

        title = records[recid].field("245__a")
        sub_title = records[recid].field("245__b")
        if record[4]:
            startpage = '(p. %s)' % record[4]
        elif record[3]:
            startpage = '(%s)' % record[3]
        else:
            startpage = ''

        # put in punctuation mark
        if sub_title:
            sub_title = " : " + sub_title
        else:
            sub_title = ""


        if volume_header:
            if volume_header != last_volume_header:
                output += '<tr><td><br/><strong>' + volume_header + '</strong></td></tr>'
            
        link = '%s/record/%s?ln=%s' % (CFG_SITE_URL, recid, bfo.lang)
        output += '''<tr><td%s><a href="%s">%s %s</a>%s</td></tr>''' % \
            (volume_header and ' style="padding-left:10px"' or '', link, title, sub_title, startpage)
        last_volume_header = volume_header
    if comparedata: output += '</table>'

    if display_search_link_to_chapters.lower() == 'yes' and len(record_ids) > 0:
        # Print a link doing more or less the same as the above, but
        # triggering a search in CDS for the chapters of this
        # book. This is usefull if users want for eg. to further
        # narrow down the search to a given collection or any other
        # more specific constraints.
        output += '<br/><small>' + \
                  create_html_link(urlbase=CFG_SITE_URL + '/search',
                                   urlargd={'p':'962:' + str(conf)},
                                   link_label="Show chapters in CDS") + \
                  '</small><br/>'
        

    return output

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0

def compare_records_by_volume_and_page(record_a, record_b):
    """
    Compare two records by volume and page number.

    The record with smaller volume get first. Records without volume get last.

    The record with the first start page is the smallest. If a record lack start page,
    it is per definition greater (will show up last).

    If the records have similar start pages, the record with the first end page is the smallest.
    If, in this case, one record lack end page, this record is considered smaller.

    If the records don't have page number(s), they will just be compared by the content of the
    pagefield, with empty pagefields coming last.

    @param a a record, given as a list of data on the form [recid, pagefield, start page, end page]
    @param b another record, given in the same way
    """

    # Compare volumes:
    if record_a[1] is None and record_b[1]:
        return 1
    if record_b[1] is None and record_a[1]:
        return -1
    if record_a[1] > record_b[1]:
        return 1
    if record_b[1] > record_a[1]:
        return -1

    # Get a chance to compare volume name in case volume number match.
    if record_a[2] > record_b[2]:
        return 1
    if record_b[2] > record_a[2]:
        return -1

    # One or both records lack start page.
    if record_a[4] is None:
        if record_b[4] is None:
            # Compare by pagefield
            if not record_b[3]:
                return -1
            if not record_a[3]:
                return 1
            if record_a[3] > record_b[3]:
                return 1
            if record_b[3] > record_a[3]:
                return -1
            return 0
        return 1
    elif record_b[4] is None:
        # B is None, but not A
        return -1

    if record_b[3] is None:
        # Is that really needed? Not sure it can be None
        return -1

    # Compare by start page.
    if record_a[4] > record_b[4]:
        return 1
    if record_b[4] > record_a[4]:
        return -1

    # One or both records lack end page.
    if record_a[5] is None:
        return -1
    if record_b[5] is None:
        return 1

    # Compare by end page.
    if record_a[5] > record_b[5]:
        return 1
    if record_b[5] > record_a[5]:
        return -1

    # Records are equal.
    return 0
