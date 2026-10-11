import ast, csv, os, sys, re, json
# source data (not committed): ecdict.csv and the ngsl PyPI package, see README
DL = os.environ.get('DANCI_DL', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dl'))
sys.path.insert(0, '.')
from awl import SUBLISTS

def ngsl_rank():
    src = open(DL + '/ngslpkg/ngsl-1.41/ngsl/rank.py', encoding='utf-8').read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, 'id', '') == 'RANK_DICT':
            return ast.literal_eval(node.value)
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'RANK_DICT' for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit('no RANK_DICT')

def ecdict():
    csv.field_size_limit(10**8)
    d = {}
    with open(DL + '/ecdict.csv', encoding='utf-8', newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            w = row['word']
            if w not in d:
                d[w] = row
    return d
