# -*- coding: utf-8 -*-

"""
Created on 06/08/2019
@author: GUIGNARDAN
Project: ShadowMS

Fork of read_credit.py with statsmodels
treatment as dataframe instead of time series
"""

import os
from os import listdir
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
#
import numpy as np
#import scipy
from statsmodels.tsa.seasonal import seasonal_decompose

import stat
import xlrd
from datetime import datetime


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



data_path = 'C:/Users\GuignardAn\Documents\ShadowMS\data\modelization'
plot_path = 'C:/Users\GuignardAn\Documents\ShadowMS\data\modelization\plots'

input_files = [f for f in listdir(data_path) if '.csv' in f]
print('Input files', input_files)

#todo: lire le fichier CREDIT
file_credit = os.path.join(data_path,'credits_histo_complet_sans_total.csv')

# stay in dataframe
df_init = pd.read_csv(file_credit, parse_dates=['date'])



###############################################################
#
#                Traitement sous forme de séries
#
###############################################################


# ordering (ascending dates)
df = df_init.sort_values("date")

dates = df['date'].values
paies = df['Paie PSOP'].values

# Coupures / sélection des données
c = df['Regroupement de comptes généraux']
i = df['intitulé_dépense']
idx = [x for x in range(0, len(c.values)) if c.values[x] == '210' and i.values[x] == 'CDI REMUNERATION SUR PRINCIPAL']
# print('len(idx)', len(idx))
# print('(idx)', (idx))



xh = [dates[i] for i in idx]
yh = [paies[i] for i in idx]


#todo: create a date range for simulations
xf = pd.date_range('2019-01-01','2021-01-01' , freq='1M')
yf1 = [yh[i]*1.5 for i in range(0,len(xf))]

#todo: forecasting here
yf2 = [yh[i]*2 for i in range(0,len(xf))]


#todo: decompose time series into its components
if 1:
    # trend

    # seasonnality (cyclic)

    df_test = df[['date','Paie PSOP']]

    df_test.reset_index(inplace=True)
    # df_test['date'] = pd.to_datetime(df_test['date'])
    df_test = df_test.set_index('date')

    # en mode dataframe
    # result_mul = seasonal_decompose(df_test, model='additive', filt=None, freq=None, extrapolate_trend=0)

    # en mode time series, il faut spécifier la fréquence
    result_mul = seasonal_decompose(yh, model='multiplicative', filt=None, freq=12, extrapolate_trend=0)
    # print('\n result_trend): ',result_mul.trend)
    # print('\n result_seasonal: ',result_mul.seasonal)
    # print('\n result_resid: ',result_mul.resid)
    # print('\n result_observed: ',result_mul.observed)       #les valeurs observées

    result_add = seasonal_decompose(yh, model='additive', filt=None, freq=12, extrapolate_trend=0)
    # print('\n result_trend): ',result_mul.trend)
    # print('\n result_seasonal: ',result_mul.seasonal)
    # print('\n result_resid: ',result_mul.resid)
    # print('\n result_observed: ',result_mul.observed)       #les valeurs observées

    # print('result_mul', result_mul)
    # # noise







# plotting
if 1:
    plot_file = os.path.join(plot_path,'evolution_credits.png')

    fig, ax = plt.subplots(1, 1, figsize=(16,5), dpi= 80)
    plt.plot(xh, yh, color='tab:blue', label='Actual')
    plt.title('Evolution de Paie PSOP pour rémunération ppale des CDI(non corrigée)', fontsize=16)


    ax.xaxis.set_minor_locator(AutoMinorLocator())

    ax.tick_params(which='both', width=2)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=3, color='k')




    plt.hlines(y=0, xmin=np.min(xh), xmax=np.max(xh), linewidth=.5)
    plt.plot(xf, yf1, color='tab:red', linestyle='-.', label='Estimate_1')
    plt.plot(xf, yf2, color='tab:orange', linestyle='-.', label='Estimate_2')

    # Trend Analysis of the time-series
    plt.plot(xh, result_add.trend+20000., color='tab:orange', linestyle='-.', label='Trend +')
    plt.plot(xh, result_mul.trend, color='tab:olive', linestyle='-.', label='Trend x')

    plt.plot(xh, result_mul.seasonal*20., color='magenta', linestyle='-.', label='Cyclic x 20')
    plt.plot(xh, result_mul.resid, color='crimson', linestyle='-.', label='Residual')

    plt.ylim(0, 1.5*np.max(yh))
    plt.legend()

    plt.show()
    # plt.savefig(plot_file)
    # plt.close(fig)







# print('\n', 'credit.keys', credit.keys())
#['Autres dépenses HPSOP', 'Paie HPSOP', 'Paie PSOP',
# 'Regroupement de comptes généraux', 'Total Consommation',
# 'année', 'compte', 'date', 'intitulé_dépense', 'mois']


# Other files reading (emplois, vpfp etc ...)
if 0:
    #todo: lire le fichier EMPLOI
    file_emploi = os.path.join(data_path,'emploi_histo_complet_sans_total.csv')
    df = pd.read_csv(file_emploi)
    emploi = df.to_dict()
    print('\n', 'emploi.keys', emploi.keys())

    #todo: lire le fichier VPFP
    file_VPFP = os.path.join(data_path,'evolution_VPFP_date.csv')
    df = pd.read_csv(file_VPFP)
    vpfp = df.to_dict()
    print('\n', 'vpfp.keys', vpfp.keys())

    #todo: lire le fichier CAS
    file_cas = os.path.join(data_path,'evolution_taux_cas_pensions_date.csv')
    df = pd.read_csv(file_cas)
    cas = df.to_dict()
    print('\n', 'cas.keys', cas.keys())



