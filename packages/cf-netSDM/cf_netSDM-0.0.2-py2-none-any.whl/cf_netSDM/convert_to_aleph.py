from lib.converters import convert_to_aleph

for minimum_ranking in [0.05, 0.1, 0.2, 0.5, 1]:
    mrs = str(minimum_ranking)
    FOLDER = 'C:/hedwig_experiments/breast/new_hyper/'
    ANNOTATIONS = FOLDER + 'annotations_%s.n3' % mrs
    ONTOLOGIES = [FOLDER + mrs + '/ontology.n3']

    r = convert_to_aleph({
        'examples': open(ANNOTATIONS).read(),
        'bk_file': [open(ontology).read() for ontology in ONTOLOGIES],
        'positive_class': '+'
    })
    print "done converting"
    open(FOLDER + '/aleph/%s/breast.b' % mrs, 'w').write(r['bk'])
    open(FOLDER + '/aleph/%s/breast.n' % mrs, 'w').write(r['neg'])
    open(FOLDER + '/aleph/%s/breast.f' % mrs, 'w').write(r['pos'])
    open(FOLDER + '/aleph/%s/skripta.bat' % mrs, 'w').write('yap64 -l skripta.pl')
    open(FOLDER + '/aleph/%s/skripta.pl' % mrs, 'w').write(''':- ['c:/aleph.pl'].
:- read_all(breast).
:- induce.
:- write_rules(out).
''')
