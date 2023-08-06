"""
 BAYESFIT (MAIN FILE) 
 Created by: Michael Slugocki
 Created on: September 28, 2017
 License: Apache 2.0
"""

# Import modules
import numpy as np
from copy import deepcopy 
import scipy as sc 
import pystan as ps 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define wrapper function
def bayesfit_build(data, options):

    # Check data structure provided by user
    # Format requested is a N x 3 data frame such that [x, y, N]
    if data.shape[1] != 3:
        raise Exception('Data provided does not contain the number of columns required! (i.e., [x, y, N])') 
    assert data.y.min() >= 0, 'The y-values provided contain a proportion less than zero! ' 
    assert data.y.max() <= 1, 'The y-values provided contain a proportion greater than one! ' 

    # Check user input for options
    if not('options' in locals()): 
        options = dict()
    else:
        options = deepcopy(options)
    if not('sigmoidType' in options.keys()):
        options['sigmoidType'] = 'weibull'
    if not('nAFC' in options.keys()):
        options['nAFC'] = 2
    if not('lapse' in options.keys()):
        options['lapse'] = True
    if not('fit' in options.keys()):
        options['fit'] = 'auto'
    # Check sigmoid type provided to convert to logspace where necessary 
    if options['sigmoidType'] in ['weibull']:
        assert data.x.min() > 0, 'The sigmoid you specified is not defined for negative data points!'

    # Check options provided 
    if options['fit'] != 'auto' and 'manual' == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'
    if options['lapse'] != True and False == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'        
    if options['sigmoidType'] != 'cnorm' and 'logistic' and 'cauchy' and 'gumbel' and 'weibull' == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'                
    if isinstance(options['nAFC'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["nAFC"].'

    # File that performs main computation
    output = bayesfit_compile(data,options)
        
    return output


# Define core fitting 
def bayesfit_compile(data, options, model_definition=dict()):
    
    if not('model_definition' in locals()):
        if options['fit'] == 'auto':
            model_definition = dict()
        elif options['fit'] == 'manual':
            assert False, 'Manual fit option chosen!  Need to provide full model definition!'
    
    if not('nAFC' in options.keys()):
        options['nAFC'] = 2
    
    if options['fit'] == 'auto':
        
        # Get initial estimate of alpha via linear regression
        def scale_est(data,options):
            y = [data.y[0], data.y[data.y.shape[0]-1]]
            x = [data.x[0], data.x[data.x.shape[0]-1]] 
            init_scale = np.polyfit(x, y, 1)
            scale_estimate = [(0.70 - init_scale[1]) / init_scale[0]]
            return scale_estimate[0]
        # Use function to obtain estimate of alpha     
        scale_guess = scale_est(data, options) 
        

        # Define gamma
        if options['nAFC'] == 0:
            gamma = 0
        else:
            gamma = 1/options['nAFC']
        
        # DEFINE DATA STRUCTURE
        model_definition['data'] = '''
            data {
            int<lower=1> N;
            vector[N] x;
            int<lower=0,upper=1> y[N];
            }'''    
        
        # DEFINE SIGMOID SPECIFIC LIKELIHOOD DEFINITIONS
        if options['sigmoidType'] == 'cnorm':    
            model_definition['parameters_pt1'] = '''
                parameters {
                real<lower=0> mu;
                real<lower=0> sigma; '''
            model_definition['likelihood_scale'] = ('''model {mu ~ normal(%f,3);''' %(scale_guess))
            model_definition['likelihood_shape'] = '''sigma ~ normal(3,5);'''
            model_definition['likelihood_model_pt2'] = ''' *normal_cdf(x[i],mu, sigma));}} '''  
    
        elif options['sigmoidType'] == 'logistic':    
            model_definition['parameters_pt1'] = '''
                parameters {
                real<lower=0> mu;
                real<lower=0> sigma; '''
            model_definition['likelihood_scale'] = ('''model {mu ~ normal(%f,3);''' %(scale_guess))
            model_definition['likelihood_shape'] = '''sigma ~ normal(3,5);'''
            model_definition['likelihood_model_pt2'] = ''' *logistic_cdf(x[i],mu, sigma));}} '''  
    
        elif options['sigmoidType'] == 'cauchy':    
            model_definition['parameters_pt1'] = '''
                parameters {
                real<lower=0> mu;
                real<lower=0> sigma; '''
            model_definition['likelihood_scale'] = ('''model {mu ~ normal(%f,3);''' %(scale_guess))
            model_definition['likelihood_shape'] = '''sigma ~ normal(3,5);'''
            model_definition['likelihood_model_pt2'] = ''' *cauchy_cdf(x[i],mu, sigma));}} '''  
    
        elif options['sigmoidType'] == 'gumbel':    
            model_definition['parameters_pt1'] = '''
                parameters {
                real<lower=0> mu;
                real<lower=0> beta; '''
            model_definition['likelihood_scale'] = ('''model {mu ~ normal(%f,3);''' %(scale_guess))
            model_definition['likelihood_shape'] = '''beta ~ normal(3,5);'''
            model_definition['likelihood_model_pt2'] = ''' *gumbel_cdf(x[i],mu, beta));}} ''' 
    
        elif options['sigmoidType'] == 'weibull':
            model_definition['parameters_pt1'] = '''
                parameters {
                real<lower=0> alpha;
                real<lower=0> beta; '''
            model_definition['likelihood_scale'] = ('''model {alpha ~ normal(%f,3);''' %(scale_guess))
            model_definition['likelihood_shape'] = '''beta ~ normal(3,5);'''
            model_definition['likelihood_model_pt2'] = ''' *weibull_cdf(x[i],beta, alpha));}} '''

        # DEFINE LAPSE SPECIFIC STRUCTURES AND LIKELIHOOD FUNCTIONS
        if options['lapse'] == True:
            model_definition['parameters_pt2'] = '''
                real<lower=0> lambda;
                }'''
            model_definition['likelihood_lambda'] = '''   
                lambda ~ beta(2,20); '''   
            model_definition['likelihood_model_pt1'] = ('''  for (i in 1:N){y[i] ~ bernoulli(%f + (1-lambda-%f) ''' %(gamma, gamma))

        else:     
            model_definition['parameters_pt2'] = '''}'''
            model_definition['likelihood_lambda'] = '''  '''   
            model_definition['likelihood_model_pt1'] = ('''  for (i in 1:N){y[i] ~ bernoulli(%f + (1-%f) ''' %(gamma, gamma))

        
#        model_definition['likelihood_model_middle_pt1'] = (''' y[i] ~ bernoulli(%f + (1-lambda-%f)*weibull_cdf(x[i],beta, alpha));} ''' %(gamma, gamma))

        # Combine full model together
        model_definition['full_model'] = model_definition['data'] + model_definition['parameters_pt1'] + model_definition['parameters_pt2'] + model_definition['likelihood_scale'] + model_definition['likelihood_shape'] + model_definition['likelihood_lambda'] + model_definition['likelihood_model_pt1'] + model_definition['likelihood_model_pt2'] 

        # Compile model in STAN
        model = ps.StanModel(model_code = model_definition['full_model']) 
    
    elif options['fit'] == 'manual':
        model = ps.StanModel(model_code = model_definition) 
    
    return model
    
    
    
def bayesfit(data, options, model):
    
    if not('iter' in options.keys()):
        options['iter'] = 5000
    if not('chains' in options.keys()):
        options['chains'] = 2  
    
    # Check options provided are numerical
    if isinstance(options['iter'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["iter"].'    
    if isinstance(options['chains'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["chains"].'
    
    # Convert from average to numerical 1 and 0 sequence
    df = pd.DataFrame([],columns=['x','y']) 
    for i in range(len(data.x)):
        approx_numsequence = np.round(data.y[i]*data.N[i])   
        response_y = np.zeros(data.N[i])
        response_y[:int(approx_numsequence)] = 1
        response_x = np.repeat(data.x[i],data.N[i])
        tmp_df = pd.DataFrame(np.column_stack((response_x,response_y)), columns=['x','y'])
        df = df.append(tmp_df)
    
    # Convert data frame above to list 
    x = [int(i) for i in pd.Series.tolist(df.x)]
    y = [int(i) for i in pd.Series.tolist(df.y)]
    data_model= {'N': len(df.x),'x': x,'y': y}

    # Generate samples from compiled model 
    fit = model.sampling(data=data_model, iter=options['iter'], chains=options['chains'])
    return fit 



def bayesfit_extract(data, options, fit):
    
    if not('param_ests' in options.keys()):
        options['param_ests'] = 'mean'
    if not('thresholdPC' in options.keys()):
        options['thresholdPC'] = .75
    if not('nAFC' in options.keys()):
        options['nAFC'] = 2
    if not('sigmoidType' in options.keys()):
        options['sigmoidType'] = 'weibull'
    if not('lapse' in options.keys()):
        options['lapse'] = True
    
    # Check arguments provided are numerical for threshold
    if options['param_ests'] != 'mean' == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'
    if isinstance(options['thresholdPC'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["thresholdPC"].'
    if isinstance(options['nAFC'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["nAFC"].'
    if options['sigmoidType'] != 'cnorm' and 'logistic' and 'cauchy' and 'gumbel' and 'weibull' == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'
    if options['lapse'] != True and False == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'

    # Define gamma
    if options['nAFC'] == 0:
        gamma = 0
    else:
        gamma = 1/options['nAFC']

    # Define lambda
    if options['lapse'] = True:
        lamb = params['lambda'][0]
    elif: options['lapse'] = False:
        lamb = 0

    # Extract summary table
    fit_summary = fit.summary()
    # Extract summary of mean estimates for parameters
    params = pd.DataFrame([fit_summary['summary'][:,0]],columns=fit_summary['summary_rownames']) 
    
    # Extract threshold 
    x = np.linspace(data.x.min(),data.x.max(),1000)
    if options['sigmoidType'] == 'cnorm':  
        y_pred = gamma + (1-lamb-gamma)*sc.stats.norm.cdf(x,params['mu'][0],params['sigma'][0])
    elif options['sigmoidType'] == 'cauchy': 
        y_pred = gamma + (1-lamb-gamma)*sc.stats.cauchy.cdf(x,params['mu'][0],params['sigma'][0])
    elif options['sigmoidType'] == 'logistic':    
        y_pred = gamma + (1-lamb-gamma)*sc.stats.logistic.cdf(x,params['mu'][0],params['sigma'][0])
    elif options['sigmoidType'] == 'gumbel':
        y_pred = gamma + (1-lamb-gamma)*(1-np.exp(10**(params['beta'][0]*(x - params['mu'][0]) )))
    elif options['sigmoidType'] == 'weibull':    
        y_pred = gamma + (1-lamb-gamma)* (1 - np.exp(-((x/params['alpha'][0])**params['beta'][0])))
    
    threshold = np.interp(options['thresholdPC'], y_pred, x)
    
    return params, threshold
    
    
def bayesfit_plot(data, options, fit, params):
    
    if not('plot' in options.keys()):
        options['plot'] = 'cdf'
    if not('nAFC' in options.keys()):
        options['nAFC'] = 2
    if not('sigmoidType' in options.keys()):
        options['sigmoidType'] = 'weibull'
    if not('lapse' in options.keys()):
        options['lapse'] = True

    if isinstance(options['nAFC'], (int, float, complex)) == False:
        assert False, 'Please provide a numerical argument for options["nAFC"].'
    if options['sigmoidType'] != 'cnorm' and 'logistic' and 'cauchy' and 'gumbel' and 'weibull' == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'
    if options['plot'] != 'cdf' and 'density' and '2D_density' and 'trace' == False:
        assert False, 'Options for PLOT provided are not those made available by module. Revise options provided.'
    if options['lapse'] != True and False == False:
        assert False, 'Options provided are not those made available by module. Revise options provided.'

    # Get parameter labels
    x_labels = list(params.columns.values)  
        
     # Define gamma
    if options['nAFC'] == 0:
        gamma = 0
    else:
        gamma = 1/options['nAFC']

    # Define lambda
    if options['lapse'] = True:
        lamb = params['lambda'][0]
    elif: options['lapse'] = False:
        lamb = 0

    if options['plot'] == 'cdf':
        x = np.linspace(data.x.min(),data.x.max(),1000)
        if options['sigmoidType'] == 'cnorm':  
            y_pred = gamma + (1-lamb-gamma)*sc.stats.norm.cdf(x,params['mu'][0],params['sigma'][0])
        elif options['sigmoidType'] == 'cauchy': 
            y_pred = gamma + (1-lamb-gamma)*sc.stats.cauchy.cdf(x,params['mu'][0],params['sigma'][0])
        elif options['sigmoidType'] == 'logistic':    
            y_pred = gamma + (1-lamb-gamma)*sc.stats.logistic.cdf(x,params['mu'][0],params['sigma'][0])
        elif options['sigmoidType'] == 'gumbel':
            y_pred = gamma + (1-lamb-gamma)*(1-np.exp(10**(params['beta'][0]*(x - params['mu'][0]) )))
        elif options['sigmoidType'] == 'weibull':    
            y_pred = gamma + (1-lamb-gamma)* (1 - np.exp(-((x/params['alpha'][0])**params['beta'][0])))
        fig,ax = plt.subplots(1,1)
        ax.scatter(data.x,data.y)
        ax.plot(x,y_pred)  
        ax.set_xlabel('Stimulus Intensity')
        ax.set_ylabel('Proportion correct')
        plt.show()
    elif options['plot'] == 'density':
        sns.set(color_codes=True)
        samples = fit.extract()
        fig,(ax1,ax2,ax3) = plt.subplots(3,1)
        sns.distplot(samples['alpha'],ax=ax1)
        ax1.set(ylabel='Frequency', xlabel=x_labels[0].capitalize())
        sns.distplot(samples['beta'],ax=ax2)
        ax2.set(ylabel='Frequency', xlabel=x_labels[1].capitalize())
        sns.distplot(samples['lambda'],ax=ax3)
        ax3.set(ylabel='Frequency', xlabel=x_labels[2].capitalize())
        fig.tight_layout()
        plt.show()
    elif options['plot'] == '2D_density':
        samples = fit.extract()
        temp_frame = pd.DataFrame(samples,columns=x_labels) 
        fig = sns.jointplot(x = x_labels[0],y = x_labels[1],data=temp_frame, kind="kde")
        plt.show()
    elif options['plot'] == 'trace':
        samples = fit.extract()
        fig,(ax1,ax2,ax3) = plt.subplots(3,1)
        ax1.plot(samples[x_labels[0]])
        ax1.set_xlabel(x_labels[0].capitalize())
        ax2.plot(samples[x_labels[1]])
        ax2.set_xlabel(x_labels[1].capitalize())
        ax3.plot(samples[x_labels[2]])
        ax3.set_xlabel(x_labels[2].capitalize())
        fig.tight_layout()
        plt.show()

  
    
    
    
    
    
    


    
    
  
