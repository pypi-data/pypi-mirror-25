import networkx as nx
import pickle
import os
import logging

from library_cli import netsdm_reduce
import os

# from lib.converters import n3_to_nx_hyper

# import rdflib
#
# g = rdflib.Graph()
# g.parse('c:/testni_grafek.n3', format='n3')
# x = n3_to_nx_hyper(g, None)
# print 1/0


HYPER = False

folder_name = 'new_hyper' if HYPER else 'new_nonhyper'
BK_FILE = 'C:/hedwig_experiments/all/%s/ontology/go.n3' % folder_name
EXAMPLES = 'C:/hedwig_experiments/all/%s/annotations.n3' % folder_name
OUTPUT_FOLDER = 'C:/hedwig_experiments/all/' + folder_name + '/%s'
BAT_LOCATION = 'C:/hedwig_experiments/all/%s/' % folder_name

TARGET = '+'
DIRECTED = True
for minimum_ranking in [0.005, 0.01, 0.02, 0.03, 0.04]: #, 0.05, 0.1, 0.2, 0.5, 1]:
    print '------'
    print minimum_ranking
    mrs = str(minimum_ranking)
    x = netsdm_reduce(open(EXAMPLES).read(), [open(BK_FILE).read()], TARGET, DIRECTED, minimum_ranking, HYPER)
    ontology = x['bk_file']
    annotations = x['annotations_file']
    folder = OUTPUT_FOLDER % mrs
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(folder + '/ontology.n3', 'w') as f:
        f.write(ontology)
    with open(BAT_LOCATION + '/annotations_%s.n3' % mrs, 'w') as f:
        f.write(annotations)
    with open(BAT_LOCATION + 'run_%s.bat' % mrs, 'w') as f:
        f.write(
            'python -m hedwig C:/hedwig_experiments/all/%s/%s C:/hedwig_experiments/all/%s/annotations_%s.n3'
            ' --adjust=none --leaves --score=wracc --beam=10 --support=0.01 --score=lift --depth=10'
            ' --output=new_rules_%s --target=+\npause' % (folder_name, mrs, folder_name, mrs, mrs))
print 1 / 0
