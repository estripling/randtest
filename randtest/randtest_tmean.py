"""
Make Randomization test with trimmed mean difference (`randtest-tmean`)
available on the command line.
"""

from functools import partial
from .base import randtest, test_statistic
from .mcts import trimmed_mean
from .argparser_bp import read_data, argparse_cli


def main():
    """Main function"""
    description = """
    Randomization test for the comparison of trimmed means computed
    based on two independent samples gathered in a controlled experiment.
    """
    parser = argparse_cli(description)
    parser.add_argument(
        "-t",
        metavar="[0-49]",
        type=int,
        choices=range(0, 50),
        default=20,
        help="value in percent used for trimming (default: 20)."
    )
    args = parser.parse_args()
    alpha = args.t / 100
    # Use functools.partial to set parameters
    tmean = partial(trimmed_mean, trim_percent=alpha)

    data_group_a = read_data(args.fname_data_A)
    data_group_b = read_data(args.fname_data_B)

    result = randtest(
        data_group_a=data_group_a,
        data_group_b=data_group_b,
        mct=tmean,
        tstat=test_statistic,
        num_permutations=args.p,
        alternative=args.a,
        num_jobs=args.n,
        log_level=args.l,
        seed=args.s)
    print(result)


if __name__ == '__main__':
    main()
