""" This module defines the BrokenStick class
"""

import numpy as np


def weighted_moments(values, weights):
    """Return weighted mean and weighted standard deviation of a sequence"""

    w_mean = np.average(values, weights=weights)

    sq_err = (values - w_mean)**2
    w_var = np.average(sq_err, weights=weights)

    w_std = np.sqrt(w_var)

    return w_mean, w_std


def calc_broken_stick(dim):
    """Generate values for broken-stick distribution of certain length"""

    if dim < 1:
        raise ValueError('Boken stick dimension must be greater than 1')

    values = np.array([
        1.0 / (i + 1)
        for i in range(dim)
        ])

    values = np.sum(values) - np.insert(np.cumsum(values)[:-1], 0, 0)
    values /= dim

    return values


def fisher_info(data):
    """Return Fisher information of a sequence"""

    if data.min() < 0:
        raise ValueError(
            'Fiser info only works on non-negative '
            'data. Current minimum: {}'.format(data.min())
            )

    # padding and renormalizing to avoid zero-values in log
    pad = 1.0e-16 * np.mean(data)
    data_pad = data - data.min() + pad
    data_pad /= np.sum(data_pad)

    data_log = np.log(data_pad)

    data_fi = np.abs(
        np.gradient(np.gradient(data_log))
        )

    return data_fi


def fit_to_data(distro_values, target_data, weights=None):
    """
    Scale and shift the values in `distro_values` to align with a
    set of observed data in the sequence `target_data`

    The values in the BrokenStick object and `target_data` will be
    log-transformed before fitting. This is useful
    when aligning series that are strictly non-negative (e.g., eigenvalues
    from P.S.D. matrices). In the case that they're not non-negative, we'll
    shift them up so that they are

    The array `weights` will determine how much importance is placed on
    matching each particular point in the series.
    """

    min_val = np.min([target_data.min(), distro_values.min()])
    pad = 1.0 / len(target_data)

    targ_trans = np.log(target_data - min_val + pad)
    dist_trans = np.log(distro_values - min_val + pad)

    targ_wmean, targ_wsd = weighted_moments(targ_trans, weights)
    dist_wmean, dist_wsd = weighted_moments(dist_trans, weights)

    scale = targ_wsd / dist_wsd
    shift = targ_wmean - scale*dist_wmean

    dist_trans_fit = scale*dist_trans + shift

    dist_fit = np.exp(dist_trans_fit) + min_val - pad

    return dist_fit


class BrokenStick(object):
    """
    BrokenStick object has a series of values in the attribute `values` that are
    generated to conform to a broken stick distribution. These values can be
    shifted and scaled to align with a target distribution that you suspect is
    distributed in a broken-stick-esque manner.
    """

    def __init__(self, in_vals, **kwargs):

        if isinstance(in_vals, (float, int)):
            self.values = calc_broken_stick(in_vals)
        else:
            self.values = calc_broken_stick(len(in_vals))
            self.rescale_broken_stick(in_vals)


    def rescale_broken_stick(self, target_data):
        """
        Align values in the BrokenStick object with the provided target_data.
        Changes are made in-place
        """

        # Determine how to (un)sort the target values based on abs-mag
        targ_sort_idx = np.argsort(-np.abs(target_data))
        targ_unsort_idx = np.argsort(targ_sort_idx)

        """
        Calculate the weights for alignment using the cumulative inverse
        Fisher information of the target values. This will make sure to
        put the most emphasis on fitting 'flat' sections and ignore the
        early parts of the distribution where the broken stick is likely to
        diverge from the observed values
        """

        targ_pdf = np.abs(target_data[targ_sort_idx])
        targ_pdf /= np.sum(targ_pdf)

        inv_fisher_info = 1.0 / fisher_info(targ_pdf)
        weights = np.cumsum(inv_fisher_info)

        fit_values_sorted = fit_to_data(
            np.abs(self.values[targ_sort_idx]),
            np.abs(target_data[targ_sort_idx]),
            weights
            )

        fit_values = fit_values_sorted[targ_unsort_idx]
        self.values = fit_values


    def find_where_target_exceeds(self, target_data):
        """
        Return the indices where the absolute value of target_data exceed
        the absolute value of the BrokenStick values
        """

        good_idx = []

        for idx in range(0, len(target_data)):
            if target_data[idx] > self.values[idx]:
                good_idx.append(idx)
            else:
                break

        return good_idx
