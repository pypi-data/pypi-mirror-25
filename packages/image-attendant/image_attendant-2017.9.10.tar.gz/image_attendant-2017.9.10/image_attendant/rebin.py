
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from . import utility


def _resize(data, factor, axis=0, verbose=False):
    """
    Do the work of resizing image data along horizontal or vertical axis.

    factor:
        positive value larger than one implies grow by integer amount
        positive value between zero and one implies shrink by integer amount (1/factor)
        negative value less than negative one implies shrink by integer amount abs(factor)

    data: 3D array
    """
    if axis not in [0, 1]:
        raise ValueError('Invalid axis: {}'.format(axis))

    num_lines, num_samples, num_bands = data.shape

    if factor < -1:
        factor = 1 / round(abs(factor))
    elif 0 < factor and factor < 1:
        factor = 1 / round(1/factor)
    elif 1 == factor:
        pass
    elif 1 < factor:
        factor = round(factor)
    else:
        raise ValueError('Invalid scale factor: {}'.format(factor))

    # Do nothing for unit scale factor.
    if factor == 1:
        return data

    # New sizes for new data.
    if axis == 0:
        num_lines_new = int(num_lines * factor)
        num_samples_new = num_samples
    else:
        num_lines_new = num_lines
        num_samples_new = int(num_samples * factor)

    if verbose:
        print(axis, factor)
        print(num_lines, num_samples)
        print(num_lines_new, num_samples_new)

    # Build new data.
    data_new = np.zeros((num_lines_new, num_samples_new, num_bands), dtype=np.float)

    if factor < 1:
        # Co-add along specified image axis.

        coadd = int(1/factor)
        for p in range(0, coadd):
            if axis == 0:
                data_p = data[p:num_lines_new*coadd:coadd, :, :]
            else:
                data_p = data[:, p:num_samples_new*coadd:coadd, :]

            data_new += data_p

        data_new /= coadd

    else:
        # Grow by nearest-neighbor sampling.
        for p in range(0, factor):
            if axis == 0:
                data_new[p::factor, :, :] = data
            else:
                data_new[:, p::factor, :] = data

    return data_new


def rebin(data, factor, verbose=False):
    """
    Resize image by integer amount.
    Pixel-averaging for shrinking, nearest-neighbor for growing.

    size_factor: integer or 2-tuple of X and Y integer scale factors.
    """

    if not hasattr(factor, '__iter__'):
        factor = [factor, factor]

    factor_lines, factor_samples = factor

    if factor_lines == 1 and factor_samples == 1:
        return data

    dtype_orig = data.dtype

    # Prepare the data.
    data = np.asarray(data)

    ndim_orig = data.ndim

    num_lines, num_samples = data.shape[0:2]
    data = data.reshape(num_lines, num_samples, -1)

    # Do the work.
    data_tmp = _resize(data, factor_lines, axis=0, verbose=verbose)
    data_new = _resize(data_tmp, factor_samples, axis=1, verbose=verbose)

    if ndim_orig == 2:
        data_new = data_new.squeeze()

    # Finish.
    if utility._is_integer_type(dtype_orig):
        data_new = np.round(data_new)

    data_new = data_new.astype(dtype_orig)

    # Done.
    return data_new


if __name__ == '__main__':
    pass
