# Read a panseq tree and relabel using names from phyllip_name_conversion.txt
# Usage: ./relabelNewick.py RAxML_bipartitions.PanSeqSnpRaxmlTree.newick phylip_name_conversion.txt > RAxML_bipartitions.PanSeqSnpRaxmlTree.Names.newick
# import os
import pandas as pd
import re
# import sys


def labelTree(tree_file, names_file):
    with open(tree_file, 'r') as f:
        tree_str = f.read()

    names_df = pd.read_table(names_file, index_col='Number')
    for num, name in names_df['Name'].iteritems():
        tree_str = re.sub('\(%d:' % num, '(%s:' % name, tree_str)
        # Lazy - requires 2 passes of re to match paren or comma
        tree_str = re.sub(',%d:' % num, ',%s:' % name, tree_str)

    return tree_str
