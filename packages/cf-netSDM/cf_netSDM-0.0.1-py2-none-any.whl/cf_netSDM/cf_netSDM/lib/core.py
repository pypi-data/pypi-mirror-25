import networkx as nx
import numpy as np
import scipy.sparse as sp
import logging


def stochastic_normalization(matrix):
    logging.info('Creating google matrix...')
    matrix = matrix.tolil()
    matrix.setdiag(0)
    matrix = matrix.tocsr()
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    d[nzs] = 1 / d[nzs]
    matrix = (sp.diags(d, 0).tocsc().dot(matrix)).transpose()
    logging.info('Google matrix created.')
    return matrix


def page_rank(matrix, start_nodes,
              epsilon=1e-6,
              max_steps=10000,
              damping=0.85,
              spread_step=10,
              spread_percent=0.5,
              try_shrink=True):
    assert(len(start_nodes)) > 0
    # this method assumes that column sums are all equal to 1 (stochastic normalizaition!)
    size = matrix.shape[0]
    if start_nodes is None:
        start_nodes = range(size)
        nz = size
    else:
        nz = len(start_nodes)
    start_vec = np.zeros((size, 1))
    start_vec[start_nodes] = 1
    start_rank = start_vec / len(start_nodes)
    rank_vec = start_vec / len(start_nodes)
    # calculate the max spread:
    shrink = False
    which = np.zeros(0)
    if try_shrink:
        v = start_vec / len(start_nodes)
        steps = 0
        while nz < size * spread_percent and steps < spread_step:
            steps += 1
            v += matrix.dot(v)
            nz_new = np.count_nonzero(v)
            if nz_new == nz:
                shrink = True
                break
            nz = nz_new
        rr = np.arange(matrix.shape[0])
        which = (v[rr] > 0).reshape(size)
        if shrink:
            start_rank = start_rank[which]
            rank_vec = rank_vec[which]
            matrix = matrix[:, which][which, :]
    diff = np.Inf
    steps = 0
    while diff > epsilon and steps < max_steps:  # not converged yet
        steps += 1
        new_rank = matrix.dot(rank_vec)
        rank_sum = np.sum(new_rank)
        if rank_sum < 0.999999999:
            new_rank += start_rank * (1 - rank_sum)
        new_rank = damping * new_rank + (1 - damping) * start_rank
        new_diff = np.linalg.norm(rank_vec - new_rank, 1)
        diff = new_diff
        rank_vec = new_rank
    if try_shrink and shrink:
        ret = np.zeros(size)
        ret[which] = rank_vec
        ret[start_nodes] = 0
        return ret.flatten()
    else:
        rank_vec[start_nodes] = 0
        return rank_vec.flatten()


def nx_pagerank(network, node_list, enriched_nodes):
    enriched_nodes = set(enriched_nodes)
    matrix = nx.to_scipy_sparse_matrix(network, dtype=float, nodelist=node_list, format='csr')
    enriched_indices = [i for i in range(len(node_list)) if node_list[i] in enriched_nodes]
    normalized_matrix = stochastic_normalization(matrix)

    pr = page_rank(normalized_matrix, enriched_indices, epsilon=1e-10, damping=0.99)

    pr_dict = {}
    for i in range(len(node_list)):
        pr_dict[node_list[i]] = pr[i]
    return pr, pr_dict


def shrink_py_pr(network, node_list, pr, percentage, enriched_symbols):
    if percentage < 1:
        pr_sorted = np.sort(pr.flatten())
        pr_sorted[:] = pr_sorted[::-1]
        threshold = pr_sorted[int(percentage * (pr.shape[0] - len(enriched_symbols)))]
        for i in range(pr.shape[0]):
            if pr[i] < threshold:
                network.remove_node(node_list[i])
    else:
        for i in range(pr.shape[0]):
            if node_list[i] in enriched_symbols:
                network.remove_node(node_list[i])


def label_propagation_normalization(matrix):
    matrix = matrix.tocsr()
    matrix.setdiag(0)
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    d[nzs] = 1 / np.sqrt(d[nzs])
    dm = sp.diags(d, 0).tocsc()
    return dm.dot(matrix).dot(dm)


def label_propagation(graph_matrix, class_matrix, alpha, epsilon=1e-12, max_steps=10000):
    # This method assumes the label-propagation normalization and a symmetric matrix with no rank sinks.
    steps = 0
    diff = np.inf
    current_labels = class_matrix
    while diff > epsilon and steps < max_steps:
        # print steps
        # print diff
        steps += 1
        new_labels = alpha * graph_matrix.dot(current_labels) + (1 - alpha) * class_matrix
        diff = np.linalg.norm(new_labels - current_labels) / np.linalg.norm(new_labels)
        current_labels = new_labels
    return current_labels