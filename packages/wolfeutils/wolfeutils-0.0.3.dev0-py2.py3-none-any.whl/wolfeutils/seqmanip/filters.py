'''Filters to remove sequences or adjust sequence headers'''
from Bio.Seq import Seq
from Bio import SeqIO


def filterFastq(input_handle, output_handle, seqids, reverse_complement=False):
    if reverse_complement:
        seqids = [str(Seq(sequence).reverse_complement())
                  for sequence in seqids]
    sequences = SeqIO.parse(input_handle, 'fastq')
    for seq in sequences:
        match = False
        for target in seqids:
            if target in seq.description:
                match = True
        if match:
            SeqIO.write(seq, output_handle, 'fastq')
