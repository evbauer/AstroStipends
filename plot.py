#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

f,ax = plt.subplots(2,figsize=(6,8))

# consumer price index
data = pd.read_csv('CPIAUCSL.csv')
date = dates.datestr2num(data['Date'].to_numpy())
cpi = data['CPI'].to_numpy()

# local rent cpi
boston_data = pd.read_csv('CUURA103SEHA.csv')
boston_rent_cpi = boston_data['Rent_CPI'].to_numpy()

#national rent cpi
national_data = pd.read_csv('CUSR0000SEHA.csv')
national_rent_cpi = national_data['Rent_CPI'].to_numpy()

# median weekly earnings
mwe_data = pd.read_csv('LES1252881500Q.csv')
mwe_date = dates.datestr2num(mwe_data['Date'].to_numpy())
mwe = mwe_data['MWE'].to_numpy()

# stipend data from advertisements on wayback machine
years = ['2011-09-01','2012-09-01','2014-09-01','2016-09-01','2017-09-01',
         '2018-09-01','2019-09-01','2020-09-01','2021-09-01','2022-09-01',
         '2023-09-01','2024-09-01']
stipends = [64500,65500,66500,67500,68000,68500,69500,70500,71600,75000,79500,82500]

years_GS = ['2012-01-01','2013-01-01','2014-01-01','2015-01-01','2016-01-01',
            '2017-01-01','2018-01-01','2019-01-01','2020-01-01','2021-01-01',
            '2022-01-01','2023-01-01','2024-01-01']
GS11_pay = [62758,62758,63386,64020,64862,66317,67643,69016,71274,71987,74129,77738,81963]
# convert to matplotlib date format in place
for i in range(len(years)):
    years[i] = dates.datestr2num(years[i])
for i in range(len(years_GS)):
    years_GS[i] = dates.datestr2num(years_GS[i])

# take first stipend entry and scale cpi and rents accordingly
cpi = np.array(cpi)*stipends[0]/cpi[0]
boston_rent_cpi = np.array(boston_rent_cpi)*stipends[0]/national_rent_cpi[0]
national_rent_cpi = np.array(national_rent_cpi)*stipends[0]/national_rent_cpi[0]

ax[0].plot(date,boston_rent_cpi,
           label='2011 Stipend Adjusted to \nBoston-Cambridge-Newton Rent CPI \n(relative to National Rent CPI)',
           c='tab:red',ls=':')

ax[0].plot(date,national_rent_cpi,label='2011 Stipend Adjusted to US Rent CPI',c='tab:red')

ax[0].plot(mwe_date,np.array(mwe)*stipends[0]/mwe[0],c='tab:green',
           label='2011 Stipend Adjusted to US Median Earnings')

ax[0].plot(date,cpi,label='2011 Stipend Adjusted to US CPI',c='tab:blue')


ax[0].scatter(years,stipends,c='k',label='Actual Stipends')
interp_actual = interp1d(years,stipends,kind='previous',fill_value='extrapolate')
ax[0].plot(date,interp_actual(date),c='k')

interp_GS = interp1d(years_GS,GS11_pay,kind='previous',fill_value='extrapolate')
#ax[0].plot(date,interp_GS(date),c='tab:gray',ls='--')
#ax[0].scatter(years_GS,GS11_pay,c='tab:gray',marker='*',s=100,label='GS-11 Step 1')

ax[0].legend(loc=2,fontsize='small')
#ax[0].set_ylim(63000,99000)
ax[0].set_title('Astro Prize Fellowship Stipends')

### add in some extrapolations to the end of this academic year
interp_cpi = interp1d(date,cpi,fill_value='extrapolate')
interp_rent = interp1d(date,national_rent_cpi,fill_value='extrapolate')
ext_start = dates.datestr2num('2024-09-01')
ext_end = dates.datestr2num('2025-09-01')
ext_range = np.linspace(ext_end,ext_start) # reverse order for dash linestyle
ax[0].plot(ext_range,interp_cpi(ext_range),ls='--',c='tab:blue')
ax[0].plot(ext_range,interp_actual(ext_range),ls='--',c='k')
#ax[0].plot(ext_range,interp_rent(ext_range),ls='--',c='tab:red')

ax[0].set_ylabel('Stipend (\$)')


ax[1].set_title('Prize Fellowship Stipends Adjusted for Inflation')
ymax = 90000
ymin = 75000
ax2 = ax[1].twinx()
ax2.set_ylim(ymin,ymax)
ax2.set_ylabel('Stipend in Real Dollars (September 2024)')
ax[1].grid(False,axis='y')
ax[1].set_ylabel('Stipend in 2011 Dollars')
ax[1].set_ylim(ymin*cpi[0]/cpi[-1],ymax*cpi[0]/cpi[-1])

ax2.plot(date,interp_actual(date)*cpi[-1]/cpi)
ax2.scatter(years,interp_actual(years)*cpi[-1]/interp_cpi(years),c='k')

### add in extrapolation
ax2.plot(ext_range,interp_actual(ext_range)*cpi[-1]/interp_cpi(ext_range),c='tab:blue',ls='--')


# matplotlib is doing stupid things with ticks, so set them manually
ticks = [dates.datestr2num('2012-01-01'),
         dates.datestr2num('2013-01-01'),
         dates.datestr2num('2014-01-01'),
         dates.datestr2num('2015-01-01'),
         dates.datestr2num('2016-01-01'),
         dates.datestr2num('2017-01-01'),
         dates.datestr2num('2018-01-01'),
         dates.datestr2num('2019-01-01'),
         dates.datestr2num('2020-01-01'),
         dates.datestr2num('2021-01-01'),
         dates.datestr2num('2022-01-01'),
         dates.datestr2num('2023-01-01'),
         dates.datestr2num('2024-01-01'),
         dates.datestr2num('2025-01-01')]

date_form = dates.DateFormatter("%Y")
start = dates.datestr2num('2011-06-01')
end = dates.datestr2num('2026-01-01')
for a in [ax[0],ax[1],ax2]:
    a.set_xticks(ticks)
    a.xaxis.set_major_formatter(date_form)
    a.set_xlim(start,end)

#plt.savefig('Stipends.png')
plt.savefig('Stipends.pdf')
