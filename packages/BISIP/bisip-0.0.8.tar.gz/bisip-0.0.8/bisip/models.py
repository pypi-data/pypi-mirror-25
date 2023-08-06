# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:05:22 2015

@author:    charleslberube@gmail.com
            École Polytechnique de Montréal

The MIT License (MIT)

Copyright (c) 2016 Charles L. Bérubé

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://opensource.org/licenses/MIT
https://github.com/clberube/bisip

This python module may be used to import SIP data, run MCMC inversion and
return the results.

It is imported as:

Call with minimal arguments:

sol = mcmcinv('ColeCole', '/Documents/DataFiles/DATA.dat')

Call with all optional arguments:

sol = mcmcinv( model='ColeCole', filename='/Documents/DataFiles/DATA.dat',
                 mcmc=mcmc_params, headers=1, ph_units='mrad', cc_modes=2,
                 debye_poly=4, c_exp = 1.0, keep_traces=False)
"""
from __future__ import division
from __future__ import print_function

#==============================================================================
# Import PyMC, Numpy, and Cython extension
from builtins import range
from past.utils import old_div
import pymc
import numpy as np
from bisip.cython_funcs import ColeCole_cyth1, Dias_cyth, Decomp_cyth, Shin_cyth
# Imports to save things
from os import path, makedirs
from os import getcwd
from datetime import datetime
import bisip.invResults as iR
from bisip.utils import format_results, get_data

#==============================================================================
# Function to run MCMC simulation on selected model
# Arguments: model <function>, mcmc parameters <dict>,traces path <string>
def run_MCMC(function, mc_p, save_traces=False, save_where=None):
    print("\nMCMC parameters:\n", mc_p)
    if save_traces:
        # If path doesn't exist, create it
        if not path.exists(save_where): makedirs(save_where)
        MDL = pymc.MCMC(function, db='txt',
                        dbname=save_where)
    else:
        MDL = pymc.MCMC(function, db='ram',
                        dbname=save_where)

    if mc_p["adaptive"]:
        if mc_p['verbose']:
            mc_p['verbose'] = 1
        MDL.use_step_method(pymc.AdaptiveMetropolis, MDL.stochastics, delay=mc_p["cov_delay"], interval=mc_p['cov_inter'], shrink_if_necessary=True, verbose=mc_p['verbose'])

    else:
        for stoc in MDL.stochastics:
            MDL.use_step_method(pymc.Metropolis, stoc,
                                proposal_distribution='Normal',
                                scale=mc_p['prop_scale'], verbose=mc_p['verbose'])

    for i in range(1, mc_p['nb_chain']+1):
        print('\n Chain #%d/%d'%(i, mc_p['nb_chain']))
        MDL.sample(mc_p['nb_iter'], mc_p['nb_burn'], mc_p['thin'], tune_interval=mc_p['tune_inter'], tune_throughout=False)
    return MDL

class mcmcinv(object):
    # Default MCMC parameters:
    default_mcmc = {"adaptive"  : False,
                   "nb_chain"   : 1,
                   "nb_iter"    : 10000,
                   "nb_burn"    : 8000,
                   "thin"       : 1,
                   "tune_inter" : 500,
                   "prop_scale" : 1.0,
                   "verbose"    : False,
                   "cov_inter"  : 10000,
                   "cov_delay"  : 10000,
                    }
    
    print_results = iR.print_resul
    plot_fit = iR.plot_fit
    plot_histograms = iR.plot_histo
    plot_traces = iR.plot_traces
    save_results = iR.save_resul
    merge_results = iR.merge_results
    plot_log_likelihood = iR.plot_logp
    plot_model_deviance = iR.plot_deviance
    plot_data = iR.plot_data
    plot_rtd = iR.plot_rtd
    plot_autocorrelation = iR.plot_autocorr
    plot_summary = iR.plot_summary
    plot_hexbin = iR.plot_hexbin
    plot_KDE = iR.plot_KDE
    get_model_type = iR.get_model_type
    
    def __init__(self, model, filename, mcmc=default_mcmc, headers=1,
                   ph_units="mrad", cc_modes=2, decomp_poly=4, c_exp=1.0, log_min_tau=-3, guess_noise=False, keep_traces=False):
        self.model = model
        self.filename = filename 
        self.mcmc = mcmc
        self.headers = headers
        self.ph_units = ph_units
        self.cc_modes = cc_modes
        self.decomp_poly = decomp_poly
        self.c_exp = c_exp
        self.log_min_tau = log_min_tau
        self.guess_noise = guess_noise
        self.keep_traces = keep_traces
        self.start()
    
#    def print_resul(self):
#    #==============================================================================
#        # Impression des résultats
#        pm, model, filename = self.pm, self.model, self.filename
#        print('\n\nInversion success!')
#        print('Name of file:', filename)
#        print('Model used:', model)
#        e_keys = sorted([s for s in list(pm.keys()) if "_std" in s])
#        v_keys = [e.replace("_std", "") for e in e_keys]
#        labels = ["{:<8}".format(x+":") for x in v_keys]
#        np.set_printoptions(formatter={'float': lambda x: format(x, '6.3E')})
#        for l, v, e in zip(labels, v_keys, e_keys):
#            print(l, pm[v], '+/-', pm[e], np.char.mod('(%.2f%%)',abs(100*pm[e]/pm[v])))
    
    #==============================================================================
    # Main inversion function.
    def start(self):
    #==============================================================================
        """Cole-Cole Bayesian Model"""
    #==============================================================================
        def ColeColeModel(cc_modes):
            # Initial guesses
            p0 = {'R0'       : 1.0,
                  'm'        : None,
                  'log_tau'  : None,
                  'c'        : None,
                  }
            # Stochastics
            R0 = pymc.Uniform('R0', lower=0.7, upper=1.3 , value=p0["R0"])
            m = pymc.Uniform('m', lower=0.0, upper=1.0, value=p0["m"], size=cc_modes)
            log_tau = pymc.Uniform('log_tau', lower=-7.0, upper=4.0, value=p0['log_tau'], size=cc_modes)
            c = pymc.Uniform('c', lower=0.0, upper=1.0, value=p0['c'], size=cc_modes)
            # Deterministics
            @pymc.deterministic(plot=False)
            def zmod(cc_modes=cc_modes, R0=R0, m=m, lt=log_tau, c=c):
                return ColeCole_cyth1(w, R0, m, lt, c)
            # Likelihood
            obs = pymc.Normal('obs', mu=zmod, tau=old_div(1.0,(self.data["zn_err"]**2)), value=self.data["zn"], size=(2,len(w)), observed=True)
            return locals()
    
    #==============================================================================
        """Shin Bayesian Model"""
    #==============================================================================
        def ShinModel():
            # Initial guesses
            p0 = {'R'      : [0.5, 0.5],
                  'log_Q'  : [0,-4],
                  'n'      : [0.5, 0.5],
                  'log_tau': None,
                  'm'      : None,
                  }
            # Stochastics
            R = pymc.Uniform('R', lower=0.0, upper=1.0, value=p0["R"], size=2)
            log_Q = pymc.Uniform('log_Q', lower=-7, upper=2, value=p0["log_Q"], size=2)
            n = pymc.Uniform('n', lower=0.0, upper=1.0, value=p0["n"], size=2)
            # Deterministics
            @pymc.deterministic(plot=False)
            def zmod(R=R, log_Q=log_Q, n=n):
                return Shin_cyth(w, R, log_Q, n)
            @pymc.deterministic(plot=False)
            def log_tau(R=R, log_Q=log_Q, n=n):
                return np.log10((R*(10**log_Q))**(old_div(1.,n)))
            @pymc.deterministic(plot=False)
            def R0(R=R):
                return R[0]+R[1]
            @pymc.deterministic(plot=False)
            def m(R=R):
                return seigle_m*( old_div(max(R), (max(R) + min(R))))
            #Likelihood
            obs = pymc.Normal('obs', mu=zmod, tau=old_div(1.0,(self.data["zn_err"]**2)), value=self.data["zn"], size = (2,len(w)), observed=True)
            return locals()
    
    #==============================================================================
        """Dias Bayesian Model"""
    #==============================================================================
        def DiasModel():
            # Initial guesses
            p0 = {'R0'     :  1.0,
                  'm'      :  seigle_m,
                  'log_tau':  None,
                  'eta'    :  None,
                  'delta'  :  None,
                  }
            # Stochastics
            R0 = pymc.Uniform('R0', lower=0.9, upper=1.1 , value=1)
            m = pymc.Uniform('m', lower=0.0, upper=1.0, value=p0['m'])
            log_tau = pymc.Uniform('log_tau', lower=-7.0, upper=0.0, value=p0['log_tau'])
            eta = pymc.Uniform('eta', lower=0.0, upper=50.0, value=p0['eta'])
            delta = pymc.Uniform('delta', lower=0.0, upper=1.0, value=p0['delta'])
            # Deterministics
            @pymc.deterministic(plot=False)
            def zmod(R0=R0, m=m, lt=log_tau, eta=eta, delta=delta):
                return Dias_cyth(w, R0, m, lt, eta, delta)
            # Likelihood
            obs = pymc.Normal('obs', mu=zmod, tau=old_div(1.0,(self.data["zn_err"]**2)), value=self.data["zn"], size = (2,len(w)), observed=True)
            return locals()
    
    #==============================================================================
        """Debye, Warburg, Cole-Cole decomposition Bayesian Model"""
    #==============================================================================
        def PolyDecompModel(decomp_poly, c_exp):
            # Initial guesses
            p0 = {'R0'         : 1.0,
                  'a'          : None,
    #              'a'          : ([0.01, -0.01, -0.01, 0.001, 0.001]+[0.0]*(decomp_poly-4))[:(decomp_poly+1)],
                  'log_tau_hi' : -5.0,
                  'm_hi'       : 0.5,
                  'TotalM'     : None,
                  'log_MeanTau': None,
                  'U'          : None,
                  }
            # Stochastics
            R0 = pymc.Uniform('R0', lower=0.7, upper=1.3, value=p0['R0'])
    #        m_hi = pymc.Uniform('m_hi', lower=0.0, upper=1.0, value=p0['m_hi'])
    #        log_tau_hi = pymc.Uniform('log_tau_hi', lower=-8.0, upper=-3.0, value=p0['log_tau_hi'])
    #        a = pymc.Uniform('a', lower=-0.1, upper=0.1, value=p0["a"], size=decomp_poly+1)
            a = pymc.Normal('a', mu=0, tau=1./(0.001**2), value=p0["a"], size=decomp_poly+1)
#            noise = pymc.Uniform('noise', lower=0., upper=1.)
            if self.guess_noise:
                noise_r = pymc.Uniform('noise_real', lower=0., upper=1.)
                noise_i = pymc.Uniform('noise_imag', lower=0., upper=1.)

#            noises = pymc.Lambda('noises', lambda noise=noise: np.reshape(noise, (2,1)))
            # Deterministics
    #        @pymc.deterministic(plot=False)
    #        def m_hi(mp_hi=mp_hi):
    #            return 10**mp_hi / (1 + 10**mp_hi)
            @pymc.deterministic(plot=False)
            def zmod(R0=R0, a=a):
                return Decomp_cyth(w, tau_10, log_taus, c_exp, R0, a)
            @pymc.deterministic(plot=False)
            def m_(a=a):
                return np.sum((a*log_taus.T).T, axis=0)
            @pymc.deterministic(plot=False)
            def total_m(m_=m_):
                return np.sum(m_[(log_tau >= self.log_min_tau)&(m_ >= 0)&(log_tau <= max(log_tau)-1)])
            @pymc.deterministic(plot=False)
            def log_half_tau(m_=m_):
                return log_tau[cond][np.where(np.cumsum(m_[cond])/np.sum(m_[cond]) > 0.5)[0][0]]
            @pymc.deterministic(plot=False)
            def log_peak_tau(m_=m_):
                cond = np.r_[True, m_[1:] > m_[:-1]] & np.r_[m_[:-1] > m_[1:], True]
                cond[0] = False
                try: return log_tau[cond][0]
                except: return log_tau[0]
            @pymc.deterministic(plot=False)
            def log_mean_tau(m_=m_):
                return np.log10(np.exp(old_div(np.sum(m_[cond]*np.log(10**log_tau[cond])),np.sum(m_[cond]))))
            # Likelihood
#            obs = pymc.Normal('obs', mu=zmod, tau=1./((self.data["zn_err"]+noise)**2), value=self.data["zn"], size = (2, len(w)), observed=True)
#            for i in range(2):
#                obs_i = pymc.Normal('obs_%s'%i, mu=zmod[i], tau=1./((self.data["zn_err"][i]+noise[i])**2), value=self.data["zn"][i], size = len(w), observed=True)
            if self.guess_noise:
                obs_r = pymc.Normal('obs_r', mu=zmod[0], tau=1./((noise_r)**2), value=self.data["zn"][0], size = len(w), observed=True)
                obs_i = pymc.Normal('obs_i', mu=zmod[1], tau=1./((noise_i)**2), value=self.data["zn"][1], size = len(w), observed=True)
            else:
                obs = pymc.Normal('obs', mu=zmod, tau=1./(self.data["zn_err"]**2), value=self.data["zn"], size = (2, len(w)), observed=True)

            return locals()
    
    #==============================================================================
        """
        Main section
        """
    #==============================================================================
        # Importing data
        self.data = get_data(self.filename, self.headers, self.ph_units)
        if (self.data["pha_err"] == 0).all():
            self.guess_noise = True
        seigle_m = (old_div((self.data["amp"][-1] - self.data["amp"][0]), self.data["amp"][-1]) ) # Estimating Seigel chargeability
        w = 2*np.pi*self.data["freq"] # Frequencies measured in rad/s
    #    n_freq = len(w)
    #    n_decades = np.ceil(max(np.log10(old_div(1.0,w)))) - np.floor(min(np.log10(old_div(1.0,w))))
        # Relaxation times associated with the measured frequencies (Debye decomposition only)
        log_tau = np.linspace(np.floor(min(np.log10(old_div(1.0,w)))-1), np.floor(max(np.log10(old_div(1.0,w)))+1), 50)
        cond = (log_tau >= min(log_tau)+1)&(log_tau <= max(log_tau)-1)
        log_taus = np.array([log_tau**i for i in range(0,self.decomp_poly+1,1)]) # Polynomial approximation for the RTD
        tau_10 = 10**log_tau # Accelerates sampling
        self.data["tau"] = tau_10 # Put relaxation times in data dictionary
    
        # Time and date (for saving traces)
        sample_name = self.filename.replace("\\", "/").split("/")[-1].split(".")[0]
    #    actual_path = str(path.dirname(path.realpath(argv[0])))
        working_path = getcwd().replace("\\", "/")+"/"
        now = datetime.now()
        save_time = now.strftime('%Y%m%d_%H%M%S')
        save_date = now.strftime('%Y%m%d')
        out_path = '%s/Txt traces/%s/%s/%s-%s-%s/'%(working_path, save_date,
                                                     sample_name, self.model,
                                                     sample_name, save_time)
    
        """
        #==========================================================================
        Call to run_MCMC function
        #==========================================================================
        """
        # "ColeCole", "Dias", "Debye" or "Shin"
        sim_dict = {"ColeCole": {"func": ColeColeModel,     "args": [self.cc_modes]          },
                    "Dias":     {"func": DiasModel,         "args": []                  },
                    "PDecomp":  {"func": PolyDecompModel,   "args": [self.decomp_poly, self.c_exp]},
                    "Shin":     {"func": ShinModel,         "args": []                  },
    #                "Custom":   {"func": YourModel,     "args": [opt_args]   },
                    }
        simulation = sim_dict[self.model] # Pick entries for the selected model
        self.MDL = run_MCMC(simulation["func"](*simulation["args"]), self.mcmc, save_traces=self.keep_traces, save_where=out_path) # Run MCMC simulation with selected model and arguments
    #    if not keep_traces: rmtree(out_path)   # Deletes the traces if not wanted
    
        """
        #==========================================================================
        Results
        #==========================================================================
        """
        self.pm = format_results(self.MDL, self.data["Z_max"]) # Format output
        zmodstats = self.MDL.stats(chain=-1)["zmod"] # Take last chain
        zn_avg = zmodstats["mean"]
        zn_l95 = zmodstats["95% HPD interval"][0]
        zn_u95 = zmodstats["95% HPD interval"][1]
        avg = self.data["Z_max"]*(zn_avg[0] + 1j*zn_avg[1]) # (In complex notation, de-normalized)
        l95 = self.data["Z_max"]*(zn_l95[0] + 1j*zn_l95[1]) # (In complex notation, de-normalized)
        u95 = self.data["Z_max"]*(zn_u95[0] + 1j*zn_u95[1]) # (In complex notation, de-normalized)
        self.fit = {"best": avg, "lo95": l95, "up95": u95} # Best fit dict with 95% HDP
        self.model_type = {"log_min_tau":self.log_min_tau, "c_exp":self.c_exp, "decomp_polyn":self.decomp_poly, "cc_modes":self.cc_modes}
        # Output
#        return {"pymc_model": MDL, "params": pm, "data": data, "fit": fit, "SIP_model": model, "path": filename, "mcmc": mcmc, "model_type": {"log_min_tau":log_min_tau, "c_exp":c_exp, "decomp_polyn":decomp_poly, "cc_modes":cc_modes}}
        # End of inversion
                    
    
    #==============================================================================
"""
References:

Chen, Jinsong, Andreas Kemna, and Susan S. Hubbard. 2008. “A Comparison between
    Gauss-Newton and Markov-Chain Monte Carlo–based Methods for Inverting
    Spectral Induced-Polarization Data for Cole-Cole Parameters.” Geophysics
    73 (6): F247–59. doi:10.1190/1.2976115.
Dias, Carlos A. 2000. “Developments in a Model to Describe Low-Frequency
    Electrical Polarization of Rocks.” Geophysics 65 (2): 437–51.
    doi:10.1190/1.1444738.
Gamerman, Dani, and Hedibert F. Lopes. 2006. Markov Chain Monte Carlo:
    Stochastic Simulation for Bayesian Inference, Second Edition. CRC Press.
Ghorbani, A., C. Camerlynck, N. Florsch, P. Cosenza, and A. Revil. 2007.
    “Bayesian Inference of the Cole–Cole Parameters from Time- and Frequency-
    Domain Induced Polarization.” Geophysical Prospecting 55 (4): 589–605.
    doi:10.1111/j.1365-2478.2007.00627.x.
Hoff, Peter D. 2009. A First Course in Bayesian Statistical Methods. Springer
    Science & Business Media.
Keery, John, Andrew Binley, Ahmed Elshenawy, and Jeremy Clifford. 2012.
    “Markov-Chain Monte Carlo Estimation of Distributed Debye Relaxations in
    Spectral Induced Polarization.” Geophysics 77 (2): E159–70.
    doi:10.1190/geo2011-0244.1.
Nordsiek, Sven, and Andreas Weller. 2008. “A New Approach to Fitting Induced-
    Polarization Spectra.” Geophysics 73 (6): F235–45. doi:10.1190/1.2987412.
Pelton, W. H., W. R. Sill, and B. D. Smith. 1983. Interpretation of Complex
    Resistivity and Dielectric Data — Part 1. Vol 29. Geophysical Transactions.
Pelton, W. H., S. H. Ward, P. G. Hallof, W. R. Sill, and P. H. Nelson. 1978.
    “Mineral Discrimination and Removal of Inductive Coupling with
    Multifrequency IP.” Geophysics 43 (3): 588–609. doi:10.1190/1.1440839.
"""
#==============================================================================
