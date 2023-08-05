from __future__ import absolute_import, print_function, unicode_literals
from builtins import dict, str
import rdflib
import logging
from rdflib.plugins.parsers.ntriples import ParseError

from indra.databases import ndex_client
from .processor import BelProcessor

logger = logging.getLogger('bel')

ndex_bel2rdf = 'http://bel2rdf.bigmech.ndexbio.org'

def process_ndex_neighborhood(gene_names, network_id=None,
                              rdf_out='bel_output.rdf', print_output=True):
    """Return a BelProcessor for an NDEx network neighborhood.

    Parameters
    ----------
    gene_names : list
        A list of HGNC gene symbols to search the neighborhood of.
        Example: ['BRAF', 'MAP2K1']
    network_id : Optional[str]
        The UUID of the network in NDEx. By default, the BEL Large Corpus
        network is used.
    rdf_out : Optional[str]
        Name of the output file to save the RDF returned by the web service.
        This is useful for debugging purposes or to repeat the same query
        on an offline RDF file later. Default: bel_output.rdf

    Returns
    -------
    bp : BelProcessor
        A BelProcessor object which contains INDRA Statements in bp.statements.

    Notes
    -----
    This function calls process_belrdf to the returned RDF string from the
    webservice.
    """
    if network_id is None:
        network_id = '9ea3c170-01ad-11e5-ac0f-000c29cb28fb'
    url = ndex_bel2rdf + '/network/%s/asBELRDF/query' % network_id
    params = {'searchString': ' '.join(gene_names)}
    # The ndex_client returns the rdf as the content of a json dict
    res_json = ndex_client.send_request(url, params, is_json=True)
    if not res_json:
        logger.error('No response for NDEx neighborhood query.')
        return None
    if res_json.get('error'):
        error_msg = res_json.get('message')
        logger.error('BEL/RDF response contains error: %s' % error_msg)
        return None
    rdf = res_json.get('content')
    if not rdf:
        logger.error('BEL/RDF response is empty.')
        return None

    with open(rdf_out, 'wb') as fh:
        fh.write(rdf.encode('utf-8'))
    bp = process_belrdf(rdf, print_output=print_output)
    return bp


def process_belrdf(rdf_str, print_output=True):
    """Return a BelProcessor for a BEL/RDF string.

    Parameters
    ----------
    rdf_str : str
        A BEL/RDF string to be processed. This will usually come from reading
        a .rdf file.

    Returns
    -------
    bp : BelProcessor
        A BelProcessor object which contains INDRA Statements in bp.statements.

    Notes
    -----
    This function calls all the specific get_type_of_mechanism()
    functions of the newly constructed BelProcessor to extract
    INDRA Statements.
    """
    g = rdflib.Graph()
    try:
        g.parse(data=rdf_str, format='nt')
    except ParseError as e:
        logger.error('Could not parse rdf: %s' % e)
        return None
    # Build INDRA statements from RDF
    bp = BelProcessor(g)
    bp.get_complexes()
    bp.get_activating_subs()
    bp.get_modifications()
    bp.get_activating_mods()
    bp.get_composite_activating_mods()
    bp.get_transcription()
    bp.get_activation()
    bp.get_conversions()

    # Print some output about the process
    if print_output:
        bp.print_statement_coverage()
        bp.print_statements()
    return bp
