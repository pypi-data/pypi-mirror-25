import argparse
import os
import sys
import wolfeutils.comparative.panseq.labelNewick
import wolfeutils.comparative.panseq.seqtools


#######################
# Create Panseq Fasta #
#######################
def createPanseqFastaArgs(args):
    parser = argparse.ArgumentParser(
        description='Create panseq-compatible fastas')
    parser.add_argument('infasta',
                        help='Fasta file to convert to panseq headers',
                        nargs='?',
                        default=sys.stdin)
    parser.add_argument('--contig-map', type=str)
    parser.add_argument(
        '--enumerate',
        action='store_true',
        help="Just label contigs by position; don't infer contig name")
    parser.add_argument('--label',
                        help='Label to use for re-written fasta header')
    parser.add_argument('--outname', help='Output name (defaults to stdout)')

    return parser.parse_args(args)


def createPanseqFastaCli():
    args = createPanseqFastaArgs(sys.argv[1:])
    wolfeutils.comparative.panseq.seqtools.main(**vars(args))


#######################
# Convert sequences   #
#######################
def convertSeqsArgs(args):
    parser = argparse.ArgumentParser(
        description='Convert sequences between formats')
    parser.add_argument('fname', help='Input file to convert')
    parser.add_argument('--in-format', help="Input format")
    parser.add_argument('--out-format', help="Output format")
    parser.add_argument('--out-fname', help="Output filename")
    parser.add_argument('--expand-id',
                        action='store_false',
                        help='Expand Sequence ID')
    parser.add_argument('--compression', '-c', choices=['gz', 'uncompressed'],  # maybe add bz2 later
                        default='gz', help='Output compression format')
    return parser.parse_args(args)


def convertSeqsCli():
    args = convertSeqsArgs(sys.argv[1:])
    wolfeutils.seqmanip.converters.biopython_convert(**vars(args))


#######################
# Filter Fastq        #
#######################
def filterFastqArgs(args):
    parser = argparse.ArgumentParser(
        description='Filter Fastq headers for specific strings')
    parser.add_argument('fastq',
                        help='Path to the input fastq file',
                        type=argparse.FileType('r'))
    parser.add_argument('--seq-ids',
                        nargs='+',
                        help="Keep any matching sequences")
    parser.add_argument('--out',
                        default=None,
                        type=argparse.FileType('w'),
                        help="Path to filtered fastq (defaults to stdout)")

    parser.add_argument('--reverse-complement',
                        action='store_true',
                        help="Reverse-complement targets before searching")
    return parser.parse_args(args)


def filterFastqCli():
    args = filterFastqArgs(sys.argv[1:])
    if not args.out:
        args.out = sys.stdout
    wolfeutils.seqmanip.filters.filterFastq(args.fastq, args.out, args.seq_ids,
                                            args.reverse_complement)


################
# Label Newick #
################
def labelNewickArgs(args):
    parser = argparse.ArgumentParser(
        description='Add otu labels to unlabeled tree as output by Panseq')
    parser.add_argument('treefile', help='Unlabeleld newick tree')
    parser.add_argument('namesfile',
                        help='Panseq phylip_name_conversion.txt file')
    parser.add_argument('--relabeled-tree',
                        type=argparse.FileType('w'),
                        help='Relabeled tree output name (defaults to stdout)')
    return parser.parse_args(args)


def labelNewickCli():
    args = labelNewickArgs(sys.argv[1:])
    tree = wolfeutils.comparative.panseq.labelNewick.labelTree(args.treefile,
                                                               args.namesfile)
    if args.relabeled_tree:
        args.relabeled_tree.write(tree)
    else:
        print(tree)  # Default write to stdout


##########################
# PGAP Standard Analysis #
##########################
def pgapBasicAnalysisCli():
    # Usage:
    # pgap_base_figures.py path/to/pgap/dir [path/to/annotated/genbanks]
    args = wolfeutils.comparative.pgap.workflows.parse_args(sys.argv[1:])
    pgap_dir = os.path.abspath(args.pgap_dir)
    wolfeutils.comparative.pgap.workflows.basicAnalysis(**vars(args))


################
# Rename Locus #
################
def renameLocusArgs(args):
    parser = argparse.ArgumentParser(
        description='Rename Locus Tags with usefull contig label')
    parser.add_argument('fname', help='Input file')
    parser.add_argument(
        '--annotations',
        '-a',
        action='append',
        help=
        'Extra annotations to add to Genbank metadata, colon separated. e.g. -a "organism:Brachybacterium"',
        default=[])
    parser.add_argument(
        '--contig-pat',
        '-c',
        default='contig_?(\d+)',
        help='Regular Expression Pattern to serach for contig number')
    parser.add_argument('--out_fname',
                        '-o',
                        default='-',
                        help='Output Filename (defaults to stdout)')
    parser.add_argument('--ids',
                        '-i',
                        default=['id', 'name'],
                        type=list,
                        help='ID fields to update')
    parser.add_argument('--prefix',
                        '-p',
                        default='contig',
                        help='Prefix to add in front of contig number')
    return parser.parse_args(args)


def renameLocusCli():
    args = renameLocusArgs(sys.argv[1:])
    # if not args.out:
    #     args.out = sys.stdout
    args.annotations = wolfeutils.seqmanip.converters.cleanAnnotationsList(
        args.annotations)
    wolfeutils.seqmanip.converters.renameLocus(**vars(args))
