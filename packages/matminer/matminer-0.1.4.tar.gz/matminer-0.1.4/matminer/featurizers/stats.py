"""
File containing general methods for computing property statistics
"""
import numpy as np
from scipy import stats

from six import string_types


# TODO: some of this needs a bit more cleanup. The kernel methods (requiring two lists) should
# probably go in a different class. Some of the method signatures are consistent, others aren't.
# Just needs a 15 minute cleanup check. -computron

class PropertyStats(object):

    @staticmethod
    def calc_stat(data_lst, stat, weights=None):
        """
        Compute a property statistic

        Args:
            data_lst (list of floats): list of values
            stat (str) - Name of property to be compute. If there are arguments to the statistics function, these
             should be added after the name and separated by two underscores. For example, the 2nd Holder mean would
             be "holder_mean__2"
            weights (list of floats): (Optional) weights for each element in data_lst
        Reteurn:
            float - Desired statistic
        """
        statistics = stat.split("__")
        return getattr(PropertyStats, statistics[0])(data_lst, weights, *statistics[1:])

    @staticmethod
    def minimum(data_lst, weights=None):
        """
        Minimum value in a list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (ignored)
        Returns: 
            minimum value
        """
        return min(data_lst) if float("nan") not in data_lst else float("nan")

    @staticmethod
    def maximum(data_lst, weights=None):
        """
        Maximum value in a list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (ignored)
        Returns: 
            maximum value
        """
        return max(data_lst) if float("nan") not in data_lst else float("nan")

    @staticmethod
    def range(data_lst, weights=None):
        """
        Range of a list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (ignored)
        Returns: 
            range
        """
        return (max(data_lst) - min(data_lst)) if float("nan") not in data_lst \
            else float("nan")

    @staticmethod
    def mean(data_lst, weights=None, **kwargs):
        """
        Mean of list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom or element in a compound
            weights (list of floats): Weights for each value
        Returns: 
            mean value
        """
        if weights is None:
            return np.average(data_lst)
        else:
            return np.dot(data_lst, weights) / sum(weights)

    @staticmethod
    def avg_dev(data_lst, weights=None):
        """
        Average absolute deviation of list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (list of floats): Atomic fractions
        Returns: 
            average absolute deviation
        """
        mean = PropertyStats.mean(data_lst, weights)
        return np.average(np.abs(np.subtract(data_lst, mean)), weights=weights)

    @staticmethod
    def std_dev(data_lst, weights=None):
        """
        Standard deviation of a list of element data
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (list of floats): Atomic fractions
        """
        if weights is None:
            return np.std(data_lst)
        else:
            dev = np.subtract(data_lst, PropertyStats.mean(data_lst, weights=weights))**2
            return np.sqrt(PropertyStats.mean(dev, weights=weights))

    @staticmethod
    def mode(data_lst, weights=None):
        """
        Mode of a list of element data. If multiple elements occur equally-frequently (or same weight, if weights are
        provided), this function will return the average of those values
        Args:
            data_lst (list of floats): Value of a property for each atom in a compound
            weights (list of floats): Atomic fractions
        Returns: 
            mode
        """
        if weights is None:
            return stats.mode(data_lst).mode[0]
        else:
            # Find the entry(s) with the largest weight
            data_lst = np.array(data_lst)
            weights = np.array(weights)
            most_freq = np.isclose(weights, weights.max())

            # Return the minimum of the most-frequent entries
            return data_lst[most_freq].min()

    @staticmethod
    def n_numerical_modes(data_lst, n, dl=0.1):
        """
        Returns the n first modes of a data set that are obtained with
            a finite bin size for the underlying frequency distribution.
        Args:
            data_lst ([float]): data values.
            n (integer): number of most frequent elements to be determined.
            dl (float): bin size of underlying (coarsened) distribution.
        Returns:
            ([float]): first n most frequent entries (or nan if not found).
        """
        if len(set(data_lst)) == 1:
            return [data_lst[0]] + [float('NaN') for _ in range(n-1)]
        hist, bins = np.histogram(data_lst, bins=np.arange(
                min(data_lst), max(data_lst), dl), density=False)
        modes = list(bins[np.argsort(hist)[-n:]][::-1])
        return modes + [float('NaN') for _ in range(n-len(modes))]

    @staticmethod
    def holder_mean(data_lst, weights=None, power=1):
        """
        Get Holder mean
        Args:
            data_lst: (list/array) of values
            weights: (list/array) of weights
            power: (int/float/str) which holder mean to compute
        Returns: Holder mean
        """

        if isinstance(power, string_types):
            power = float(power)

        if weights is None:
            if power == 0:
                return stats.mstats.gmean(data_lst)
            else:
                return np.power(np.mean(np.power(data_lst, power)), 1.0 / power)
        else:
            # Compute the normalization factor
            alpha = sum(weights)

            # If power=0, return geometric mean
            if power == 0:
                return np.product(np.power(data_lst, np.divide(weights, np.sum(weights))))
            else:
                return np.power(np.sum(np.multiply(weights, np.power(data_lst, power))) / alpha, 1.0/power)

    @staticmethod
    def sorted(data_lst):
        """
        Returns the sorted data_lst
        """
        return np.sort(data_lst)

    @staticmethod
    def eigenvalues(data_lst, symm = False, sort = False):
        """
        Return the eigenvalues of a matrix as a numpy array
        Args:
            data_lst: (matrix-like) of values
            symm: whether to assume the matrix is symmetric
            sort: wheter to sort the eigenvalues
        Returns: eigenvalues
        """
        eigs = np.linalg.eigvalsh(data_lst) if symm else np.linalg.eigvals(data_lst)
        if sort:
            eigs.sort()
        return eigs

    @staticmethod
    def flatten(data_lst):
        """oxi
        Returns a flattened copy of data_lst-as a numpy array
        """
        return np.array(data_lst).flatten()

    @staticmethod
    def laplacian_kernel(arr0, arr1, SIGMA):
        """
        Returns a Laplacian kernel of the two arrays
        for use in KRR or other regressions using the
        kernel trick.
        """
        diff = arr0 - arr1
        return np.exp(-np.linalg.norm(diff.A1, ord=1) / SIGMA)

    @staticmethod
    def gaussian_kernel(arr0, arr1, SIGMA):
        """
        Returns a Gaussian kernel of the two arrays
        for use in KRR or other regressions using the
        kernel trick.
        """
        diff = arr0 - arr1
        return np.exp(-np.linalg.norm(diff.A1, ord=2)**2 / 2 / SIGMA**2)
