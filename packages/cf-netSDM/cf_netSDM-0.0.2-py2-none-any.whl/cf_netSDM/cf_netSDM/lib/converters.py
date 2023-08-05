import networkx as nx
from settings import HEDWIG
from rdflib import RDF
from rdflib.term import Literal
from helpers import user_defined
import logging
import rdflib


def n3_to_nx(data, positive_class):
    return_graph = nx.DiGraph()
    positive_class = Literal(positive_class)
    generelization_predicates = list(data.subjects(predicate=RDF.type, object=HEDWIG.GeneralizationPredicate))
    for predicate in generelization_predicates:
        for sub, obj in data.subject_objects(predicate=predicate):
            if user_defined(sub) and user_defined(obj):
                return_graph.add_edge(sub, obj, type=predicate)
    target_nodes = set()
    for example in data.subjects(predicate=RDF.type, object=HEDWIG.Example):
        if (example, HEDWIG.class_label, positive_class) in data:
            target_nodes.add(example)
            for annotation_link in data.objects(subject=example, predicate=HEDWIG.annotated_with):
                annotations = data.objects(subject=annotation_link, predicate=HEDWIG.annotation)
                annotation = annotations.next()
                if next(annotations, None) is not None:
                    raise Exception("Unable to parse data - annotations for example %s are unclear" % example)
                if annotation not in return_graph:
                    raise Exception("Data - BK synchronization error: annotation %s does not appear in the Background "
                                    "knowledge!" % annotation)
                return_graph.add_edge(example, annotation)
    roots = [node for node in return_graph if len(return_graph.edge[node]) == 0]
    for root in roots:
        return_graph.add_edge(root, HEDWIG.dummy_root, type=RDF.type)
    return return_graph, target_nodes, generelization_predicates


def nx_to_n3(network):
    logging.info('Building graph')
    g = rdflib.Graph()
    for term in network.edge:
        for end in network.edge[term]:
            g.add((term, network.edge[term][end]['type'], end))
    return g

def digraph_to_graph(graph):
    return nx.Graph(graph)
