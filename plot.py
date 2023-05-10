#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

f,ax = plt.subplots(2,figsize=(6,8))

# consumer price index
date = []
cpi = []
with open('CPIAUCSL.csv') as f:
    for row in csv.reader(f):
        date.append(dates.datestr2num(row[0]))
        cpi.append(float(row[1]))

# local rent cpi
boston_rent_cpi = []
with open('CUURA103SEHA.csv') as f:
    for row in csv.reader(f):
        boston_rent_cpi.append(float(row[1]))

national_rent_cpi = []
with open('CUSR0000SEHA.csv') as f:
    for row in csv.reader(f):
        national_rent_cpi.append(float(row[1]))

# median weekly earnings
mwe = []
mwe_date = []
with open('LES1252881500Q.csv') as f:
    for row in csv.reader(f):
        mwe_date.append(dates.datestr2num(row[0]))
        mwe.append(float(row[1]))

# stipend data from advertisements on wayback machine
years = ['2011-09-01','2012-09-01','2014-09-01','2016-09-01','2017-09-01',
         '2018-09-01','2019-09-01','2020-09-01','2021-09-01','2022-09-01']
stipends = [64500,65500,66500,67500,68000,68500,69500,70500,71600,75000]
# convert to matplotlib date format in place
for i in range(len(years)):
    years[i] = dates.datestr2num(years[i])

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

ax[0].legend(loc=2,fontsize='small')
#ax[0].set_ylim(63000,99000)
ax[0].set_title('Astro Prize Fellowship Stipends')

### add in some extrapolations to the end of this academic year
interp_cpi = interp1d(date,cpi,fill_value='extrapolate')
interp_rent = interp1d(date,national_rent_cpi,fill_value='extrapolate')
ext_start = dates.datestr2num('2022-09-01')
ext_end = dates.datestr2num('2023-09-01')
ext_range = np.linspace(ext_end,ext_start) # reverse order for dash linestyle
ax[0].plot(ext_range,interp_cpi(ext_range),ls='--',c='tab:blue')
ax[0].plot(ext_range,interp_actual(ext_range),ls='--',c='k')
#ax[0].plot(ext_range,interp_rent(ext_range),ls='--',c='tab:red')

ax[0].set_ylabel('Stipend (\$)')


ax[1].set_title('Prize Fellowship Stipends Adjusted for Inflation')
ymax = 87000
ymin = 73000
ax2 = ax[1].twinx()
ax2.set_ylim(ymin,ymax)
ax2.set_ylabel('Stipend in Real Dollars (April 2023)')
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
         dates.datestr2num('2023-01-01')]

date_form = dates.DateFormatter("%Y")
start = dates.datestr2num('2011-06-01')
end = dates.datestr2num('2023-12-01')
for a in [ax[0],ax[1],ax2]:
    a.set_xticks(ticks)
    a.xaxis.set_major_formatter(date_form)
    a.set_xlim(start,end)

plt.savefig('Stipends.png')
#plt.savefig('Stipends.pdf')
