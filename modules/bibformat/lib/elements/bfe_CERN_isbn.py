from invenio import bibrecord

def format_element(bfo):
	"""
        bfe_ISBN.py returns string containing ISBN, ISSN of a record.
        020$a = ISBN; 020(R); $a(NR)
        020$u = ISSN; 020(R); $u(NR)

        """

	out = ""

	list_of_020_datafields = bibrecord.record_get_field_instances(bfo.get_record(), '020')

 	for item in list_of_020_datafields:
            item_a = bibrecord.field_get_subfield_values(item, 'a')
            item_u = bibrecord.field_get_subfield_values(item, 'u')

            if item_a:
	        out += item_a[0]
            if item_u:
		out += ' ('
		out += item_u[0]
		out += ')'

            out += "<br/>"
	return out


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
