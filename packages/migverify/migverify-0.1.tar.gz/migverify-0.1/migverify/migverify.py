'''
A class to deal with Migrate-N infile
'''

import collections
import math
import re
import logging
import gettext
import shutil
import datetime


class Infile:
    '''
    A class to parse a migrate infile
    '''
    def __init__(self, path):
        self.path = path

    def _get_handle(self):
        '''
        Makes sure the file is open, and that it is always at the
        right spot.
        '''
        handle = getattr(self, "handle", None)
        if handle is None:
            self.open()
            handle = getattr(self, "handle", None)
        handle.seek(0)
        return handle

    def open(self):
        '''
        Open file and return handle
        '''
        logging.info(f"Opening {self.path}.")
        try:
            self.handle = open(self.path, 'rt')
        except OSError:
            logging.critical(f'Could not open {self.path}')
        except:
            logging.criticial(f'Unexpected error when opening {self.path}')
            raise

    def parse_first_line(self):
        logging.info("Parsing header line.")
        handle = self._get_handle()
        first_line = handle.readline()
        first_line = first_line.strip().split()
        self.n_pop = int(first_line[0])
        self.n_loci = int(first_line[1])
        self.title = first_line[2]
        logging.info(f"Found {self.n_pop}"
                     f" {gettext.ngettext('population', 'populations', self.n_pop)}.")
        logging.info(f"Found {self.n_loci}"
                     f" {gettext.ngettext('locus', 'loci', self.n_loci)}.")

    def parse_loci_sizes(self):
        logging.info("Parsing size of loci.")
        handle = self._get_handle()
        second_line = handle.readlines()[1]
        self.loci_sizes = [int(s) for s in second_line.strip().split()]

    def parse_populations(self, max_prop_missing_loci=0.1):
        logging.info("Parsing population data.")
        handle = self._get_handle()
        loci = {k: {'seq': set(), 'pop': collections.defaultdict(str),
                    'size': self.loci_sizes[i]}
                for k, i in [(f'Loc{i}', i) for i in range(self.n_loci)]}
        for n, l in enumerate(handle):
            if n > 1:  # skipping header lines
                try:
                    # attempt to split the string, if ok
                    # attempt to make the first element of the split
                    # string into an int
                    # if these two are ok, then it is very likely this
                    # is a population delimiter, and proceed.
                    # if it fails, then see if it is a sample
                    n_samples_str, pop_name_tmp = l.strip().split()
                    n_samples = int(n_samples_str)
                    pop_name = pop_name_tmp
                    line_no = 0
                except:
                    if len(l.strip()) == 0:
                        # if it is an empty line: skip
                        continue
                    # otherwise, find out the locus number with
                    # a bit of math. The math is at base 0, so
                    # must add 1 to line_no after figuring out
                    # the current locus
                    loc = f'Loc{math.floor(line_no/n_samples)}'
                    line_no += 1
                    sample, hap = l.strip().split()
                    if self.exclude_sample(hap,
                                           max_prop_missing_loci=max_prop_missing_loci):
                        # skip sample if I need to exclude it because
                        # of missing data.
                        logging.warning(f"{loc} did not meet minimum data"
                                        " requirements.")
                        loci[loc]['include'] = False
                        # continue
                    loci[loc]['pop'][pop_name] += l
                    loci[loc]['seq'].add(hap)
        self.loci = loci

    def exclude_loci(self, min_haplotypes=4):
        '''
        Tag loci with fewer than min_haplotypes haplotypes to be
        excluded from the final file
        '''
        logging.info(f"Checking if loci meet minimum diversity"
                     f" requirement of {min_haplotypes}")
        for l in self.loci:
            if 'include' in self.loci[l] and not self.loci[l]['include']:
                logging.warning(f'Loc {l} is being skipped.')
                continue
            if len(self.loci[l]['seq']) >= min_haplotypes:
                self.loci[l]['include'] = True
            else:
                logging.warning(f"Locus {l} did not meet minimum diversity"
                                " requirements.")
                self.loci[l]['include'] = False

    def exclude_sample(self, hap, max_prop_missing_loci=0.1):
        '''
        If individual has more missing data than allowed, remove from
        the final dataset
        '''
        miss_dat_pat = re.compile(r'-|N')
        hap_len = len(hap)
        n_miss_data = len(miss_dat_pat.findall(hap))
        prop_miss_data = n_miss_data/hap_len
        logging.debug(f"Proportion missing data {prop_miss_data}.")
        if prop_miss_data > max_prop_missing_loci:
            logging.warning(f"Locus had more than {max_prop_missing_loci}"
                            " proportion missing data.")
            return True
        else:
            return False

    def output_filtered_loci(self):
        '''
        Output a fixed infile
        '''
        shutil.copy(self.path, self.path+'.bk')
        fn = open('infile_clean', 'wt')
        nloc_included = 0
        today = datetime.date.today().strftime('%Y-%m-%d')
        title = self.title + f' FIXED on {today}'
        locus_sizes = []
        pops = collections.defaultdict(collections.defaultdict)
        for l in self.loci:
            if self.loci[l]['include']:
                nloc_included += 1
                locus_sizes.append(f"{self.loci[l]['size']}")
                for p in self.loci[l]['pop']:
                    samples = self.loci[l]['pop'][p]
                    try:
                        pops[p]['samples'] += samples
                    except:
                        pops[p]['samples'] = samples
                    pops[p]['size'] = len(samples.split('\n')) - 1
        fn.write(f"{len(pops)} {nloc_included} {title}\n")
        fn.write(' '.join(locus_sizes)+'\n')
        for p in pops:
            pop_line = f"{pops[p]['size']} {p}"
            samples = pops[p]['samples']
            fn.write('\n'.join([pop_line, samples]))
        fn.close()
