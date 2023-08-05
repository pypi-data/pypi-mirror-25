import pandas as pd
import os
def get_time_from_filename_with_mcode( filepath, return_string = True, split_on_underscore = False):
    # convert m name
    filename = os.path.split(filepath)[1]
    if filename.endswith('.ndf'):
        tstamp = float(filename.split('.')[0][-10:])
    elif filename.endswith('.h5'):
        tstamp = float(filename.split('_')[0][-10:])
    elif split_on_underscore:
        tstamp = float(filename.split('_')[0][-10:])
    else:
        print('fileformat for splitting unknown')
        return 0

    if return_string:
        ndf_time = str(pd.Timestamp.fromtimestamp(tstamp)).replace(':', '-')
        ndf_time =  ndf_time.replace(' ', '-')
        return ndf_time
    else:
        ndf_time = pd.Timestamp.fromtimestamp(tstamp)
        return ndf_time

def add_seconds_to_pandas_timestamp(seconds, timestamp):

    new_stamp = timestamp + pd.Timedelta(seconds=float(seconds))
    return new_stamp

def get_time_from_seconds_and_filepath(filepath, seconds,split_on_underscore = False):
    '''
    Args:
        filepath:
        seconds:
        split_on_underscore:

    Returns:
        a pandas timestamp

    '''
    f_stamp = get_time_from_filename_with_mcode(filepath, return_string=False, split_on_underscore=split_on_underscore)
    time_stamp_combined = add_seconds_to_pandas_timestamp(seconds, f_stamp)
    return time_stamp_combined

def filterArray(array,window_size = 51,order=3):
    '''
    Simple for-loop based indexing for savitzky_golay filter

    Inputs:
    array:
    	array.shape[1] are datapoints - each row a trace, columns the datapoints
    	array should be <= 3d
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.


    '''

    import copy
    fData = copy.copy(array)
    ndimensions = len(fData.shape) # number of dimension
    if ndimensions == 1:
        fData = savitzky_golay(array,window_size,order)
    elif ndimensions == 2:
         for trace_i in range(array.shape[0]):
                    fData[trace_i,:] = savitzky_golay(array[trace_i,:],window_size,order)
    elif ndimensions == 3:
        for index in range(array.shape[2]):
                for index2 in range(array.shape[1]):
                    fData[:,index2,index] = savitzky_golay(array[:,index2,index],window_size,order)
    #else:
        #print "Jonny only bothered too (badly) code up to 3 array dimensions!"

    return fData

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688

       http://wiki.scipy.org/Cookbook/SavitzkyGolay
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')