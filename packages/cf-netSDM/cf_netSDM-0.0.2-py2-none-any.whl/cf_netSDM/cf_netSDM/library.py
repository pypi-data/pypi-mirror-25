from rdflib.graph import Graph
from lib.converters import n3_to_nx, digraph_to_graph, nx_to_n3
from lib.helpers import prepare, add_generalization_predicates
from lib.core import nx_pagerank, shrink_py_pr, page_rank, stochastic_normalization, label_propagation, \
    label_propagation_normalization
from networkx import read_gml
from lib.HIN import HeterogeneousInformationNetwork
from collections import defaultdict
import numpy as np
import logging



def netsdm_reduce(input_dict):
    data = Graph()
    prepare(data)
    data.parse(data=input_dict['examples'], format='n3')
    for ontology in input_dict['bk_file']:
        data.parse(data=ontology, format='n3')
    full_network, positive_nodes, generalization_predicates = n3_to_nx(data, input_dict['target'])
    if not input_dict['directed'] == 'true':
        full_network = digraph_to_graph(full_network)
    node_list = full_network.nodes()
    scores, scores_dict = nx_pagerank(full_network, node_list, positive_nodes)
    shrink_py_pr(full_network, node_list, scores, float(input_dict['minimum_ranking']), positive_nodes)

    rdf_network = nx_to_n3(full_network)
    add_generalization_predicates(rdf_network, generalization_predicates)

    return {'bk_file': rdf_network.serialize(format='n3')}


def load_hml(input_dict):
    net = read_gml(input_dict['file'])
    logging.info('Read file')
    hin = HeterogeneousInformationNetwork(net, input_dict['label_delimiter'])
    train_indices = []
    test_indices = []
    for index, node in enumerate(hin.node_list):
        if len(hin.graph.node[node]['labels']) > 0:
            train_indices.append(index)
        else:
            test_indices.append(index)
    hin.split_to_indices(train_indices=train_indices, test_indices=test_indices)
    hin.create_label_matrix()
    return {'net': hin, 'train_indices': train_indices, 'test_indices': test_indices}


def hinmine_decompose(input_dict):
    return {'test': 'test'}


def hinmine_decompose_post(postdata, input_dict, output_dict):
    try:
        cycles = postdata['cycle']
    except KeyError:
        raise Exception('No decomposition cycle selected')
    hin = input_dict['network']
    for cycle in cycles:
        cycle = cycle.split('_____')
        node_sequence = []
        edge_sequence = []
        for i in range(len(cycle)):
            if i % 2 == 0:
                node_sequence.append(cycle[i])
            else:
                edge_sequence.append(cycle[i])
        degrees = defaultdict(int)
        for item in hin.midpoint_generator(node_sequence, edge_sequence):
            for node in item:
                degrees[node] += 1
        hin.decompose_from_iterator('decomposition',
                                    input_dict['heuristic'],
                                    None,
                                    hin.midpoint_generator(node_sequence, edge_sequence),
                                    degrees=degrees)

        # save_sparse(tehin.decomposed['MAM_%s' % weighing], 'D:/imdb_data/MAM.%s_fold_%i.npz' % (weighing, fold))
        logging.info('%s done' % input_dict['heuristic'])

    return {'network': hin}


def hinmine_propositionalize(input_dict):
    hin = input_dict['network']
    assert isinstance(hin, HeterogeneousInformationNetwork)
    n = hin.decomposed['decomposition'].shape[0]
    vectors = np.zeros((n, n))
    graph = stochastic_normalization(hin.decomposed['decomposition'])
    for index in range(n):
        pr = page_rank(graph, [index], try_shrink=True)
        norm = np.linalg.norm(pr, 2)
        if norm > 0:
            pr = pr / np.linalg.norm(pr, 2)
            vectors[index, :] = pr
    train_features = {
        'data': vectors[hin.train_indices, :],
        'target': hin.label_matrix[hin.train_indices, :],
        'target_names': [str(x) for x in hin.label_list],
        'DESCR': None
    }
    test_features = {
        'data': vectors[hin.test_indices, :],
        'target_names': [str(x) for x in hin.label_list],
        'DESCR': None
    }
    return {'train_features': train_features, 'test_features': test_features}


def hinmine_label_propagation(input_dict, weights=None, alpha=0.85, semibalanced=None):
    hin = input_dict['network']
    assert isinstance(hin, HeterogeneousInformationNetwork)
    matrix = label_propagation_normalization(hin.decomposed['decomposition'])
    hin.create_label_matrix(weights=weights)
    propagated_matrix = label_propagation(matrix, hin.label_matrix, alpha)
    return {'result': propagated_matrix}