from settings import EXAMPLE_SCHEMA, HEDWIG, W3C
from rdflib import RDF


def prepare(data):
    data.parse(EXAMPLE_SCHEMA, format='n3')


def add_generalization_predicates(rdf_network, generalization_predicates):
    for predicate in generalization_predicates:
        rdf_network.add((predicate, RDF.type, HEDWIG.GeneralizationPredicate))


def anonymous_uri(uri):
    return not uri.startswith('http')


def user_defined(uri):
    """
    Is this resource user defined?
    """
    return not uri.startswith(W3C) and not uri.startswith(HEDWIG) and not anonymous_uri(uri)