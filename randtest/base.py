"""
Module: randtest

Implements:
 - Systematic randomization test
 - Monte Carlo randomization test

Allows for user-defined:
 - Test statistic
 - Measure of central tendency

"""

import random
import logging
import functools
import multiprocessing as mp
from types import FunctionType, GeneratorType
from itertools import combinations
from statistics import mean


class RandTestResult():
    """
    RandTestResult class

    Attributes
    ----------
        method : str
            Indicates type of randomization test.

        alternative : str
            Indicates the alternative.

        mcta : float
            Measure of central tendency of group A.

        mctb : float
            Measure of central tendency of group B.

        statistic : float
            Observed test statistic value.

        num_successes : int
            Number of successes within generated number of permutations
            according to the `alternative`. For example,
            if `alternative='two_sided'`, `num_successes` corresponds to the
            number of permutations where the absolute test statistic value is
            larger than or equal to the observed test statistic value.

        num_permutations : int
            Number of permutations.

        p_value : int
            The p value is equal to `num_successes / num_permutations`.

        seed : int, None,
    """

    def __init__(
            self,
            method: str,
            alternative: str,
            mcta: float,
            mctb: float,
            statistic: float,
            num_successes=0,
            num_permutations=0,
            seed=None):
        self._method = method
        self._alternative = alternative
        self._mcta = mcta
        self._mctb = mctb
        self._tobs = statistic
        self._nhits = num_successes
        self._nperms = num_permutations
        self._seed = seed

    @property
    def method(self) -> str:
        """Getter: method"""
        return self._method

    @property
    def alternative(self) -> str:
        """Getter: alternative"""
        return self._alternative

    @property
    def mcta(self) -> float:
        """Getter: mcta"""
        return self._mcta

    @property
    def mctb(self) -> float:
        """Getter: mctb"""
        return self._mctb

    @property
    def statistic(self) -> float:
        """Getter: statistic"""
        return self._tobs

    @property
    def num_successes(self) -> int:
        """Getter: num_successes"""
        return self._nhits

    @property
    def num_permutations(self) -> int:
        """Getter: num_permutations"""
        return self._nperms

    @property
    def p_value(self) -> float:
        """Getter: p_value"""
        return self.num_successes / self.num_permutations

    @property
    def seed(self) -> float:
        """Getter: seed"""
        return self._seed

    def __repr__(self):
        repr_string = "{}".format(
            self.__class__,
        )
        return repr_string

    def __str__(self):
        print_string = (
            "{}\n" +
            "Method = {}\n" +
            "Alternative = {}\n" +
            "MCT(data of group A) = {:g}\n" +
            "MCT(data of group B) = {:g}\n" +
            "Observed test statistic value = {:g}\n" +
            "Number of successes = {:d}\n" +
            "Number of permutations = {:d}\n" +
            "p value = {:g}\n"
            "seed = {}"
        ).format(
            self.__class__,
            self.method,
            self.alternative,
            self.mcta,
            self.mctb,
            self.statistic,
            self.num_successes,
            self.num_permutations,
            self.p_value,
            self.seed,
        )
        return print_string


class RandTest:
    """
    RandTest Class

    Carries out the computation of a randomization test.
    """
    def __init__(self,
                 data_group_a,
                 data_group_b,
                 mct,
                 tstat,
                 num_permutations,
                 alternative,
                 n_jobs,
                 seed):
        self.mct = mct
        self.tstat = tstat
        self.method = (
            "Monte Carlo"
            if num_permutations > 1 else
            "Systematic"
        )
        self.alternative = alternative
        self.njobs = n_jobs
        self.rng = check_random_state(seed)

        self.tobs = self.tstat(data_group_a, data_group_b, self.mct)
        self.data = data_group_a + data_group_b
        self.n_x = len(data_group_a)
        self.n_data = len(self.data)

        self.num_successes = 0
        self.num_permutations = num_permutations

    def compute_test_statistic(self, idx_group_a) -> bool:
        """Function to the multiprocessing computation of the test statistic"""
        idx_group_b = (
            i
            for i in range(self.n_data)
            if i not in idx_group_a
        )
        tval = self.tstat(
            (self.data[i] for i in idx_group_a),
            (self.data[j] for j in idx_group_b),
            self.mct,
        )
        if self.alternative == "two_sided":
            hit = abs(tval) >= abs(self.tobs)
        elif self.alternative == "greater":
            hit = tval >= self.tobs
        else:
            hit = tval <= self.tobs
        return hit

    def run(self):
        """Run the multiprocessing computation of randomization test."""
        if self.method == "Systematic":
            self.num_permutations = 0
            with mp.Pool(self.njobs) as pool:
                for is_success in pool.imap_unordered(
                        self.compute_test_statistic,
                        combinations(range(self.n_data), self.n_x)):
                    self.num_permutations += 1
                    self.num_successes += int(is_success)
                    self._log_progress()
        else:
            # Valid Monte Carlo Randomization Test includes observed tobs
            self.num_successes += 1
            with mp.Pool(self.njobs) as pool:
                for is_success in pool.imap_unordered(
                        self.compute_test_statistic,
                        self._get_random_indices()):
                    self.num_successes += int(is_success)
                    self._log_progress()

    def _log_progress(self):
        """Log Progress"""
        logging.info(
            "p value = %d / %d = %g",
            self.num_successes,
            self.num_permutations,
            self.num_successes / self.num_permutations,
        )

    def _get_random_indices(self):
        # Valid Monte Carlo Randomization Test includes observed tobs
        # Generate one random permutation less
        for _ in range(self.num_permutations - 1):
            yield self.rng.sample(range(self.n_data), self.n_x)


def test_statistic(
        data_group_a: GeneratorType,
        data_group_b: GeneratorType,
        mct: FunctionType) -> float:
    """Compute test statistic: Difference between MCTs"""
    return mct(data_group_a) - mct(data_group_b)


def check_random_state(seed):
    """
    Turn seed into a random.Random instance
    If seed is None, return the Random singleton used by random.
    If seed is an int, return a new Random instance seeded with seed.
    If seed is already a Random instance, return it.
    Otherwise raise ValueError.
    """
    # Code slightly adjusted from scikit-learn utils/validation.py
    if seed is None or isinstance(seed, int):
        rng = random.Random(seed)
    elif isinstance(seed, random.Random):
        rng = seed
    else:
        raise ValueError(
            "### error: '{}' cannot be used to seed random.Random instance."
            .format(seed)
        )
    return rng


def randtest(
        data_group_a,
        data_group_b,
        mct=mean,
        tstat=test_statistic,
        num_permutations=10000,
        alternative="two_sided",
        num_jobs=1,
        log_level="warn",
        seed=None):
    """
    Perform a randomization test with custom test statistic.

    data_group_a : tuple
        Data of group A.

    data_group_b : tuple
        Data of group B.

    mct : function
        Measure of central tendency to be computed in the test statistic.
        Default: mean().

    tstat : function
        Test statistic.
        Default: Difference between the mcts of the two groups.

    num_permutations : int
        Number of permutations to be carried out for the randomization test.
        If `num_permutations > 0`, a Monte Carlo randomization test is
        performed with the specified number of randomly generated data
        permutations.  If `num_permutations = -1`, a systematic randomization
        test is performed, meaning that all possible data permutations are
        generated.

    alternative : str
        Alternative hypothesis.
        Possible values: 'two_sided' (default), 'greater', and 'less'.

    num_jobs : int
        Number of jobs to carry out the computation.

    log_level : str
        Set log level.
        Possible values: 'debug', 'info', 'warn' (default), 'error',
        and 'critical'.

    seed : None, int, random.Random() instance

    Returns
    -------
    RandTestResult object with following attributes
        method : str
            Indicates type of randomization test.

        alternative : str
            Indicates the alternative.

        mcta : float
            Measure of central tendency of group A.

        mctb : float
            Measure of central tendency of group B.

        statistic : float
            Observed test statistic value

        num_successes : int
            Number of successes within generated number of permutations
            according to the `alternative`. For example,
            if `alternative='two_sided'`, `num_successes` corresponds to the
            number of permutations where the absolute test statistic value is
            larger than or equal to the observed test statistic value.

        num_permutations : int
            Number of permutations.

        p_value : int
            The p value is equal to `num_successes / num_permutations`.
    """
    if not isinstance(data_group_a, tuple):
        data_group_a = tuple(data_group_a)
    if not isinstance(data_group_b, tuple):
        data_group_b = tuple(data_group_b)
    assert isinstance(mct, (FunctionType, functools.partial))
    assert isinstance(tstat, FunctionType)
    assert isinstance(num_permutations, int) and num_permutations != 0
    if num_permutations < 0:
        assert num_permutations == -1
    assert (
        isinstance(alternative, str) and
        alternative in ["two_sided", "greater", "less"]
    )
    assert isinstance(num_jobs, int) and num_jobs != 0
    assert (
        isinstance(log_level, str) and
        log_level in ["debug", "info", "warn", "error", "critical"]
    )
    log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    logging.basicConfig(
        level=log_levels.get(log_level, logging.WARNING),
        format=(
            "%(levelname)s :: " +
            "%(name)s :: " +
            "pid = %(process)d :: " +
            "%(asctime)s :: " +
            "%(message)s"
        ),
        #  datefmt='%Y-%m-%d %H:%M:%S'
    )

    max_cores = mp.cpu_count()
    if num_jobs > 0:
        n_jobs = num_jobs
        if num_jobs > max_cores:
            logging.warning(
                "Specified number of jobs (%d) is larger than the " +
                "maximum number of cores (%d). " +
                "Setting number of jobs to %d.",
                num_jobs,
                max_cores,
                max_cores,
            )
            n_jobs = max_cores
    else:
        n_jobs = max_cores + num_jobs + 1
        if n_jobs <= 0:
            logging.warning(
                "Specified number of jobs (%d) goes beyond " +
                "the maximum number of cores (%d). " +
                "Setting number of jobs to %d.",
                num_jobs,
                max_cores,
                max_cores,
            )
            n_jobs = max_cores

    rtest = RandTest(
        data_group_a,
        data_group_b,
        mct,
        tstat,
        num_permutations,
        alternative,
        n_jobs,
        seed,
    )
    rtest.run()
    return RandTestResult(
        rtest.method,
        rtest.alternative,
        mct(data_group_a),
        mct(data_group_b),
        rtest.tobs,
        rtest.num_successes,
        rtest.num_permutations,
        seed,
    )
