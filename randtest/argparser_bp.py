"""
argparse boilerplate code
"""

import ast
import argparse
import textwrap
from randtest import __version__


def read_data(ifname):
    """Read in data: assuming no header, only numbers"""
    with open(ifname, 'r') as fobj:
        data = (
            ast.literal_eval(num.strip())
            for num in fobj.readlines()
        )
    return data


def argparse_cli(description):
    """argparse boilerplate code"""
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(description)
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        #  version="%(prog)s " + __version__,
        version=__version__,
    )
    parser.add_argument(
        "-a",
        metavar="alternative",
        type=str,
        choices=["two_sided", "greater", "less"],
        default="two_sided",
        help="alternative hypothesis (default: 'two_sided')."
    )
    parser.add_argument(
        "-p",
        metavar="num_permutations",
        type=int,
        default=10000,
        help="number of permutations (default: 10000)."
    )
    parser.add_argument(
        "-n",
        metavar="num_jobs",
        type=int,
        default=1,
        help="number of jobs (default: 1)."
    )
    parser.add_argument(
        "-l",
        metavar="log_level",
        type=str,
        choices=["debug", "info", "warn", "error", "critical"],
        default="warn",
        help="set log level (default: 'warn')."
    )
    parser.add_argument(
        "-s",
        metavar="seed",
        type=int,
        default=None,
        help="seed to initialize the random number generator (default: None)",
    )

    parser.add_argument(
        "fname_data_A",
        type=str,
        help="file name group A data.",
    )
    parser.add_argument(
        "fname_data_B",
        type=str,
        help="file name group B data.",
    )
    return parser
