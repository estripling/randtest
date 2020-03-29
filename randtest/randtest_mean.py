"""
Make Randomization test with mean difference (`randtest-mean`)
available on the command line.
"""

from statistics import mean
from .base import randtest, test_statistic
from .argparser_bp import read_data, argparse_cli


def main():
    """Main function"""
    description = """
    Randomization test for the comparison of arithmetic means computed
    based on two independent samples gathered in a controlled experiment.
    """
    parser = argparse_cli(description)
    args = parser.parse_args()
    data_group_a = read_data(args.fname_data_A)
    data_group_b = read_data(args.fname_data_B)
    result = randtest(
        data_group_a=data_group_a,
        data_group_b=data_group_b,
        mct=mean,
        tstat=test_statistic,
        num_permutations=args.p,
        alternative=args.a,
        num_jobs=args.n,
        log_level=args.l,
        seed=args.s)
    print(result)


if __name__ == '__main__':
    main()
