# -*- coding: utf-8 -*-
"""
Domain adaptation with optimal transport with GPU implementation
"""

# Author: Remi Flamary <remi.flamary@unice.fr>
#         Nicolas Courty <ncourty@irisa.fr>
#         Michael Perrot <michael.perrot@univ-st-etienne.fr>
#         Leo Gautheron <https://github.com/aje>
#
# License: MIT License


import numpy as np
from ..utils import unif
from ..da import OTDA
from .bregman import sinkhorn
import cudamat


def pairwiseEuclideanGPU(a, b, returnAsGPU=False, squared=False):
    """
    Compute the pairwise euclidean distance between matrices a and b.


    Parameters
    ----------
    a : np.ndarray (n, f)
        first matrice
    b : np.ndarray (m, f)
        second matrice
    returnAsGPU : boolean, optional (default False)
        if True, returns cudamat matrix still on GPU, else return np.ndarray
    squared : boolean, optional (default False)
        if True, return squared euclidean distance matrice


    Returns
    -------
    c : (n x m) np.ndarray or cudamat.CUDAMatrix
        pairwise euclidean distance distance matrix
    """
    # a is shape (n, f) and b shape (m, f). Return matrix c of shape (n, m).
    # First compute in c_GPU the squared euclidean distance. And return its
    # square root. At each cell [i,j] of c, we want to have
    # sum{k in range(f)} ( (a[i,k] - b[j,k])^2 ). We know that
    # (a-b)^2 = a^2 -2ab +b^2. Thus we want to have in each cell of c:
    # sum{k in range(f)} ( a[i,k]^2 -2a[i,k]b[j,k] +b[j,k]^2).

    a_GPU = cudamat.CUDAMatrix(a)
    b_GPU = cudamat.CUDAMatrix(b)

    # Multiply a by b transpose to obtain in each cell [i,j] of c the
    # value sum{k in range(f)} ( a[i,k]b[j,k] )
    c_GPU = cudamat.dot(a_GPU, b_GPU.transpose())
    # multiply by -2 to have sum{k in range(f)} ( -2a[i,k]b[j,k] )
    c_GPU.mult(-2)

    # Compute the vectors of the sum of squared elements.
    a_GPU = cudamat.pow(a_GPU, 2).sum(axis=1)
    b_GPU = cudamat.pow(b_GPU, 2).sum(axis=1)

    # Add the vectors in each columns (respectivly rows) of c.
    # sum{k in range(f)} ( a[i,k]^2 -2a[i,k]b[j,k] )
    c_GPU.add_col_vec(a_GPU)
    # sum{k in range(f)} ( a[i,k]^2 -2a[i,k]b[j,k] +b[j,k]^2)
    c_GPU.add_row_vec(b_GPU.transpose())

    if not squared:
        c_GPU = cudamat.sqrt(c_GPU)

    if returnAsGPU:
        return c_GPU
    else:
        return c_GPU.asarray()


def sinkhorn_lpl1_mm(a, labels_a, b, M_GPU, reg, eta=0.1, numItermax=10,
                     numInnerItermax=200, stopInnerThr=1e-9,
                     verbose=False, log=False):
    """
    Solve the entropic regularization optimal transport problem with nonconvex group lasso regularization

    The function solves the following optimization problem:

    .. math::
        \gamma = arg\min_\gamma <\gamma,M>_F + reg\cdot\Omega_e(\gamma)+ \eta \Omega_g(\gamma)

        s.t. \gamma 1 = a

             \gamma^T 1= b

             \gamma\geq 0
    where :

    - M is the (ns,nt) metric cost matrix
    - :math:`\Omega_e` is the entropic regularization term :math:`\Omega_e(\gamma)=\sum_{i,j} \gamma_{i,j}\log(\gamma_{i,j})`
    - :math:`\Omega_g` is the group lasso  regulaization term :math:`\Omega_g(\gamma)=\sum_{i,c} \|\gamma_{i,\mathcal{I}_c}\|^{1/2}_1`   where  :math:`\mathcal{I}_c` are the index of samples from class c in the source domain.
    - a and b are source and target weights (sum to 1)

    The algorithm used for solving the problem is the generalised conditional gradient as proposed in  [5]_ [7]_


    Parameters
    ----------
    a : np.ndarray (ns,)
        samples weights in the source domain
    labels_a : np.ndarray (ns,)
        labels of samples in the source domain
    b : np.ndarray (nt,)
        samples weights in the target domain
    M_GPU : cudamat.CUDAMatrix (ns,nt)
        loss matrix
    reg : float
        Regularization term for entropic regularization >0
    eta : float, optional
        Regularization term  for group lasso regularization >0
    numItermax : int, optional
        Max number of iterations
    numInnerItermax : int, optional
        Max number of iterations (inner sinkhorn solver)
    stopInnerThr : float, optional
        Stop threshold on error (inner sinkhorn solver) (>0)
    verbose : bool, optional
        Print information along iterations
    log : bool, optional
        record log if True


    Returns
    -------
    gamma : (ns x nt) ndarray
        Optimal transportation matrix for the given parameters
    log : dict
        log dictionary return only if log==True in parameters


    References
    ----------

    .. [5] N. Courty; R. Flamary; D. Tuia; A. Rakotomamonjy, "Optimal Transport for Domain Adaptation," in IEEE Transactions on Pattern Analysis and Machine Intelligence , vol.PP, no.99, pp.1-1
    .. [7] Rakotomamonjy, A., Flamary, R., & Courty, N. (2015). Generalized conditional gradient: analysis of convergence and applications. arXiv preprint arXiv:1510.06567.

    See Also
    --------
    ot.lp.emd : Unregularized OT
    ot.bregman.sinkhorn : Entropic regularized OT
    ot.optim.cg : General regularized OT

    """
    p = 0.5
    epsilon = 1e-3
    Nfin = len(b)

    indices_labels = []
    classes = np.unique(labels_a)
    for c in classes:
        idxc, = np.where(labels_a == c)
        indices_labels.append(cudamat.CUDAMatrix(idxc.reshape(1, -1)))

    Mreg_GPU = cudamat.empty(M_GPU.shape)
    W_GPU = cudamat.empty(M_GPU.shape).assign(0)

    for cpt in range(numItermax):
        Mreg_GPU.assign(M_GPU)
        Mreg_GPU.add_mult(W_GPU, eta)
        transp_GPU = sinkhorn(a, b, Mreg_GPU, reg, numItermax=numInnerItermax,
                              stopThr=stopInnerThr, returnAsGPU=True)
        # the transport has been computed. Check if classes are really
        # separated
        W_GPU.assign(1)
        W_GPU = W_GPU.transpose()
        for (i, c) in enumerate(classes):
            (_, nbRow) = indices_labels[i].shape
            tmpC_GPU = cudamat.empty((Nfin, nbRow)).assign(0)
            transp_GPU.transpose().select_columns(indices_labels[i], tmpC_GPU)
            majs_GPU = tmpC_GPU.sum(axis=1).add(epsilon)
            cudamat.pow(majs_GPU, (p - 1))
            majs_GPU.mult(p)

            tmpC_GPU.assign(0)
            tmpC_GPU.add_col_vec(majs_GPU)
            W_GPU.set_selected_columns(indices_labels[i], tmpC_GPU)

        W_GPU = W_GPU.transpose()

    return transp_GPU.asarray()


class OTDA_GPU(OTDA):
    def normalizeM(self, norm):
        if norm == "median":
            self.M_GPU.divide(float(np.median(self.M_GPU.asarray())))
        elif norm == "max":
            self.M_GPU.divide(float(np.max(self.M_GPU.asarray())))
        elif norm == "log":
            self.M_GPU.add(1)
            cudamat.log(self.M_GPU)
        elif norm == "loglog":
            self.M_GPU.add(1)
            cudamat.log(self.M_GPU)
            self.M_GPU.add(1)
            cudamat.log(self.M_GPU)


class OTDA_sinkhorn(OTDA_GPU):
    def fit(self, xs, xt, reg=1, ws=None, wt=None, norm=None, **kwargs):
        cudamat.init()
        xs = np.asarray(xs, dtype=np.float64)
        xt = np.asarray(xt, dtype=np.float64)

        self.xs = xs
        self.xt = xt

        if wt is None:
            wt = unif(xt.shape[0])
        if ws is None:
            ws = unif(xs.shape[0])

        self.ws = ws
        self.wt = wt

        self.M_GPU = pairwiseEuclideanGPU(xs, xt, returnAsGPU=True,
                                          squared=True)
        self.normalizeM(norm)
        self.G = sinkhorn(ws, wt, self.M_GPU, reg, **kwargs)
        self.computed = True


class OTDA_lpl1(OTDA_GPU):
    def fit(self, xs, ys, xt, reg=1, eta=1, ws=None, wt=None, norm=None,
            **kwargs):
        cudamat.init()
        xs = np.asarray(xs, dtype=np.float64)
        xt = np.asarray(xt, dtype=np.float64)

        self.xs = xs
        self.xt = xt

        if wt is None:
            wt = unif(xt.shape[0])
        if ws is None:
            ws = unif(xs.shape[0])

        self.ws = ws
        self.wt = wt

        self.M_GPU = pairwiseEuclideanGPU(xs, xt, returnAsGPU=True,
                                          squared=True)
        self.normalizeM(norm)
        self.G = sinkhorn_lpl1_mm(ws, ys, wt, self.M_GPU, reg, eta, **kwargs)
        self.computed = True
