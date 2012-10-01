#!/usr/bin/env python
import numpy as np
from scipy.io import savemat

from mldata import parse_c45

def main(dataset, inputdir='.', outputfile=None):
    if outputfile is None:
        outputfile = dataset
    examples = parse_c45(dataset, inputdir)
    X = np.array(examples.to_float(), dtype=float)
    savemat(outputfile, {dataset: X})

if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(usage="Usage: %prog [options] dataset")
    parser.add_option('-d', '--input-dir', dest='inputdir',
                      type='str', metavar='DIR', default='.')
    parser.add_option('-o', '--output-file', dest='outputfile',
                      type='str', metavar='FILE', default=None)
    options, args = parser.parse_args()
    options = dict(options.__dict__)
    if len(args) != 1:
        parser.print_help()
        exit()
    options['dataset'] = args[0]
    main(**options)
