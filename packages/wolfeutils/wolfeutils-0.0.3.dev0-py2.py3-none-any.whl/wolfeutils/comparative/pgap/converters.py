#!/usr/bin/env python
import datetime
# from glob import glob
import gzip
# from multiprocessing import Pool
import os
import pandas as pd
import re
import shutil
from StringIO import StringIO
import sys
import tarfile
import tempfile
# import time
import urllib2
import warnings

from Bio import BiopythonWarning
from Bio.Blast.Applications import NcbirpsblastCommandline
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import wolfeutils.base


warnings.simplefilter('error', BiopythonWarning)


def gbk2Pgap(infile, source='auto', cog_lookup=False):
    base, ext = default_outfile(infile)
    seqs = read_gbk(infile, source)

    # Concatenate Records
    seq_df = pd.DataFrame(seqs)
    if not len(seq_df):
        raise ValueError('No sequences parsed successfully.')
    seq_df.index = seq_df['seed_xref']
    seq_df['nuc_length'] = seq_df['nuc'].apply(lambda x: len(x))
    seq_df = seq_df[seq_df['nuc_length'] >= 15]

    # Write pep records to temp file for rpsblast
    peps = []
    nucs = []

    for seq_id, seq in seq_df.iterrows():
        s = len(seq.pep)
        if s < 5:
            print(s)
        pep = SeqRecord(
            Seq(seq.pep[:-1]),
            id=str(seq_id),
            description='')  # Remove Stop Codon
        nuc = SeqRecord(Seq(seq.nuc), id=str(seq_id), description='')
        peps.append(pep)
        nucs.append(nuc)

    pep_fa = '%s.pep' % base
    nuc_fa = '%s.nuc' % base

    with open(pep_fa, 'w') as f:
        out_count = SeqIO.write(peps, f, 'fasta')
    with open(nuc_fa, 'w') as f:
        SeqIO.write(nucs, f, 'fasta')

    print('Wrote %d seqs' % out_count)

    # Cache?
    # seq_df.to_csv('%s.csv.gz' % base, compression='gzip')

    if cog_lookup:
        cogs = lookup_cog(pep_fa)
        seq_df['cog'].update(cogs)

    seq_df[['cog', 'description']].to_csv('%s.function' % base,
                                          header=False,
                                          sep='\t')


def read_gbk(infile, source):
    '''Read a Genbank file and parse its sequences, annotations and features'''
    seqs = []
    feature_count, seq_count = 0, 0
    # Counters for coding sequences and total number of features

    bad_triplet, size_mismatch, zero_length = 0, 0, 0
    # Fail counters - zero length prediciton, bad modulo for the nucleotide
    # (not divisible by 3 so probably not a good aa coding sequence) and
    # a mismatch in total between the length of the aa and the na

    if source == 'auto':
        source = infer_source(infile)

    if source == 'kbase':
        feature_type = 'gene'
    else:
        feature_type = 'CDS'

    for seq_record in SeqIO.parse(wolfeutils.base.openFunc(infile), "genbank"):
        seq_count += 1
        features = [f for f in seq_record.features if f.type == feature_type]
        for feature in features:
            try:
                feature_count += 1
                feature_info = parse_feature(feature, seq_record, source)
                seqs.append(feature_info)
                status = '.'
            except (KeyError, ValueError) as err:
                if 'bad_triplet' in err.message:
                    bad_triplet += 1
                elif 'zero_length' in err.message:
                    zero_length += 1
                elif 'size_mismatch' in err.message:
                    size_mismatch += 1
                else:
                    raise
                status = 'x'
            sys.stderr.write(status)
            sys.stderr.flush()

    print_summary(feature_count, seq_count, bad_triplet, zero_length, size_mismatch)
    return seqs


def parse_feature(feature, seq_record, source):
    '''Parse a Seq object to extract nuc sequence, translated pep and COG.

    Depending on the source of the genbank file, NCBI or RAST being the
    two most common, unique feature IDs to use may be found in different
    locations wtihin the Genbank.

    NCBI: 'protein_id'
    RAST: 'product'

    n.b. In this case we're using seed_xref as the unique id.
    Returns a dict with keys:
    * nuc
    * pep

    Also returns strings for error cases.
    '''
    nuc = feature.extract(seq_record).seq
    if len(str(nuc)) % 3:
        raise ValueError('bad_triplet')
    elif len(str(nuc)) == 0:
        raise ValueError('zero_length')

    description = read_description(feature.qualifiers, source)

    try:
        pep, seed_xref = parse_pep(feature, nuc, source)
    except StandardError as err:
        # pat = ('Size mismatch between pep (%d) and nuc '
        #        '(nuc was %d, expected %d) in %s. Skipping')
        # print(pat % (len(pep), len(nuc), len(pep) * 3, seed_xref))
        raise ValueError('size_mismatch')

    return dict(nuc=str(nuc),
                pep=str(pep),
                description=description,
                cog='-',
                seed_xref=seed_xref,)


def read_description(qualifiers, source):
    if source == 'kbase':
        if 'function' in qualifiers.keys():
            desc = qualifiers['function'][0]
        else:
            desc = 'no function'
    else:
        desc = qualifiers['product'][0]
    return desc


def parse_pep(feature, nuc, source):
    if source == 'kbase':
        if len(str(nuc)) % 3:
            raise ValueError("Nuc can't be translated - not divisible by 3")
        else:
            pep = nuc.translate()
        seed_xref = feature.qualifiers['kbase_id'][0]
    elif source == 'auto':
        if 'protein_id' in feature.qualifiers:
            seed_xref = feature.qualifiers['protein_id'][0]
            pep_str = feature.qualifiers['translation'][0]
            if not pep_str.endswith('*'):
                pep_str += '*'
            pep = Seq(pep_str)
        elif 'db_xref' in feature.qualifiers:
            seed_xref = feature.qualifiers['db_xref'][0]
            if 'translation' in feature.qualifiers.keys():
                pep_str = feature.qualifiers['translation'][0]
                if not pep_str.endswith('*'):
                    pep_str += '*'
                pep = Seq(pep_str)
            else:
                pep = nuc.translate()
        elif 'locus_tag' in feature.qualifiers:
            seed_xref = feature.qualifiers['locus_tag'][0]
            if 'translation' in feature.qualifiers.keys():
                pep_str = feature.qualifiers['translation'][0]
                if not pep_str.endswith('*'):
                    pep_str += '*'
                pep = Seq(pep_str)
            else:
                pep = nuc.translate()
        else:
            pepmsg = 'Feature must contain at least one of the following:\n'
            pepmsg += '"protein_id", "db_xref", "locus_tag"\n'
            raise KeyError(pepmsg)

    if len(str(nuc)) != len(str(pep)) * 3:
        raise ValueError('not divisble by 3')

    return pep, seed_xref


def print_summary(feature_count, seq_count, bad_triplet, zero_length, size_mismatch):
    print('\nRead a total of %d coding sequences (CDS) on %d sequences.' %
          (feature_count, seq_count))
    err_pat = ('Of those %d (%.02f%%) appeared to be an incorrect nucleic '
               'acid length (not divisible by 3), %d (%.02f%%) were 0-length, '
               'and %d (%.02f%%) had a mismatched length between na and aa')
    err_args = (bad_triplet, 100 * bad_triplet / float(feature_count),
                zero_length, 100 * zero_length / float(feature_count),
                size_mismatch, 100 * size_mismatch / float(feature_count))
    print(err_pat % err_args)


def infer_source(infile):
    raise NotImplemented()


# RPS Constants
RPSBLAST_DB = os.path.expanduser('~/Downloads/Cog_LE/Cog')
RPSBLAST_EXE = '/usr/local/bin/rpsblast'
E_VALUE_THRESH = 1E-5

def lookup_cog(pep_fa):
    '''Lookup COG groups for functions preferred by PGAP

    nb Even when .func is provided correctly, PGAP doesn't seem to use it,
    so this step is usually skipped because it takes time and doesn't help.

    However, the rpsblast does run successfully, so I'm leaving the code in
    in case it is useful in the future. It's certainly fragile (e.g. exe path
    is hard-coded) but could be hardened with a little work.
'''
    if not os.path.exists(RPSBLAST_DB + '.rps'):
        setup_cog_le(RPSBLAST_DB)

    # Run rpsblast
    cline = NcbirpsblastCommandline(cmd=RPSBLAST_EXE,
                                    db=RPSBLAST_DB,
                                    query=pep_fa,
                                    evalue=E_VALUE_THRESH,
                                    outfmt=5,
                                    max_target_seqs=1)
    # Option num_threads max value == number of
    # databases, so 1 in this case. Misleading
    # to even include it in the options.

    print('')
    print('Running rpsblast to lookup COGs...')
    print(cline)
    stdout, stderr = cline()

    # Parse rpsblast output
    cog_pat = re.compile('COG\d{4}')
    index = []
    cogs_list = []
    print('Parsing blast output...')
    for record in NCBIXML.parse(StringIO(stdout)):  # open('fmt5.xml', 'r')
        # print "QUERY: %s" % record.query
        for align in record.alignments:
            # print " MATCH: %s..." % align.title[:60]
            # print align
            match = cog_pat.search(align.title)
            if match:
                index.append(record.query)
                cog = match.group()
                cogs_list.append(cog)

    print('Successfull lookup for %d CDS' % len(cogs_list))
    cogs = pd.Series(cogs_list, index)


    return cogs


def default_outfile(fname, sanitize_fname=False):
    # Split Filename
    pth = os.path.dirname(fname)
    fbase = os.path.basename(fname)
    if fbase.endswith('.gz'):
        fbase = fbase[:-3]  # Strip gz first
    base, ext = os.path.splitext(fbase)
    # print pth, base, ext

    if sanitize_fname:
        base = base.replace(' ', '')
    return base, ext


def setup_cog_le(rpsblast_db_path):
    '''Download and Prepare COG LE Database

    COG Position Specific Scoring Matricies (PSSM) exist to help lookup COG
    groups using RPSBlast. Download and set them up here.

    Input: Path to the Cog database, as would be passed to rpsblast command
           line.

    Notes also from:
        * https://www.biostars.org/p/137151/
    '''
    rpsblast_dir = os.path.dirname(rpsblast_db_path)
    cog_filename = 'Cog_LE.tar.gz'
    cog_url = (
        'ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/' + cog_filename)
    print('Downloading COG Database %s; please wait' % cog_url)
    try:
        tempdir = tempfile.mkdtemp()
        print(tempdir)

        # Download and save tar
        cog_file = os.path.join(tempdir, cog_filename)
        r = urllib2.urlopen(cog_url)
        with open(cog_file, 'w') as f:
            f.write(r.read())

        # Decompress and move to target location
        tar = tarfile.TarFile.open(cog_file)
        tar.extractall(tempdir)
        shutil.move(tempdir, rpsblast_dir)
        readme_msg = 'Downloaded on %s from %s' % (datetime.date.today(),
                                                   cog_url)
        with open(os.path.join(rpsblast_dir, 'README.md'), 'w') as f:
            f.write(readme_msg)
    finally:
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
