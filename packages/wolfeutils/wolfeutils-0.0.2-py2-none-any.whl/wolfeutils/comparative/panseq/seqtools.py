import os
import pandas as pd
import re
import sys
import wolfeutils.base


def main(infasta, outname=None, enumerate=False, contig_map=None, label='contig_'):
    '''Create panseq-compatibile fasta Headers

    Take FASTA files named just by contig and clean them up.
    Instead of mucking around with regular expressions, just recreate the
    header to be sure it will be clean. Also check! for invalid characters.

    By default, search for "contig_XX" in the header line, and assign that
    contig number to stay consistent with the orignal. Alternatively, use
    --enumerate to simply wipe out the old contig labels and write new ones.

    A new mapping file contigMap.csv is written either way mapping from the old
    label to the onew.
    '''
    # Read FASTA

    with wolfeutils.base.smart_open(infasta, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    if 'endswith' in dir(infasta):
        # Split Filename
        base = os.path.basename(infasta)
        base, ext = os.path.splitext(base)
    else:
        if outname:
            base, ext = os.path.basename(outname), None
        else:
            base, ext = 'seq', None

    invalid = re.compile("[^\w]")

    if outname:
        outHandle = open(outname, 'w')
    else:
        outHandle = sys.stdout

    contigN = 0  # Header lines seen
    contigMap = []

    # Write Lines or Cleaned Headers
    for line in lines:
        l = line
        if line[0] == '>':
            if not enumerate:
                # Determine the correct contig for label
                match_decimals = re.search('tig_?(\d+)', line, flags=re.IGNORECASE)
                match_letters = re.search('tig[_ ]?([\w-]+)', line, flags=re.IGNORECASE)
                if match_decimals:
                    contignum = int(match_decimals.groups()[0])
                    if len(l.split('|')) > 2:
                        if invalid.search(l.split('|')[2]):
                            raise StandardError('Invalid Space in %s' % l)
                    l = '>%s%d' % (label, contignum)
                elif match_letters:
                    contigname = match_letters.groups()[0]
                    l = '>%s%s' % (label, contigname)
                else:
                    match_mito = re.search('mitochondria', line, flags=re.IGNORECASE)
                    if match_mito:
                        # Ignore mitochondrial contigs
                        pass
                    else:
                        raise StandardError('Unrecognized contig number for %s' % l)


            else:
                # Just label contigs by position
                contigN += 1
                l = '|'.join(['>lcl', base.replace('.', '_'),
                              'contig_%s' % contigN])
            contigMap.append({'new': l, 'original': line})

        outHandle.write('%s\n' % l)
    if not contig_map:
        if base:
            contig_out = base + '_contigMap.csv'
        else:
            contig_out = 'contig_map.csv'
    else:
        contig_out = contig_map
    pd.DataFrame(contigMap).to_csv(contig_out)

# label='lcl|%s|contig_%d'
# >%slcl|%s|contig_%d
