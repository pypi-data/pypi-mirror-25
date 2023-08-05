import tqdm
import numpy
from scipy.stats import gaussian_kde
from fgivenx.io import CacheError, Cache
from fgivenx.parallel import openmp_apply, mpi_apply, rank

def dkl(arrays):
    """ Compute the Kullback-Liebler divergence from samples from prior and posterior. """
    samples, prior_samples = arrays
    samples = samples[~numpy.isnan(samples)]
    prior_samples = prior_samples[~numpy.isnan(prior_samples)]
    return (
            gaussian_kde(samples).logpdf(samples) 
            - gaussian_kde(prior_samples).logpdf(samples)
            ).mean()


def compute_dkl(x, fsamps, prior_fsamps, **kwargs):

    parallel = kwargs.pop('parallel', '')
    nprocs = kwargs.pop('nprocs', None)
    cache = kwargs.pop('cache', None)

    if cache is not None:
        cache = Cache(cache + '_dkl')
        try:
            return cache.check(x, fsamps, prior_fsamps)  
        except CacheError as e:
            print(e.args[0])

    zip_fsamps = list(zip(fsamps, prior_fsamps))

    if parallel is '':
        dkls = [dkl(arrays) for arrays in tqdm.tqdm(zip_fsamps)]
    elif parallel is 'openmp':
        dkls = openmp_apply(dkl, zip_fsamps, nprocs=nprocs)
    else:
        raise ValueError("keyword parallel=%s not recognised,"
                         "options are 'openmp' or 'mpi'" % parallel)

    dkls = numpy.array(dkls)

    if cache is not None:
        cache.data = x, fsamps, prior_fsamps, dkls

    return dkls

