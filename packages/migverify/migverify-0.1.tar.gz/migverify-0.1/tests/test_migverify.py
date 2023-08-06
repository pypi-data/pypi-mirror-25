'''
Test migverify
'''

import unittest
import io
from migverify import migverify


class TestMigverify(unittest.TestCase):
    '''
    The format:
      <n pops> <n loci> <title>
      <n sites locus 1> <n sites locus 2> ... <n sites locus n>
      <n inds locus 1> <n inds locus 2> ... <n inds locus n> <pop name>
      <ind 1 max 10 chars> <data locus 1>
      <ind 2 max 10 chars> <data locus 1>
      <ind 1 max 10 chars> <data locus 2>
    '''
    def setUp(self):
        self.infile_good = io.StringIO(
            '''  2 2 Make believe data set using simulated data (2 loci)
50 46
3 pop1
eis ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
zwo ACACAAAACACGGCCCGCGGACAGGGGCTCGAGGGGTCACTGAGTGGCAC
drue ATACCCAGCACGGCCGGCGGACAGGGGCTCGAGGGAGCACTGAGTGGAAC
eis ACGCGGCGCGCGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
zwo ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
drue ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
2 pop2
vier CAGCGCGCGTATCGCCCCATGTGGTTCGGCCAAAGAATGGTAGAGCGGAG
fuef CAGCGCGAGTCTCGCCCCATGGGGTTAGGCCAAATAATGTTAGAGCGGCA
vier TCGACTAGATCTGCAGCACATACGAGGGTCATGCGTCCCAGATGTG
fuefLoc2 TCGACTAGATATGCAGCAAATACGAGGGGCATGCGTCCCAGATGTG
        ''')
        self.infile_first_locus_mono = io.StringIO(
            '''  2 2 Make believe data set using simulated data (2 loci)
50 46
3 pop1
eis ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
zwo ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
drue ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
eis ACGCGGCGCGCGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
zwo ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
drue ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
2 pop2
vier ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
fuef ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
vier TCGACTAGATCTGCAGCACATACGAGGGTCATGCGTCCCAGATGTG
fuefLoc2 TCGACTAGATATGCAGCAAATACGAGGGGCATGCGTCCCAGATGTG
''')
        self.infile_missing_data = io.StringIO(
            '''  2 2 Make believe data set using simulated data (2 loci)
50 46
3 pop1
eis ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC
zwo ACACAAAACACGGCCCGCGGACAGGGGCTCGAGGGGTCACTGAGTGGCAC
drue ATACCCAGCACGGCCGGCGGACAGGGGCTCGAGGGAGCACTGAGTGGAAC
eis ACGCGGCGCGCGAACGNNNACCAAATCTTCTTGATCCCCAAGTGTC
zwo ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
drue ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC
2 pop2
vier CAGCGCGCGTATCGCCCCATGTGGTTCGGCCAAAGAATGGTAGAGCGGAG
fuef CAGCGCGAGTCTCGCCCCATGGGGTTAGGCCAAATAATGTTAGAGCGGCA
vier TCGACTAGATCT------CATACGAGGGTCATGCGTCCCAGATGTG
fuefLoc2 TCGACTAGATATGCAGCAAATACGAGGGGCATGCGTCCCAGATGTG
        ''')
        self.locus_one_poly = list(['ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC', 'CAGCGCGAGTCTCGCCCCATGGGGTTAGGCCAAATAATGTTAGAGCGGCA', 'ACACAAAACACGGCCCGCGGACAGGGGCTCGAGGGGTCACTGAGTGGCAC', 'CAGCGCGCGTATCGCCCCATGTGGTTCGGCCAAAGAATGGTAGAGCGGAG', 'ATACCCAGCACGGCCGGCGGACAGGGGCTCGAGGGAGCACTGAGTGGAAC'])
        self.locus_one_mono = list(['ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC'])
        self.locus_two_poly = list(['ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC', 'ACGCGGCGCGCGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC', 'TCGACTAGATATGCAGCAAATACGAGGGGCATGCGTCCCAGATGTG', 'TCGACTAGATCTGCAGCACATACGAGGGTCATGCGTCCCAGATGTG'])
        self.obj = migverify.Infile(path=None)
        self.locus_one_poly_pop1 = 'eis ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\nzwo ACACAAAACACGGCCCGCGGACAGGGGCTCGAGGGGTCACTGAGTGGCAC\ndrue ATACCCAGCACGGCCGGCGGACAGGGGCTCGAGGGAGCACTGAGTGGAAC\n'
        self.locus_one_poly_pop2 = 'vier CAGCGCGCGTATCGCCCCATGTGGTTCGGCCAAAGAATGGTAGAGCGGAG\nfuef CAGCGCGAGTCTCGCCCCATGGGGTTAGGCCAAATAATGTTAGAGCGGCA\n'
        self.locus_one_mono_pop1 = 'eis ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\nzwo ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\ndrue ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\n'
        self.locus_one_mono_pop2 = 'vier ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\nfuef ACACCCAACACGGCCCGCGGACAGGGGCTCGAGGGATCACTGACTGGCAC\n'
        self.locus_two_poly_pop1 = 'eis ACGCGGCGCGCGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC\nzwo ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC\ndrue ACGCGGCGCGAGAACGAAGACCAAATCTTCTTGATCCCCAAGTGTC\n'
        self.locus_two_poly_pop2 = 'vier TCGACTAGATCTGCAGCACATACGAGGGTCATGCGTCCCAGATGTG\nfuefLoc2 TCGACTAGATATGCAGCAAATACGAGGGGCATGCGTCCCAGATGTG\n'

    def test_parse_first_line(self):
        '''
        Test the parse_first_line function. It should return two
        new attributtes to the object, an n_pop with the correct number
        of populations, and an n_loci with the correct number of
        loci in the file.
        '''
        self.obj.handle = self.infile_good
        self.obj.parse_first_line()
        self.assertEqual(self.obj.n_pop, 2, 'Failed test that number of populations was 2.')
        self.assertEqual(self.obj.n_loci, 2, 'Failed test that number of loci was 2.')

    def test_parse_loci_size(self):
        '''
        Test the parse_loci_sizes function. It should return two
        new attributtes to the object, an n_pop with the correct number
        of populations, and an n_loci with the correct number of
        loci in the file.
        '''
        self.obj.handle = self.infile_good
        self.obj.parse_loci_sizes()
        self.assertEqual([50, 46], self.obj.loci_sizes, 'Failed test that loci lengths match expected values.')

    def test_parse_population_all_polymorphic(self):
        '''
        Test if correctly parses all loci when they are polymorphic.
        '''
        self.obj.handle = self.infile_good
        self.obj.n_loci = 2
        self.obj.n_pop = 2
        self.obj.loci_sizes = [50, 46]
        self.obj.parse_populations()
        self.assertEqual(5, len(self.obj.loci['Loc0']['seq']), msg=f'Failed test that length of number of haplotypes is 5 for first locus')
        self.assertEqual(4, len(self.obj.loci['Loc1']['seq']), msg=f'Failed test that length of number of haplotypes is 4 for second locus')
        self.assertTrue(all([hap in self.obj.loci['Loc0']['seq'] for hap in self.locus_one_poly]), msg='Failed test to assert that a haplotype in locus 1 is found in the set of found haplotypes')
        self.assertTrue(all([hap in self.obj.loci['Loc1']['seq'] for hap in self.locus_two_poly]), msg='Failed test to assert that a haplotype in locus 1 is found in the set of found haplotypes')
        self.assertEqual(self.locus_one_poly_pop1, self.obj.loci['Loc0']['pop']['pop1'])
        self.assertEqual(self.locus_one_poly_pop2, self.obj.loci['Loc0']['pop']['pop2'])
        self.assertEqual(self.locus_two_poly_pop1, self.obj.loci['Loc1']['pop']['pop1'])
        self.assertEqual(self.locus_two_poly_pop2, self.obj.loci['Loc1']['pop']['pop2'])

    def test_parse_population_one_monorphic(self):
        '''
        Test if it will correctly identify a monomorphic locus
        '''
        self.obj.handle = self.infile_first_locus_mono
        self.obj.n_loci = 2
        self.obj.n_pop = 2
        self.obj.loci_sizes = [50, 46]
        self.obj.parse_populations()
        self.assertEqual(1, len(self.obj.loci['Loc0']['seq']), msg = f'Failed test that length of number of haplotypes is 5 for first locus')
        self.assertEqual(4, len(self.obj.loci['Loc1']['seq']), msg = f'Failed test that length of number of haplotypes is 4 for second locus')
        self.assertTrue(all([hap in self.obj.loci['Loc0']['seq'] for hap in self.locus_one_mono]), msg = 'Failed test to assert that a haplotype in locus 1 is found in the set of found haplotypes')
        self.assertTrue(all([hap in self.obj.loci['Loc1']['seq'] for hap in self.locus_two_poly]), msg = 'Failed test to assert that a haplotype in locus 1 is found in the set of found haplotypes')
        self.assertEqual(self.locus_one_mono_pop1, self.obj.loci['Loc0']['pop']['pop1'])
        self.assertEqual(self.locus_one_mono_pop2, self.obj.loci['Loc0']['pop']['pop2'])
        self.assertEqual(self.locus_two_poly_pop1, self.obj.loci['Loc1']['pop']['pop1'])
        self.assertEqual(self.locus_two_poly_pop2, self.obj.loci['Loc1']['pop']['pop2'])

    def test_exclude_sample(self):
        '''
        Test if correct excluding samples bases on proportion
        '''
        self.assertTrue(self.obj.exclude_sample(hap='ATNN', max_prop_missing_loci = 0.1))
        self.assertFalse(self.obj.exclude_sample(hap='AAAAAAAAAN', max_prop_missing_loci = 0.1))
        self.assertTrue(self.obj.exclude_sample(hap='AT--', max_prop_missing_loci = 0.1))
        self.assertFalse(self.obj.exclude_sample(hap='AAAAAAAAA-', max_prop_missing_loci = 0.1))

    def test_exclude_loci(self):
        '''
        Test if it will correctly filters out a monomorphic locus
        '''
        self.obj.handle = self.infile_first_locus_mono
        self.obj.n_loci = 2
        self.obj.n_pop = 2
        self.obj.loci_sizes = [50, 46]
        self.obj.parse_populations()
        self.obj.exclude_loci()
        self.assertFalse(self.obj.loci['Loc0']['include'], msg='FAILED: Locus 0 is monomorphic, and should NOT be included.')
        self.assertTrue(self.obj.loci['Loc1']['include'], msg='FAILED: Locus 1 is polymorphic and SHOULD be included')


if __name__ == "__main__":
    unittest.main()
