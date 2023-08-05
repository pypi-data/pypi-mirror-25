from library_cli import netsdm_reduce
import os

GENOTYPE = 'pw363'
minimum_ranking = 0.95
# [0.005, 0.01, 0.03, 0.05, 0.1, 0.5, 1]:

GOTYPE = 'go'

HYPER = False

ONTOLOGY_LOCATION = 'C:/ziva/go/HEDWIG_ready/%s/%s_dpi/%s_ontology'
ANNOTATIONS_LOCATION = 'C:/ziva/go/HEDWIG_ready/%s/'
BAT_LOCATION = 'C:/ziva/' + GOTYPE + '/HEDWIG_ready/pruned_%s_%s_%i_dpi_run_'
BK_FILE = 'C:/ziva/' + GOTYPE + '/HEDWIG_ready/ontology/go.n3'
EXAMPLES = 'C:/ziva/' + GOTYPE + '/HEDWIG_ready/%s/%i_dpi/hedwig.n3'


TARGET = '-'
DIRECTED = True
for dpi in [1, 3, 6]:
    for minimum_ranking in [0.05, 0.1, 0.5, 1]:
        examples = EXAMPLES % (GENOTYPE, dpi)
        print '------'
        print dpi
        print minimum_ranking
        x = netsdm_reduce(open(examples).read(), [open(BK_FILE).read()], TARGET, DIRECTED, minimum_ranking, HYPER)
        folder = ONTOLOGY_LOCATION % (GENOTYPE, str(dpi), str(minimum_ranking))
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(folder + '/ontology.n3', 'w') as f:
            f.write(x['bk_file'])
        with open('/'.join(folder.split('/')[:-1]) + '_%s_annotations.n3' % str(minimum_ranking), 'w') as f:
            f.write(x['annotations_file'])
        with open(BAT_LOCATION % (GENOTYPE, str(minimum_ranking), dpi) + '+.bat', 'w') as f_pos, open(BAT_LOCATION % (GENOTYPE, str(minimum_ranking), dpi) + '-.bat', 'w') as f_neg:
            f_neg.write('python -m hedwig C:/ziva/%s/HEDWIG_ready/%s/%i_dpi/%s_ontology/ C:/ziva/%s/HEDWIG_ready/%s/%i_dpi_%s_annotations.n3 --adjust=none --leaves --beam=10 --support=0.001 --score=lift --depth=10 --output=c:/ziva/go/HEDWIG_results/%s/pruned/%i_dpi_%s.neg_rules --target=-\npause' % (GOTYPE, GENOTYPE, dpi, str(minimum_ranking), GOTYPE, GENOTYPE, dpi, str(minimum_ranking), GENOTYPE, dpi, str(minimum_ranking)))
            f_pos.write('python -m hedwig C:/ziva/%s/HEDWIG_ready/%s/%i_dpi/%s_ontology/ C:/ziva/%s/HEDWIG_ready/%s/%i_dpi_%s_annotations.n3 --adjust=none --leaves --beam=10 --support=0.001 --score=lift --depth=10 --output=c:/ziva/go/HEDWIG_results/%s/pruned/%i_dpi_%s.pos_rules --target=+\npause' % (GOTYPE, GENOTYPE, dpi, str(minimum_ranking), GOTYPE, GENOTYPE, dpi, str(minimum_ranking), GENOTYPE, dpi, str(minimum_ranking)))

