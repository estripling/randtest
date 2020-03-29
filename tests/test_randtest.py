"""
Unit tests for randtest
"""

import unittest
import subprocess
from types import GeneratorType
from randtest import randtest
from randtest.mcts import (
    arithmetic_mean,
    trimmed_mean,
)


class TestRandTest(unittest.TestCase):
    """Unittesting randtest()"""

    def test_randtest_systematic_twosided(self):
        """Simple functionality test: systematic, two_sided randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_greater(self):
        """Simple functionality test: systematic, greater randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="greater",
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_less(self):
        """Simple functionality test: systematic, less randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="less",
        )
        self.assertEqual(1, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_twosided(self):
        """Multiproc. functionality test: systematic, two_sided randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="two_sided",
            num_jobs=-1,
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_greater(self):
        """Multiproc. functionality test: systematic, greater randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="greater",
            num_jobs=-1,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_systematic_multiproc_less(self):
        """Multiproc. functionality test: systematic, less randtest()"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            num_permutations=-1,
            alternative="less",
            num_jobs=-1,
        )
        self.assertEqual(1, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug(self):
        """Smart drug data: systematic, two_sided randtest()"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            num_permutations=30,
            alternative="two_sided",
            num_jobs=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)

    def test_randtest_systematic_twosided_mct_func(self):
        """Test supplying a function to mct"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            mct=mct_func_mean,
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_mct_func_mean(self):
        """Smart drug data: systematic, two_sided randtest(): mct mean func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            mct=mct_func_mean,
            num_permutations=1000,
            alternative="two_sided",
            num_jobs=-1,
            seed=0,
        )
        self.assertEqual(128, test_result.num_successes)
        self.assertEqual(1000, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_mct_func_tmean(self):
        """Smart drug data: systematic, two_sided randtest(): mct tmean func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            mct=mct_func_trimmed_mean,
            num_permutations=1000,
            alternative="two_sided",
            num_jobs=-1,
            seed=0,
        )
        self.assertEqual(10, test_result.num_successes)
        self.assertEqual(1000, test_result.num_permutations)

    def test_randtest_systematic_twosided_tstat_func(self):
        """Test supplying a function to test statistic"""
        test_result = randtest(
            (5, 6),
            (8, 10),
            tstat=test_statistic_difference,
            num_permutations=-1,
            alternative="two_sided",
        )
        self.assertEqual(2, test_result.num_successes)
        self.assertEqual(6, test_result.num_permutations)

    def test_randtest_monte_multiproc_twosided_smartdrug_tstat_func(self):
        """Smart drug data: systematic, two_sided randtest(): tstat func"""
        with open("../data/smart_drug_data_treatment_group.dat", 'r') as fobj:
            group_a = tuple(int(val.strip()) for val in fobj.readlines())
        with open("../data/smart_drug_data_placebo_group.dat", 'r') as fobj:
            group_b = tuple(int(val.strip()) for val in fobj.readlines())
        test_result = randtest(
            group_a,
            group_b,
            tstat=test_statistic_difference,
            num_permutations=30,
            alternative="two_sided",
            num_jobs=-1,
            seed=42,
        )
        self.assertEqual(6, test_result.num_successes)
        self.assertEqual(30, test_result.num_permutations)

    def test_randtest_mean(self):
        """Test CLI: randtest-mean"""
        result = subprocess.run(
            [
                "randtest-mean",
                "-p -1",
                "../data/group_A.dat",
                "../data/group_B.dat",
            ],
            capture_output=True,
        )
        excepted_output = (
            "<class 'randtest.base.RandTestResult'>\n" +
            "Method = Systematic\n" +
            "Alternative = two_sided\n" +
            "MCT(data of group A) = 5.5\n" +
            "MCT(data of group B) = 9\n" +
            "Observed test statistic value = -3.5\n" +
            "Number of successes = 2\n" +
            "Number of permutations = 6\n" +
            "p value = 0.333333\n" +
            "seed = None\n"
        )
        self.assertEqual(excepted_output, result.stdout.decode("ascii"))

    def test_randtest_mean_smart_drug(self):
        """Test CLI: randtest-mean smart drug example"""
        result = subprocess.run(
            [
                "randtest-mean",
                "-s 0",
                "-p 1000",
                "../data/smart_drug_data_treatment_group.dat",
                "../data/smart_drug_data_placebo_group.dat",
            ],
            capture_output=True,
        )
        excepted_output = (
            "<class 'randtest.base.RandTestResult'>\n" +
            "Method = Monte Carlo\n" +
            "Alternative = two_sided\n" +
            "MCT(data of group A) = 101.915\n" +
            "MCT(data of group B) = 100.357\n" +
            "Observed test statistic value = 1.55775\n" +
            "Number of successes = 128\n" +
            "Number of permutations = 1000\n" +
            "p value = 0.128\n" +
            "seed = 0\n"
        )
        self.assertEqual(excepted_output, result.stdout.decode("ascii"))

    def test_randtest_tmean_smart_drug_percent20(self):
        """Test CLI: randtest-tmean (20 percent) smart drug example"""
        result = subprocess.run(
            [
                "randtest-tmean",
                "-s 0",
                "-p 1000",
                "-t 20",
                "../data/smart_drug_data_treatment_group.dat",
                "../data/smart_drug_data_placebo_group.dat",
            ],
            capture_output=True,
        )
        excepted_output = (
            "<class 'randtest.base.RandTestResult'>\n" +
            "Method = Monte Carlo\n" +
            "Alternative = two_sided\n" +
            "MCT(data of group A) = 101.586\n" +
            "MCT(data of group B) = 100.538\n" +
            "Observed test statistic value = 1.04775\n" +
            "Number of successes = 10\n" +
            "Number of permutations = 1000\n" +
            "p value = 0.01\n" +
            "seed = 0\n"
        )
        self.assertEqual(excepted_output, result.stdout.decode("ascii"))

    def test_randtest_tmean_smart_drug_percent10(self):
        """Test CLI: randtest-tmean (10 percent) smart drug example"""
        result = subprocess.run(
            [
                "randtest-tmean",
                "-s 0",
                "-p 1000",
                "-t 10",
                "../data/smart_drug_data_treatment_group.dat",
                "../data/smart_drug_data_placebo_group.dat",
            ],
            capture_output=True,
        )
        excepted_output = (
            "<class 'randtest.base.RandTestResult'>\n" +
            "Method = Monte Carlo\n" +
            "Alternative = two_sided\n" +
            "MCT(data of group A) = 101.487\n" +
            "MCT(data of group B) = 100.529\n" +
            "Observed test statistic value = 0.957768\n" +
            "Number of successes = 64\n" +
            "Number of permutations = 1000\n" +
            "p value = 0.064\n" +
            "seed = 0\n"
        )
        self.assertEqual(excepted_output, result.stdout.decode("ascii"))



def mct_func_mean(data: GeneratorType) -> float:
    """MCT test function: mean"""
    # You are starting the pool before you define your function and classes,
    # that way the child processes cannot inherit any code. Move your pool
    # start up to the bottom and protect it with if __name__ == '__main__':
    # Then a lambda should work as well.
    #
    # HERE: define mct_func_mean function to be used
    return arithmetic_mean(data)


def mct_func_trimmed_mean(data: GeneratorType, trim_percent=.2) -> float:
    """MCT test function: trimmed mean"""
    return trimmed_mean(data, trim_percent)


def test_statistic_difference(data1, data2, mct) -> float:
    """Test function for test statistic: Difference between MCT"""
    return mct(data1) - mct(data2)


if __name__ == "__main__":
    unittest.main()
