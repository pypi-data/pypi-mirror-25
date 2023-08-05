# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from .version import __version__, __description__
from .zap import process, CFTYPE_OPTIONS


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__description__
    )
    addarg = parser.add_argument
    addarg('incube', help='Input datacube path')
    addarg('--version', '-V', action='version',
           version='%(prog)s ' + __version__)
    addarg('--debug', '-d', action='store_true',
           help='show debug info')
    addarg('--overwrite', action='store_true',
           help='overwrite output files if they already exists')
    addarg('--no-clean', action='store_true',
           help='disable NaN values interpolation')
    addarg('--ncpu', type=int, default=None,
           help='maximum number of cpus to use, all by default')
    addarg('--mask', help='mask file to exclude sources')
    addarg('--outcube', '-o', default='DATACUBE_FINAL_ZAP.fits',
           help='output datacube path')
    addarg('--skycube', help='output sky datacube path')
    addarg('--varcurve', help='output variance curves')
    addarg('--zlevel', default='median',
           help='method for the zeroth order sky removal: none, sigclip or '
           'median')
    addarg('--cftype', default='weight',
           help='method for the continuum filter: {}. For the '
           'weight method, a zeroth order sky is required (see zlevel)'
           .format(', '.join(CFTYPE_OPTIONS)))
    addarg('--cfwidthSVD', type=int, default=300,
           help='window size for the median or weight continuum filter, '
           'for the SVD computation')
    addarg('--cfwidthSP', type=int, default=300,
           help='window size for the median or weight continuum filter')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        process(
            args.incube, outcubefits=args.outcube, clean=not args.no_clean,
            skycubefits=args.skycube, mask=args.mask, zlevel=args.zlevel,
            cfwidthSVD=args.cfwidthSVD, cfwidthSP=args.cfwidthSP,
            cftype=args.cftype, overwrite=args.overwrite, ncpu=args.ncpu,
            varcurvefits=args.varcurve)
    except KeyboardInterrupt:
        sys.exit('Interrupted!')
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit('Failed to process file: %s' % e)


if __name__ == "__main__":
    main()
