from unittest import TestCase
import os.path

import wolfeutils.seqmanip.converters

thisDir, filename = os.path.split(os.path.abspath(__file__))
FIXTURES = os.path.join(thisDir, 'fixtures')

class TestGenbankToFastaConvert(TestCase):
    def test_genbank_to_fasta_convert(self):
        in_fasta = os.path.join(FIXTURES, 'P._paneum_FM227.gbk.gz')
        out_fname = '/tmp/tmp.faa'
        wolfeutils.seqmanip.converters.biopython_convert(
            fname=in_fasta, in_format='genbank', out_format='fasta',
            out_fname=out_fname, compression='uncompressed')
        self.assertTrue(os.path.exists(out_fname))
        # self.assertTrue(isinstance(s, basestring))

class TestFilterFastq(TestCase):
    def test_filter_fastq(self):
        pass
        # in_fasta = os.path.join(FIXTURES, 'P._paneum_FM227.gbk.gz')
        # out_fname = '/tmp/tmp.faa'
        # wolfeutils.seqmanip.converters.biopython_convert(
        #     fname=in_fasta, in_format='genbank', out_format='fasta',
        #     out_fname=out_fname, compression='uncompressed')
        # self.assertTrue(os.path.exists(out_fname))
        # # self.assertTrue(isinstance(s, basestring))
