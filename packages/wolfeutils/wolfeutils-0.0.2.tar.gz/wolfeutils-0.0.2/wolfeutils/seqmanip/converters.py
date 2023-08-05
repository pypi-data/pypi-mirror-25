# from Bio.Alphabet import generic_dna
# from Bio.Seq import Seq
from Bio import SeqIO
import gzip
import os.path
import re
import sys
from wolfeutils import base


def biopython_convert(fname,
                      in_format,
                      out_format,
                      expand_id=True,
                      compression='gz',
                      out_fname=None):
    """Usage: biopython_convert.py Ancestor.gb genbank embl"""

    input_handle = base.openFunc(fname, "rU")

    if fname.endswith('.gz'):
        fname_base = os.path.basename(fname[:-3])
    else:
        fname_base = os.path.basename(fname)

    if compression == 'gz':
        out_openfunc = gzip.open
    elif compression == 'uncompressed':
        out_openfunc = open
    else:
        raise StandardError('Output zip format not recognized: %s' %
                            compression)

    sequences = SeqIO.parse(input_handle, in_format)

    if out_format == 'genbank':
        count = 0
        for sequence in sequences:
            print(sequence.id, sequence.description)
            if not out_fname:
                out = base.fileslug(sequence.description) + out_format
            else:
                out = out_fname
            if compression and compression == 'gz' and not out.endswith('.gz'):
                out += '.gz'

            output_handle = out_openfunc(out, "w")
            SeqIO.write(sequence, output_handle, out_format)
            output_handle.close()
            count += 1
        print("Converted %i records" % count)
    else:
        if not out_fname:
            out = base.fileslug(fname_base) + '.' + out_format
        else:
            out = out_fname
            if compression and compression == 'gz':
                out_fname += '.gz'

        sys.stderr.write('Writing to ' + out)
        sys.stderr.flush()
        with base.smart_open(out_fname,
                             mode="w",
                             stream=sys.stdout) as output_handle:
            for sequence in sequences:
                # print(sequence.id, sequence.description)
                if expand_id:
                    sequence.id = sequence.description
                SeqIO.write(sequence, output_handle, out_format)
        # output_handle.close()

    input_handle.close()


def renameLocus(fname,
                out_fname='-',
                prefix='',
                ids=['id', 'name'],
                annotations={}, contig_pat=r'contig_?(\d+)'):
    '''Rename Genbanks with bad locus tags'''
    in_format = 'genbank'
    out_format = 'genbank'

    input_handle = base.openFunc(fname, "rU")

    if fname.endswith('.gz'):
        fname_base = os.path.basename(fname[:-3])
    else:
        fname_base = os.path.basename(fname)

    if out_fname.endswith('.gz'):
        compression = 'gz'
    else:
        compression = 'uncompressed'

    # if compression == 'gz':
    #     out_openfunc = gzip.open
    # elif compression == 'uncompressed':
    #     out_openfunc = open
    # else:
    #     raise StandardError('Output zip format not recognized: %s' % compression)

    # Special Handling: Cast Taxonomy annotation to list
    if 'taxonomy' in annotations.keys():
        annotations['taxonomy'] = [s.strip()
                                   for s in annotations['taxonomy'].split(';')]

    contig_pat = re.compile(contig_pat)

    sequences = SeqIO.parse(input_handle, in_format)

    if not out_fname:
        out = base.fileslug(fname_base) + '.' + out_format
    else:
        out = out_fname
        if (compression and compression == 'gz' and
                not out_fname.endswith('.gz')):
            out_fname += '.gz'

    sys.stderr.write('Writing to ' + out)
    sys.stderr.flush()
    with base.smart_open(out_fname,
                         mode="w",
                         stream=sys.stdout) as output_handle:
        for sequence in sequences:
            # print(sequence.id, sequence.description)
            match = contig_pat.search(sequence.description)
            if match:
                contig = match.groups()[0]
            else:
                raise StandardError('%s did not match %s' %
                                    (sequence.description, contig_pat))
            seqid = prefix + contig

            for id_label in ids:
                sequence.__setattr__(id_label, seqid)
                # sequence.name = seqid
                # sequence.id = seqid

            sequence.annotations.update(annotations)
            # for key, val in annotations.iteritems():
            #     sequence.annotations[key] = val
            # e.g.
            # sequence.annotations['data_file_division'] = 'BCT'
            # sequence.annotations['organism'] = 'Brachybacterium'
            # sequence.annotations['taxonomy'] = ['Bacteria', 'Terrabacteria group', 'Actinobacteria', 'Actinobacteria', 'Micrococcales', 'Dermabacteraceae']

            SeqIO.write(sequence, output_handle, out_format)
    # output_handle.close()

    input_handle.close()


def cleanAnnotationsList(annotations):
    '''Clean a list of colon-separated fields to create an annotations dict'''
    new_annot = {}
    for annot in annotations:
        k, v = annot.split(':')
        new_annot[k] = v
    return new_annot
