import os
import argparse
from pyats.easypy import run

# script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main():
    '''job file entrypoint'''

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_model_dir', type=str, default=None)
    args, _ = parser.parse_known_args()

    # run script
    run(testscript=os.path.join(SCRIPT_PATH, 'pyats_aetest.py'), data_model_dir=args.data_model_dir)
