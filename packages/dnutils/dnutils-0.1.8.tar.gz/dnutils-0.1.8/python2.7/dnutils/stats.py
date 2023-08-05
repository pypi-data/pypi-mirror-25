'''
Created on Jan 5, 2017

@author: nyga
'''
try:
    import numpy as np
    from tabulate import tabulate
    from dnutils import ifnone
except ImportError:
    pass
else:
    class Gaussian(object):
        '''
        A Gaussian distribution that can be incrementally updated with new samples
        '''

        def __init__(self, mean=None, cov=None, data=None):
            '''
            Creates a new Gaussian distribution.
            :param mean:    the mean of the Gaussian. May be a scalar (univariante) or an array (multivariate).
            :param cov:     the covariance of the Gaussian. May be a scalar (univariate) or a matrix (multivariate).
            :param data:    if ``mean`` and ``cov`` are not provided, ``data`` may be a data set (matrix) from which
                            the parameters of the distribution are estimated.
            '''
            self.mean = mean
            self.cov = cov
            self.samples = []
            if data is not None:
                self.estimate(data)

        @property
        def mean(self):
            if self._mean is not None and len(self._mean) == 1:
                return self._mean[0]
            else:
                return self._mean

        @mean.setter
        def mean(self, mu):
            if mu is not None and hasattr(mu, '__len__'):
                self._mean = np.array([mu])
            else:
                self._mean = ifnone(mu, None, np.array)

        @property
        def cov(self):
            if self._cov is not None and len(self._cov) == 1:
                return self._cov[0, 0]
            else:
                return self._cov

        @cov.setter
        def cov(self, cov):
            if cov is not None and hasattr(cov, '__len__'):
                self._cov = np.array([[cov]])
            else:
                self._cov = ifnone(cov, None, np.array)

        @property
        def dim(self):
            if self._mean is None:
                raise ValueError('no dimensionality specified yet.')
            return len(self._mean)

        def update(self, x):
            '''update the Gaussian distribution with a new data point `x`.'''
            if not hasattr(x, '__len__'):
                x = [x]
            if self._mean is None or self._cov is None:
                self._mean = np.zeros(len(x))
                self._cov = np.zeros(shape=(len(x), len(x)))
            else:
                assert len(x) == len(self._mean) and self._cov.shape == (len(x), len(x))
            n = len(self.samples)
            oldmean = np.array(self._mean)
            oldcov = np.array(self._cov)
            for i, (m, d) in enumerate(zip(self._mean, x)):
                self._mean[i] = ((n * m) + d) / (n + 1)
            self.samples.append(x)
            if n > 0:
                for j in range(self.dim):
                    for k in range(self.dim):
                        self._cov[j, k] = (oldcov[j, k] * (n - 1) + n * oldmean[j] * oldmean[k] + x[j] * x[k] - (n + 1) * self._mean[j] * self._mean[k]) / float(n)

        def update_all(self, data):
            '''Update the distribution with new data points given in `data`.'''
            for x in data:
                self.update(x)
            return self

        def estimate(self, data):
            '''Estimate the distribution parameters with subject to the given data points.'''
            self.mean = self.cov = None
            return self.update_all(data)

        def sample(self, n=1):
            '''Return `n` samples from the distribution subject to the parameters.'''
            if self.mean is None or self.cov is None:
                raise ValueError('no parameters. You have to set mean and covariance before you draw samples.')
            return np.random.multivariate_normal(self.mean, self.cov, size=n)

        @property
        def var(self):
            if self._cov is None: return None
            return np.array([self._cov[i, i] for i in range(self.dim)])

        def reset(self):
            self.samples = []
            self.mean = None
            self.cov = None

        def __repr__(self):
            try:
                dim = '%s-dim' % str(self.dim)
                if self.dim == 1:
                    dim = 'mu=%.2f, var=%.2f' % (self.mean, self.cov)
            except ValueError:
                dim = '(undefined)'
            return '<Gaussian %s at 0x%s>' % (dim, hex(id(self)))

        def __str__(self):
            try:
                if self.dim > 1:
                    args = '\nmean=\n%s\ncov=\n%s' % (self.mean, tabulate(self.cov))
                else:
                    args = 'mean=%.2f, var=%.2f' % (self.mean, self.cov)
            except ValueError:
                args = 'undefined'
            return '<Gaussian %s>' % args
