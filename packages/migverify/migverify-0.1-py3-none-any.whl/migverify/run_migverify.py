'''
An entrypoint for migverify
'''

import click
import logging

from .migverify import Infile


@click.command()
@click.argument("infile")
@click.option("--min_haplotypes", "-m", default=2,
              help="Minimum number of haplotypes",
              show_default=True)
@click.option("--max_prop_missing_loci", "-p", default=0.1,
              help="Maximum proportion of missing data at a sample",
              show_default=True)
@click.option("--debug", "-d", is_flag=True)
def migverify(infile, min_haplotypes, max_prop_missing_loci, debug):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)
    verify = Infile(infile)
    verify.open()
    verify.parse_first_line()
    verify.parse_loci_sizes()
    verify.parse_populations(max_prop_missing_loci=max_prop_missing_loci)
    verify.exclude_loci(min_haplotypes=min_haplotypes)
    verify.output_filtered_loci()


if __name__ == '__main__':
    migverify()
