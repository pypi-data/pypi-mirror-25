# -*- coding: utf-8 -*-
#
#Created on Fri Apr 21 11:13:09 2017
#
#author: Elina THIBEAU-SUTRE
#
from joblib import Parallel,delayed
from abc import abstractmethod
import numpy as np
import scipy.linalg
from scipy.special import gammaln,iv
import math
import warnings
import h5py
import time

def _full_covariance_matrix(points,mean,weight,resp,reg_covar):
    """
    Compute the correspondong covariance matrix
    """
    _,dim = points.shape

    diff = points - mean
    diff_weighted = diff * resp
    cov = 1/weight * np.dot(diff_weighted.T,diff)
    cov.flat[::dim + 1] += reg_covar
    return cov

def _full_covariance_matrices(points,means,weights,resp,reg_covar,n_jobs=1):
    """
    Compute the full covariance matrices
    """
    nb_points,dim = points.shape
    n_components,_ = means.shape
    
    covariance = Parallel(n_jobs=n_jobs,backend='threading')(
            delayed(_full_covariance_matrix)(points,means[i],weights[i],resp[:,i:i+1],
                   reg_covar) for i in range(n_components))
    
    covariance = np.asarray(covariance)
    
    return covariance

def _spherical_covariance_matrices(points,means,weights,assignements,reg_covar,n_jobs=1):
    """
    Compute the coefficients for the spherical covariances matrices
    """
    n_points,dim = points.shape
    n_components,_ = means.shape
    
    covariance = np.zeros(n_components)

    for i in range(n_components):
        assignements_i = assignements[:,i:i+1]
        
        points_centered = points - means[i]
        points_centered_weighted = points_centered * assignements_i
        product = points_centered * points_centered_weighted
        covariance[i] = np.sum(product)/weights[i]
        covariance[i] += reg_covar
    
    return covariance / dim

def _compute_precisions_chol(cov,covariance_type):
    
     if covariance_type in 'full':
        n_components, n_features, _ = cov.shape
        precisions_chol = np.empty((n_components, n_features, n_features))
        for k, covariance in enumerate(cov):
            try:
                cov_chol = scipy.linalg.cholesky(covariance, lower=True)
            except scipy.linalg.LinAlgError:
                raise ValueError(str(k) + "-th covariance matrix non positive definite")
            precisions_chol[k] = scipy.linalg.solve_triangular(cov_chol,
                                                               np.eye(n_features),
                                                               lower=True,check_finite=False).T
     return precisions_chol

def _log_normal_matrix_core(points,mu,prec_chol):
    y = np.dot(points,prec_chol) - np.dot(mu,prec_chol)
    return np.sum(np.square(y),axis=1)

def _log_normal_matrix(points,means,cov,covariance_type,n_jobs=1):
    """
    This method computes the log of the density of probability of a normal law centered. Each line
    corresponds to a point from points.
    
    :param points: an array of points (n_points,dim)
    :param means: an array of k points which are the means of the clusters (n_components,dim)
    :param cov: an array of k arrays which are the covariance matrices (n_components,dim,dim)
    :return: an array containing the log of density of probability of a normal law centered (n_points,n_components)
    """
    n_points,dim = points.shape
    n_components,_ = means.shape
    
    if covariance_type == "full":
        precisions_chol = _compute_precisions_chol(cov,covariance_type)
        log_det_chol = np.log(np.linalg.det(precisions_chol))
        
        log_prob = Parallel(n_jobs=n_jobs,backend='threading')(
           delayed(_log_normal_matrix_core)(points,means[k],precisions_chol[k]) for k in range(n_components))
        log_prob = np.asarray(log_prob).T
        
    elif covariance_type == "spherical":
        precisions_chol = np.sqrt(np.reciprocal(cov))
        log_det_chol = dim * np.log(precisions_chol)
        
        log_prob = np.empty((n_points,n_components))
        for k, (mu, prec_chol) in enumerate(zip(means,precisions_chol)):
            y = prec_chol * (points - mu)
            log_prob[:,k] = np.sum(np.square(y), axis=1)
            
    return -.5 * (dim * np.log(2*np.pi) + log_prob) + log_det_chol

def _log_vMF_matrix(points,means,K,n_jobs=1):
    """
    This method computes the log of the density of probability of a von Mises Fischer law. Each line
    corresponds to a point from points.
    
    :param points: an array of points (n_points,dim)
    :param means: an array of k points which are the means of the clusters (n_components,dim)
    :param cov: an array of k arrays which are the covariance matrices (n_components,dim,dim)
    :return: an array containing the log of density of probability of a von Mises Fischer law (n_points,n_components)
    """
    n_points,dim = points.shape
    n_components,_ = means.shape
    dim = float(dim)
    
    log_prob = K * np.dot(points,means.T)
    # Regularisation to avoid infinte terms
    bessel_term = iv(dim*0.5-1,K)
    idx = np.where(bessel_term==np.inf)[0]
    bessel_term[idx] = np.finfo(K.dtype).max
               
    log_C = -.5 * dim * np.log(2*np.pi) - np.log(bessel_term) + (dim/2-1) * np.log(K)
            
    return log_C + log_prob


def _log_B(W,nu):
    """
    The log of a coefficient involved in the Wishart distribution
    see Bishop book p.693 (B.78)
    """
    
    dim,_ = W.shape
    
    det_W = np.linalg.det(W)
    log_gamma_sum = np.sum(gammaln(.5 * (nu - np.arange(dim)[:, np.newaxis])), 0)
    result = - nu*0.5*np.log(det_W) - nu*dim*0.5*np.log(2)
    result += -dim*(dim-1)*0.25*np.log(np.pi) - log_gamma_sum
    return result


def _log_C(alpha):
    """
    The log of a coefficient involved in the Dirichlet distribution
    see Bishop book p.687 (B.23)
    """
    
    return gammaln(np.sum(alpha)) - np.sum(gammaln(alpha))


def _check_saving(saving,saving_iter):
    if saving is None or saving == 'final':
        def condition(iteration):
            return False
    elif saving == 'log':
        if saving_iter <= 1 or not isinstance(saving_iter,int):
            raise ValueError('Innapropriate argument value for saving_iter %s'
    								  "it must be an int > 1."
                             %saving_iter)
        def condition(iteration):
            return math.log(iteration,saving_iter)%1 == 0
    elif saving == 'linear':
        if saving_iter < 1 or not isinstance(saving_iter,int):
            raise ValueError('Innapropriate argument value for saving_iter %s'
    								  "it must be an int > 0."
                             %saving_iter)
        def condition(iteration):
            return iteration%saving_iter == 0
    else:
        raise ValueError('Innapropriate argument value for saving %s'
								  "it must be in ['log','linear','final']"
								  %saving)
    return condition


class BaseMixture():
    """
    Base class for mixture models.
    This abstract class specifies an interface for other mixture classes and
    provides basic common methods for mixture models.
    """

    def __init__(self, n_components=1,init="GMM",n_iter_max=1000,
                 tol=1e-3,patience=0,type_init='resp'):
        
        super(BaseMixture, self).__init__()

        self.n_components = n_components
        self.init = init
        self.type_init = type_init
        
        self._is_initialized = False
        
    def _check_common_parameters(self):
        """
        This function tests the parameters common to all algorithms
        
        """
        
        if self.n_components < 1:
            raise ValueError("The number of components cannot be less than 1")
        else:
            self.n_components = int(self.n_components)
            
                        
        if self.type_init not in ['resp','mcw']:
            raise ValueError("Invalid value for 'type_init': %s "
                             "'type_init' should be in "
                             "['resp','mcw']"
                             % self.type_init)
            
    def _check_prior_parameters(self,points):
        """
        This function tests the hyperparameters of the VBGMM and the DBGMM
        
        """
        n_points,dim = points.shape
        
        #Checking alpha_0
        if self.alpha_0 is None:
            self.alpha_0 = 1/self.n_components
        elif self.alpha_0 < 0:
            raise ValueError("alpha_0 must be positive")
        
        #Checking beta_0
        if self.beta_0 is None:
            self.beta_0 = 1.0
        
        #Checking nu_0
        if self.nu_0 is None:
            self.nu_0 = dim
        
        elif self.nu_0 < dim:
            raise ValueError("nu_0 must be more than the dimension of the"
                             "problem or the gamma function won't be defined")
        
        
        #Checking prior mean
        if self._means_prior is None:
            self._means_prior = np.mean(points,axis=0)
        elif len(self._means_prior) != dim:
            raise ValueError("the mean prior must have the same dimension as "
                             "the points : %s."
                             % dim)
        
        # Checking prior W-1
        if self.covariance_type == 'full':
            if self._inv_prec_prior is None:
                self._inv_prec_prior = np.cov(points.T)
            elif self._inv_prec_prior.shape != (dim,dim):
                raise ValueError("the covariance prior must have the same "
                                 "dimension as the points : %s."
                                 % dim)
                
        elif self.covariance_type == 'spherical':
            if self._inv_prec_prior is None:
                self._inv_prec_prior = np.var(points)
            elif not isinstance(self._inv_prec_prior, float):
                raise ValueError("Please enter a float for "
                                 "the spherical covariance prior.")
        
    def _check_points(self,points):
        """
        This method checks that the points have the same dimension than the
        problem
        
        """
        
        
        if len(points.shape) == 1:
            points=points.reshape(1,len(points))
            
        elif len(points.shape) != 2:
            raise ValueError('Only 2D or 1D arrays are admitted')

        _,dim_points = points.shape
        _,dim_means = self.means.shape
        if dim_means != dim_points:
            raise ValueError('The points given must have the same '
                             'dimension as the problem : ' + str(dim_means))
        return points
    
    @abstractmethod   
    def _convergence_criterion(self,points,log_resp,log_prob_norm):
        """
        The convergence criterion is different for GMM and VBGMM/DPGMM :
            - in GMM the log likelihood is used
            - in VBGMM/DPGMM the lower bound of the log likelihood is used
            
        """
        pass
        
    @abstractmethod   
    def _convergence_criterion_simplified(self,points,log_resp,log_prob_norm):
        """
        The convergence criterion is different for GMM and VBGMM/DPGMM :
            - in GMM the log likelihood is used
            - in VBGMM/DPGMM the lower bound of the log likelihood is used
            
        This function was implemented as the convergence criterion is easier
        to compute with training data as the original formula can be simplified
        
        """
        pass
    
    
    def _initialize_cov(self,points):
        from .kmeans import dist_matrix
        n_points,dim = points.shape
        assignements = np.zeros((n_points,self.n_components))
        
        M = dist_matrix(points,self.means)
        for i in range(n_points):
            index_min = np.argmin(M[i]) #the cluster number of the ith point is index_min
            if (isinstance(index_min,np.int64)):
                assignements[i][index_min] = 1
            else: #Happens when two points are equally distant from a cluster mean
                assignements[i][index_min[0]] = 1
                            
        weights = np.sum(assignements,axis=0) + 10 * np.finfo(assignements.dtype).eps

        if self.covariance_type == 'full':
            self.cov = _full_covariance_matrices(points,self.means,weights,assignements,self.reg_covar,self.n_jobs)
        elif self.covariance_type == 'spherical':
            self.cov = _spherical_covariance_matrices(points,self.means,weights,assignements,self.reg_covar,self.n_jobs)
        
    
    def fit(self,points_data,points_test=None,tol=1e-3,patience=None,
            n_iter_max=100,n_iter_fix=None,saving=None,file_name='model',
            saving_iter=2):
        """The EM algorithm
        
        Parameters
        ----------
        points_data : array (n_points,dim)
            A 2D array of points on which the model will be trained
            
        tol : float, defaults to 1e-3
            The EM algorithm will stop when the difference between two steps 
            regarding the convergence criterion is less than tol.
            
        n_iter_max : int, defaults to 100
            number of iterations maximum that can be done
        
        saving_iter : int | defaults 2
            An int to know how often the model is saved (see saving below).
            
        file_name : str | defaults model
            The name of the file (including the path).
            
        Other Parameters
        ----------------
        points_test : array (n_points_bis,dim) | Optional
            A 2D array of points on which the model will be tested.
            
        patience : int | Optional
            The number of iterations performed after having satisfied the
            convergence criterion
        
        n_iter_fix : int | Optional
            If not None, the algorithm will exactly do the number of iterations
            of n_iter_fix and stop.
        
        saving : str | Optional
            A string in ['log','linear']. In the following equations x is the parameter
            saving_iter (see above).
            
            * If 'log', the model will be saved for all iterations which verify :
                log(iter)/log(x) is an int
                
            * If 'linear' the model will be saved for all iterations which verify :
                iter/x is an int
            
        Returns
        -------
        None
        
        """
        
        early_stopping = points_test is not None
            
        resume_iter = True
        first_iter = True
        iter_patience = 0
        iter_algo = 0
        best_criterion = -np.Inf
        
        condition = _check_saving(saving,saving_iter)
        
        if patience is None:
            if early_stopping:
                warnings.warn('You are using early stopping with no patience. '
                              'Set the patience parameter to 0 to not see this '
                              'message again')
            patience = 0

        #Initialization
        if not self._is_initialized or self.init!='user':
            self._initialize(points_data,points_test)
            self.iter = 0
            
        self.convergence_criterion_data = []
        self.convergence_criterion_test = []
                
        #Saving the initialization
        if saving is not None:
            file = h5py.File(file_name + ".h5", "w")
            grp = file.create_group('init')
            self.write(grp)
            file.close()
        
        while resume_iter:
            #EM algorithm
            log_prob_norm_data,log_resp_data = self._step_E(points_data)
            if early_stopping:
                log_prob_norm_test,log_resp_test = self._step_E(points_test)
                
            self._step_M(points_data,log_resp_data)
            
            #Computation of the convergence criterion(s)
            self.convergence_criterion_data.append(self._convergence_criterion_simplified(points_data,log_resp_data,log_prob_norm_data))
            if early_stopping:
                self.convergence_criterion_test.append(self._convergence_criterion(points_test,log_resp_test,log_prob_norm_test))
            
            if early_stopping:
                criterion = self.convergence_criterion_test
                norm = len(points_test)
            else:
                criterion = self.convergence_criterion_data
                norm = len(points_data)
                
            self.iter+=1
                
            #Computation of resume_iter
            if n_iter_fix is not None:
                resume_iter = self.iter < n_iter_fix
                
            elif first_iter:
                resume_iter = True
                first_iter = False
            
            elif self.iter > n_iter_max:
                resume_iter = False
            
            else:
                diff = criterion[iter_algo] - criterion[iter_algo-1]
                diff /= norm
                if diff < tol:
                    resume_iter = iter_patience < patience
                    iter_patience += 1
            
            # Keep the best parameters
            if criterion[iter_algo] > best_criterion:
                best_params = self._get_parameters()
                best_criterion = criterion[iter_algo]
                
            #Saving the model
            if saving is not None and not resume_iter:
                self._set_parameters(best_params)
                file = h5py.File(file_name + ".h5", "a")
                grp = file.create_group('best')
                self.write(grp)
                file.close()
                
            elif condition(self.iter):
                f = h5py.File(file_name + '.h5', 'a')
                grp = f.create_group('iter' + str(self.iter))
                self.write(grp)
                f.close()
        
            iter_algo += 1
        
        print("Number of iterations :", self.iter)
    
    def predict_log_resp(self,points):
        """
        This function returns the logarithm of each point's responsibilities
        
        Parameters
        ----------
        points : array (n_points_bis,dim)
            a 1D or 2D array of points with the same dimension as the problem
            
        Returns
        -------
        log_resp : array (n_points_bis,n_components)
            the logarithm of the responsibilities
            
        """
        
        points = self._check_points(points)
        
        if self._is_initialized:
            _,log_resp = self._step_E(points)
            return log_resp
    
        else:
            raise Exception("The model is not initialized")
    
    def score(self,points):
        """
        This function return the score of the function, which is the logarithm of
        the likelihood for GMM and the logarithm of the lower bound of the likelihood
        for VBGMM and DPGMM
        
        Parameters
        ----------
        points : array (n_points_bis,dim)
            a 1D or 2D array of points with the same dimension as the problem
            
        Returns
        -------
        score : float
            
        """
        points = self._check_points(points)
            
        if self._is_initialized:
            log_prob,log_resp = self._step_E(points)
            score = self._convergence_criterion(points,log_resp,log_prob)
            return score
        
        else:
            raise Exception("The model is not fitted")
    
    def write(self,group):
        """
        A method creating datasets in a group of an hdf5 file in order to save
        the model
        
        Parameters
        ----------
        group : HDF5 group
            A group of a hdf5 file in reading mode

        """
        group.create_dataset('means',self.means.shape,dtype='float64')
        group['means'][...] = self.means
        group.create_dataset('log_weights',self.log_weights.shape,dtype='float64')
        group['log_weights'][...] = self.log_weights
        group.attrs['iter'] = self.iter
        group.attrs['time'] = time.time()
        
        if self.name in ['GMM','VBGMM','DPGMM']:
            group.create_dataset('cov',self.cov.shape,dtype='float64')
            group['cov'][...] = self.cov
        
        if self.name in ['VBGMM','DPGMM']:
            initial_parameters = np.asarray([self.alpha_0,self.beta_0,self.nu_0])
            group.create_dataset('initial parameters',initial_parameters.shape,dtype='float64')
            group['initial parameters'][...] = initial_parameters
            group.create_dataset('means prior',self._means_prior.shape,dtype='float64')
            group['means prior'][...] = self._means_prior
            group.create_dataset('inv prec prior',self._inv_prec_prior.shape,dtype='float64')
            group['inv prec prior'][...] = self._inv_prec_prior

    
    def read_and_init(self,group,points):
        """
        A method reading a group of an hdf5 file to initialize DPGMM
        
        Parameters
        ----------
        group : HDF5 group
            A group of a hdf5 file in reading mode
            
        """
        self.means = np.asarray(group['means'].value)
        self.log_weights = np.asarray(group['log_weights'].value)
        self.iter = group.attrs['iter']

        n_components = len(self.means)
        if n_components != self.n_components:
            warnings.warn('You are now currently working with %s components.'
                          % n_components)
            self.n_components = n_components
        
        self.type_init ='user'
        self.init = 'user'
        
        
        if self.name in ['GMM','VBGMM','DPGMM']:
            try:
                self.cov = np.asarray(group['cov'].value)
            except KeyError:
                warnings.warn('You are reading a model with no prior '
                              'parameters. They will be initialized '
                              'if not already given during __init__')
                self.type_init = 'kmeans'
        
        if self.name in ['VBGMM','DPGMM']:
            try:
                initial_parameters = group['initial parameters'].value
                self.alpha_0 = initial_parameters[0]
                self.beta_0 = initial_parameters[1]
                self.nu_0 = initial_parameters[2]
                self._means_prior = np.asarray(group['means prior'].value)
                self._inv_prec_prior = np.asarray(group['inv prec prior'].value)
            except KeyError:
                warnings.warn('You are reading a model with no prior '
                              'parameters. They will be initialized '
                              'if not already given during __init__')
            
        self._initialize(points)
        
        
    def simplified_model(self,points):
        """
        A method creating a new model with simplified parameters: clusters unused
        are removed
        
        Parameters
        ----------
        points : an array (n_points,dim)
        
        Returns
        -------
        GM : an instance of the same type of self: GMM,VBGMM or DPGMM

        """
        import copy
        
        GM = copy.copy(self)
        params = self._limiting_model(points)
        GM._set_parameters(params)
        return GM