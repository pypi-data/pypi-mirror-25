import numpy as np
from .. import T

from .exponential import ExponentialFamily

from .gaussian import Gaussian

__all__ = ["MatrixNormal", "MN"]

class MatrixNormal(ExponentialFamily):

    def expected_value(self):
        raise NotImplementedError()

    def sample(self, num_samples=1):
        raise NotImplementedError()

    @classmethod
    def regular_to_natural(cls, regular_parameters):
        M, S, V = regular_parameters
        vec_dim = T.prod(T.shape(M)[-2:])
        vec_M = T.reshape(M, [-1, vec_dim])
        VS_inv = T.matrix_inverse(T.kronecker(V[0], S[0]))[None]
        return Gaussian.pack([
            -0.5 * VS_inv,
            T.einsum('iab,ib->ia', VS_inv, vec_M)
        ])

    @classmethod
    def natural_to_regular(cls, natural_parameters):
        raise NotImplementedError

    def log_likelihood(self, x):
        pass

    def log_z(self):
        eta1, eta2 = Gaussian.unpack(self.get_parameters('natural'))
        eta1_inv = T.matrix_inverse(eta1)
        d = T.to_float(T.shape(eta2)[-1])
        return d * 0.5 * T.log(2 * np.pi) - 0.25 * T.einsum('ia,iab,ib->i', eta2, eta1_inv, eta2) - 0.5 * T.logdet(-2 * eta1)

    def log_h(self, x):
        raise NotImplementedError

    def sufficient_statistics(self, x):
        raise NotImplementedError

    def expected_sufficient_statistics(self):
        eta1, eta2 = Gaussian.unpack(self.get_parameters('natural'))
        eta1_inv = T.matrix_inverse(eta1)
        mu = -0.5 * T.einsum('iab,ib->ia', eta1_inv, eta2)
        return Gaussian.pack([
            -0.5 * eta1_inv + 0.25 * T.einsum('ia,ib->iab', mu, mu),
            mu,
        ])

MN = MatrixNormal
