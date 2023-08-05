""" Utilities for computing the probability mass function. """
import scipy.stats
import scipy.interpolate
import numpy
from fgivenx.parallel import parallel_apply
from fgivenx.io import CacheError, Cache


def PMF(samples, t=None):
    """ Compute the probability mass function.

        The set of samples defines a probability density P(t),
        which is computed using a kernel density estimator.

        From P(t) we define:

                    /
        PMF(p) =    | P(t) dt
                    /
                P(t) < p

        This is the cumulative distribution function expressed as a
        function of the probability

        We aim to compute M(t), which indicates the amount of
        probability contained outside the iso-probability contour
        passing through t.


         ^ P(t)                   ...
         |                     | .   .
         |                     |       .
        p|- - - - - - - - - - .+- - - - . - - - - - - - - - - -
         |                   .#|        #.
         |                  .##|        ##.
         |                  .##|        ##.
         |                 .###|        ###.     M(p)
         |                 .###|        ###.     is the
         |                 .###|        ###.     shaded area
         |                .####|        ####.
         |                .####|        ####.
         |              ..#####|        #####..
         |          ....#######|        #######....
         |         .###########|        ###########.
         +---------------------+-------------------------------> t
                              t

         ^ M(p)                        ^ M(t)
         |                             |
        1|                +++         1|         +
         |               +             |        + +
         |       ++++++++              |       +   +
         |     ++                      |     ++     ++
         |   ++                        |   ++         ++
         |+++                          |+++             +++
         +---------------------> p     +---------------------> t
        0                   1

        Parameters
        ----------
        samples: array-like
            Array of samples from a probability density P(t).

        t: array-like (optional)
            Array to evaluate the PDF at

        Returns
        -------
        if t == None:
            function for the log of the pmf
        else:
            PMF evaluated at each t value

    """
    # Compute the kernel density estimator from the samples
    samples = numpy.array(samples)
    samples = samples[~numpy.isnan(samples)]
    kernel = scipy.stats.gaussian_kde(samples)

    # Sort the samples in t, and find their probabilities
    samples = kernel.resample(10000)[0]
    samples.sort()
    ps = kernel(samples)

    # Compute the cumulative distribution function M(t) by
    # sorting the ps, and finding the position in that sort
    # We then store this as a log
    logms = numpy.log(scipy.stats.rankdata(ps) / float(len(samples)))

    samples
    # create an interpolating function of log(M(t))
    logpmf = scipy.interpolate.interp1d(samples, logms,
                                        bounds_error=False,
                                        fill_value=-numpy.inf)
    if t is not None:
        return numpy.exp(logpmf(numpy.array(t)))
    else:
        return logpmf


def compute_pmf(fsamps, y, **kwargs):
    """ Compute the pmf defined by fsamps at each x for each y.

    Parameters
    ----------
    fsamps: 2D array-like
        array of function samples, as returned by fgivenx.compute_samples

    y: 1D array-like
        y values to evaluate the PMF at

    Keywords
    --------
    parallel:
        see docstring for fgivenx.parallel.parallel_apply.

    Returns
    -------
    """
    parallel = kwargs.pop('parallel', False)
    cache = kwargs.pop('cache', None)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)

    if cache is not None:
        cache = Cache(cache + '_masses')
        try:
            return cache.check(fsamps, y)
        except CacheError as e:
            print(e)

    masses = parallel_apply(PMF, fsamps, postcurry=y, parallel=parallel)
    masses = numpy.array(masses).transpose().copy()

    if cache is not None:
        cache.save(fsamps, y, masses)

    return masses
