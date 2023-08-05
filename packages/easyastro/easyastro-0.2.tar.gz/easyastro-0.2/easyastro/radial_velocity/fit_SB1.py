import numpy as np
import emcee, sys, os, time as timee
from .generate_radial_velocities import calculate_radial_velocity
from astropy.table import Table,Column
from astropy import constants

def liklihood(theta, time, rv1, rv1_e):
    ##########
    # Unpack
    #########
    period, T0, K1, fs, fc, V0, dV0, jitter = theta
    e = fs*fs + fc*fc
    w = np.arctan2(fs,fc)

    ##############
    # Get rv model
    ##############
    rv_model1, rv_model2  = calculate_radial_velocity(time, period = period, \
                                                      T0 = T0, \
                                                      K1 = K1, e= e, w = w,K2 = K1, \
                                                      V0 = V0, dV0 = dV0)
    if True in np.isnan(rv_model1):
        return np.inf
    
    #####################
    # Calculate loglike
    #####################
    if rv1_e == None:
        wt = 1./(jitter**2)
    else:
        wt = 1./(rv1_e**2 + jitter**2)
     

    #print(-0.5 * np.sum((rv1-rv_model1)**2*wt - np.log(wt)))
    lnlike_rv = np.sum((rv1-rv_model1)**2*wt - np.log(wt))

    return lnlike_rv
    
def lnprob(theta, time,rv1,rv1_e, orig_period, orig_T0):
    prior = lnprior(theta, orig_period, orig_T0)
    if prior==np.inf:
        return -np.inf
    return -0.5*prior  -0.5*liklihood(theta, time, rv1, rv1_e)
        
    
def lnprior(theta, orig_period, orig_T0):
    period, T0, K1, fs, fc, V0,dV0, jitter= theta
    e = fs*fs + fc*fc    
    
    ###############################
    # First check step is in range
    ###############################
    
    if (period < 0) or (period > 100):
        return np.inf
    if (K1 < 0) or (K1 > 100):
        return np.inf
    if (e < 0) or (e > 0.5):
        return np.inf
    if (jitter < 0):# or (jitter > 100):
        return np.inf
    if abs(V0) > 200:
        return np.inf
    if abs(dV0) > 1e-5:
        return np.inf
    
    
    #######################################################
    # Now we put a strict (ish) prior on period and epoch
    #######################################################

    return (period - orig_period)**2/(10**-15) + (T0 - orig_T0)**2/(10**-15) + (dV0 - 0)**2/(10**-15) 
    
    
    
        
    

def fit_SB1(time, rv1,  T0, P ,draws=1000, rv1_e = None):
    '''
    Fits the radial velocity lightcurve for an SB1.
    
    Input
    -----
    time : numpy array
        The time stamps of the corrosponding radial velocity measurements.
    rv1 : numpy array
        The radial velocity measurmeents corresponding to time.
    T0 : float
        A first estimate of epoch. A strict prior is imposed on this value.
    P : float
        A first estimate of the period of the system. A strict prior is 
        imposed on this value.
    draws : int
        How many draws to be genereate from 100 Monte Carlo chains.
    rv1_e : numpy array (optional)
        The uncertainty of radial velocity measurements. If left to "None"
        then the weighting (wt) is:
            
            wt = 1./(rv1**2 + jitter**2)
        
        else if specified:
            
            wt = 1./(rv1_e**2 + jitter**2)

    Returns
    -------
    t : astropy Table
        An astropy table containing the results of the Monte Carlo analysis.
    best_model : dictT_tr
        A dictionary containing numerous entries:
            
            "time" : original time stamps.
            
            "time_phase" : phase-folded "time" values with the best fitting
                           period and epoch.
            "rv1" : The best model of radial velocity found by the sampler.
            "rv1_drift_corrected" : The best model of radial velocity
                                    found by the sampler with drifts in 
                                    systematic velocity removed (dV0). To
                                    produce graphs one should plot "time_phase"
                                    against "rv1_drift_corrected".
            "phase" : An equally spaced phase space with 1000 values between
                      0 and 1. 
            "rv1_phase : The best fitting model in phase space with no
                         drift in velocity. 
                         
        For example, one could first plot
        
            "time_phase" VS "rv1_drift_corrected" 
        
        to plot the phase folded data points with no drift. One could then
        plot
        
            "phase" VS "rv1_phase"
            
        to overplot the best fitting model.
        
    sampler : emcee sampler
        The burnt sampler from emcee incase you need it. 
    '''
    ########################################
    # Preliminaries and starting positions
    ########################################
    ndim, nwalkers = 8, 100
    p0 =[]
    # period, T0, K1, fs, fc, V0, dV0, jitter

    while len(p0) < nwalkers:
        theta_test = [np.random.normal(P, 1e-5), np.random.normal(T0, 1e-5), \
                  np.random.normal(23,1e-2), np.random.normal(0.5,1e-4), \
                  np.random.normal(0.1,1e-4), np.random.normal(25.7,1e-2), \
                  np.random.normal(0,1e-7), np.random.normal(2,1e-2)  ]
        
        lnlike_test = lnprior(theta_test, P, T0)
        if lnlike_test != -np.inf:
            p0.append(theta_test)
        
    ################
    # Run the MCMC
    ################
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[time,rv1,rv1_e, P, T0])



#    sampler.run_mcmc(p0, draws)
 

    width=30
    start_time = timee.time()
    for i, result in enumerate(sampler.sample(p0, iterations=draws)):
        n = int((width+1) * float(i) / draws)
        delta_t = timee.time()-start_time# time to do float(i) / n_steps % of caluculations
        time_incr = delta_t/(float(i+1) / draws) # seconds per increment
        time_left = time_incr*(1- float(i) / draws)
        m, s = divmod(time_left, 60)
        h, m = divmod(m, 60)
        sys.stdout.write("\r[{0}{1}] {2}% – {3}h:{4}m:{5:.2f}s".format('#' * n, ' ' * (width - n), 100*float(i) / draws ,h, m, s)) 
  
    ####################
    # Create the Table
    ####################
    t = Table(sampler.flatchain, names=['Period', 'T0', 'K1', 'fs', 'fc', 'V0','dV0', 'jitter'])
    e = np.array(t['fs'])*np.array(t['fs']) + np.array(t['fc'])*np.array(t['fc'])
    w = 180*np.arctan(np.array(t['fs'])/ np.array(t['fc']) ) / np.pi
    K1 = np.array(t['K1'])
    period = np.array(t['Period'])
    mass_func = ((1-e**2)**1.5)*period*86400.1*((K1*10**3)**3)/(2*np.pi*constants.G.value*1.989e30)

    t.add_column(Column(mass_func,name='mass_function'))
    t.add_column(Column(e,name='eccentricity'))
    t.add_column(Column(w,name='argument_periastron'))
    t.add_column(Column(sampler.flatlnprobability,name='loglike'))
    indices = np.mgrid[0:nwalkers,0:draws]
    step = indices[1].flatten()
    walker = indices[0].flatten()
    t.add_column(Column(step,name='step'))
    t.add_column(Column(walker,name='walker'))
    
    
    #####################
    # Get best step
    #####################
    best_idx = np.argmax(t['loglike'])
    period, T0, K1, fs, fc, V0,dV0, jitter, mass_function, eccentricity, argument_periastron, loglike, step, walker = t[best_idx]
    e = fs*fs + fc*fc
    w = np.arctan2(fs,fc)
    while w <0:
        w = w + np.pi


    #print('Mass function: {}'.format(mass_func))
    
    ########################
    # Print best parameters
    #####################
    msg = '''

Best model:
    step:                   {}
    Walker:                 {}
    Loglike:                {:.2f}
    Chi_red:                {:.2f}
        
    Period:                 {:.5f} d
    Epoch:                  {:.5f}
    K1:                     {:.2f} km/s
    fs:                     {:.2f}
    fc:                     {:.2f}
    e:                      {:.2f}
    w:                      {:.2f}
    Systematic velocity:    {:.2f} km/s
    Drift velovity:         {:.2f} km/s
    Jitter:                 {:.2f} km/s

    Mass function           {:.5f} M_sun
'''.format(step, walker, loglike, -0.5*loglike/8.,
    period, T0, K1, fs, fc,e,w, V0,dV0, jitter,mass_function)
    
    print(msg)   
    
    ####################
    # return best model
    ####################
    best_model = {}
    best_model['time'] = time
    best_model['time_phase'] = (((time-T0)/P + 0.5) % 1) -0.5

    best_model['rv1_model'] = calculate_radial_velocity(time, period = period, \
                                                      T0 = T0, \
                                                      K1 = K1, e= e, w = w, \
                                                      V0 = V0, dV0 = dV0)[0]
    best_model['rv1_drift_corrected'] = rv1 + (dV0 * (time-T0))
    
    
    ###########################
    # return best phased model
    ###########################
    best_model['phase'] = np.linspace(-0.5,0.5,1000)
    best_model['rv1_phase'] = calculate_radial_velocity(best_model['phase'], period = 1.0, \
                                                      T0 = 0.0, \
                                                      K1 = K1, e= e, w = w, \
                                                      V0 = V0, dV0 = 0)[0]
    
    return t, best_model, sampler
