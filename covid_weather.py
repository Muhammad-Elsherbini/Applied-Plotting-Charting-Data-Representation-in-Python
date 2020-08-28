# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:11:37 2020

@author: Muhammad Elsherbini
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
sns.set_style('dark')
sns.set_palette('bright')
#loading datasets
 
#NYC COVID-19 data
# for more info: https://data.cityofnewyork.us/Health/COVID-19-Daily-Counts-of-Cases-Hospitalizations-an/rc75-m7u3
df_cr = pd.read_csv('COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths .csv')

# LA COVID-19 data
# for more info: https://data.ca.gov/dataset/covid-19-cases

df_crla = pd.read_csv('LA_statewide_cases.csv')

# NY and LA weather data
# for more info: https://www.ncdc.noaa.gov/cdo-web/datasets

df_wn = pd.read_csv('NOAA_nyweather_central_park.csv')
df_wla = pd.read_csv('NOAA_LAweather.csv')

# cleaning datasets

df_cr.columns = ['DATE', 'cases', 'HOSPITALIZED', 'DEATH']
df_cr.drop(columns='HOSPITALIZED', inplace= True)
df_cr.columns = list(map(lambda i : i.lower() , df_cr.columns))

df_cr['cases'] = df_cr['cases'].str.replace(',','') 
df_cr['cases'] = df_cr['cases'].astype(int)

df_crla = df_crla[df_crla['county'] == 'Los Angeles']
df_crla.drop(columns=['county'], inplace= True)

df_wn.drop(columns = ['NAME','STATION'],inplace =True)
df_wn.columns = list(map(lambda x:  x.lower(), df_wn.columns))

df_wla.drop(columns = ['NAME','STATION'],inplace =True)
df_wla.columns = list(map(lambda x:  x.lower(), df_wla.columns))

# using day average to fill nulls in temp avg columns

df_wn['tavg'] = (df_wn['tmax'] + df_wn['tmin'] ) / 2
df_wla['tavg'] = (df_wla['tmax'] + df_wla['tmin'] ) / 2

df_cr.date = pd.to_datetime(df_cr.date)
df_wn.date = pd.to_datetime(df_wn.date)
df_wla.date = pd.to_datetime(df_wla.date)
df_crla.date = pd.to_datetime(df_crla.date)

# setting the index to date columns in both data sets

df_wn.set_index('date',inplace= True)
df_cr.set_index('date',inplace= True)
df_crla.set_index('date',inplace= True)
df_wla.set_index('date',inplace= True)

# merging the datasets

df_msn = df_wn.merge(df_cr, how='inner', left_index= True, right_index=True)
df_msla = df_wla.merge(df_crla, how='inner', left_index= True, right_index=True)
df_msn = df_msn.iloc[18:,:]

# plotting tempreture and cases count for NYC

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(8,8))
df_wn.tavg.plot(ax=ax1, c= 'darkorange', alpha =.7,sharex=True)
ax1.set_title('average temperature in NYC')
df_cr.cases.plot(ax = ax2, alpha=.7)
ax1.grid()
ax2.set_title('number of cases in NYC')
ax2.xaxis.label.set_visible(False)
ax2.grid()
plt.show()

# overlay tempreture with cases count
fig, ax1 = plt.subplots(1,1, figsize=(8,4))
df_wn.tavg.plot(ax=ax1, c= 'darkorange',alpha=.7, label ='temperature')
ax1.set_title('average temperature (in c) vs cases count in NYC')
plt.grid()
ax2 = ax1.twinx()
df_cr.cases.plot(ax = ax2, label= 'cases', alpha=.7)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=7)
ax1.xaxis.label.set_visible(False)
plt.show()

# plotting tempreture and cases count for LA

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(8,8))
df_wla.tavg.plot(ax=ax1, c= 'darkorange',alpha= .7,sharex=True)
ax1.set_title('average temperature in LA')
df_crla.cases.plot(ax = ax2, alpha=.7)
ax1.grid()
ax2.set_title('number of cases in LA')
ax2.xaxis.label.set_visible(False)
ax2.grid()
plt.show()

# overlay tempreture with cases count
fig, ax1 = plt.subplots(1,1, figsize=(8,4))
df_wla.tavg.plot(ax=ax1, c= 'darkorange',alpha=.7, label ='temperature')
ax1.set_title('average temperature (in c) vs cases count in LA')
plt.grid()
ax2 = ax1.twinx()
df_crla.cases.plot(ax = ax2, label= 'cases', alpha=.7)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=4)
ax1.xaxis.label.set_visible(False)
plt.show()

ncrr = round(df_msn.tavg.corr(df_msn.cases),3)
lacrr = round(df_msla.tavg.corr(df_msla.cases),3)

# plotting scatter plot of tempreture and cases


plt.figure()
l = df_msn.plot.scatter('tavg','cases', c = 'cases', cmap='viridis', sharex=False,figsize=(8,4))
plt.title('correlation between tempreture and cases\nin NYC: {}'.format(ncrr))
l.yaxis.set_visible(False)
l.xaxis.label.set_visible(False)
plt.grid()
plt.show()


plt.figure()
l = df_msla.plot.scatter('tavg','cases', c = 'cases', cmap='viridis',sharex=False,figsize=(8,4))
plt.grid()
plt.title('correlation between tempreture and cases\nin LA: {}'.format(lacrr))
l.xaxis.label.set_visible(False)
l.yaxis.set_visible(False)
plt.show()

# plotting a master figure
fig = plt.figure(figsize=(16,18))
grid = gridspec.GridSpec(3,2)

ax1 = fig.add_subplot(grid[0, :])

df_wn.tavg.plot(ax=ax1, c= 'darkorange',alpha=.7, label ='temperature')
ax1.set_title('Average temperature (in c) vs cases count in NYC')
plt.grid()
ax1a = ax1.twinx()
df_cr.cases.plot(ax = ax1a, label= 'cases', alpha=.7)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax1a.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc=2)
ax1.xaxis.label.set_visible(False)

ax2 = fig.add_subplot(grid[1, :])

df_wla.tavg.plot(ax=ax2, c= 'darkorange',alpha=.7, label ='temperature')
ax2.set_title('Average temperature (in c) vs cases count in LA')
plt.grid()
ax2a = ax2.twinx()
df_crla.cases.plot(ax = ax2a, label= 'cases', alpha=.7)
lines, labels = ax2.get_legend_handles_labels()
lines2, labels2 = ax2a.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=2)
ax2.xaxis.label.set_visible(False)

ax3 = fig.add_subplot(grid[2, 0])

l = df_msn.plot.scatter('tavg','cases',ax= ax3 ,c = 'cases', cmap='viridis', sharex=False)
plt.title('correlation between tempreture and cases\nin NYC: {}'.format(ncrr))
l.yaxis.set_visible(False)
l.xaxis.label.set_visible(False)

ax4 = fig.add_subplot(grid[2, 1])

l = df_msla.plot.scatter('tavg','cases',ax= ax4, c = 'cases', cmap='viridis',sharex=False)
plt.grid()
plt.title('correlation between tempreture and cases\nin LA: {}'.format(lacrr))
l.xaxis.label.set_visible(False)
l.yaxis.set_visible(False)
plt.show()