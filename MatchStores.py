import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

#%%
lines = pd.Series(open('storelocatorasda.txt').read().splitlines()) #read in data
walmartno = []
#%%
for i in range(len(lines)):
    if lines[i].count("<WalMartNo>"): 
        s1 = lines[i].find("<WalMartNo>")+11 
        if lines[i].count("</WalMartNo>"):
            s2 = lines[i].find("</WalMartNo>")
        walmartno.append(lines[i][s1:s2])
walmartno = pd.Series(walmartno) 
walmartno = walmartno.rename("WalMartNo")

#%%
lat = []
for i in range(len(lines)):
    if lines[i].count("<Lat>"): 
        s1 = lines[i].find("<Lat>")+5 
        if lines[i].count("</Lat>"):
            s2 = lines[i].find("</Lat>")
        lat.append(lines[i][s1:s2])
lat = pd.Series(lat) 
lat = lat.rename("Lat")

#%%
lon = []
for i in range(len(lines)):
    if lines[i].count("<Lon>"): 
        s1 = lines[i].find("<Lon>")+5 
        if lines[i].count("</Lon>"):
            s2 = lines[i].find("</Lon>")
        lon.append(lines[i][s1:s2])
lon = pd.Series(lon) 
lon = lon.rename("Lon")
asdastores = pd.concat([walmartno,lat,lon],axis =1)

#%%
import datetime as dt
import random

import time

def randtimegen(start,end):
    stime = time.mktime(time.strptime(start, '%m/%d/%Y %I:%M %p'))
    etime = time.mktime(time.strptime(end, '%m/%d/%Y %I:%M %p'))
    ptime = stime + random.random() * (etime - stime)
    return time.strftime('%m/%d/%Y %I:%M %p', time.localtime(ptime))
  
randdt = []
for i in range(50000):
    randdt.append(randtimegen("1/1/2017 12:00 AM","12/31/2017 11:59 PM"))
randdt = pd.Series(randdt)
randdt = randdt.rename('Random Time Stamps')
#%%
randomlocations = []
randomlat = []
randomlon = []
for i in range(40000):
    randnum = random.randint(0,len(asdastores)-1)
    randomlocations.append(asdastores['WalMartNo'].loc[randnum])
    randomlat.append(asdastores['Lat'].loc[randnum])
    randomlon.append(asdastores['Lon'].loc[randnum])
randomlocations = (pd.Series(randomlocations)).rename('Random Store Num')
randomlat = (pd.Series(randomlat)).rename('Lat')
randomlon = (pd.Series(randomlon)).rename('Lon')
randomsample = pd.concat([randomlocations,lat,lon,randdt],axis = 1)

#%%
#randpurchasetimespos = pd.date_range('1/1/2017','12/31/2017',periods = 50000)
randpurchasetimespos = []
for i in range(50000):
    randpurchasetimespos.append(randtimegen("1/1/2017 12:00 AM","12/31/2017 11:59 PM"))
randpurchasetimespos = pd.Series(randpurchasetimespos)
randpurchasetimespos = randpurchasetimespos.rename('Time Stamp POS')

randomproductcodepos = []
for i in range(50000):
    randomproductcodepos.append(random.randint(0,100))

randomstorelocpos = []
for i in range(50000):
    tempstorenum = asdastores['WalMartNo'].loc[random.randint(0,asdastores['WalMartNo'].size-1)]
    randomstorelocpos.append(tempstorenum)

randomproductcodepos = (pd.Series(randomproductcodepos)).rename('Prod Code')
randomstorelocpos = (pd.Series(randomstorelocpos)).rename('Store Location')

randomsamplepos = pd.concat([randpurchasetimespos,randomproductcodepos,randomstorelocpos],axis = 1)
randomsamplepos['Customer id'] = randomsamplepos.index

### end of creating the sample data, in a format where you can put in real data

#%%
randomsample['Random Time Stamps'] = pd.to_datetime(randomsample['Random Time Stamps'])
randomsamplepos['Time Stamp POS'] = pd.to_datetime(randomsamplepos['Time Stamp POS'])



#%%
#gran = randomsamplepos.groupby(['Store Location'])
gran = randomsample.groupby(['Random Store Num'])


#for key, item in gran:
#    print(gran.get_group(key), "\n\n")
#%%
gb = gran.groups    #all 646 stores

grandf = pd.DataFrame()
for i in gb:
    grandf = grandf.append(gran.get_group(i))


#%%
randomsample.drop(['Lat', 'Lon'], axis=1, inplace=True)   # getting rid of lat and lon columns, key with asdastores
#%%

granpos = randomsamplepos.groupby(['Store Location'])
gbpos = gran.groups
granposdf = pd.DataFrame()

#%%
grancount = randomsample.groupby(['Random Store Num']).count()
granposcount = randomsamplepos.groupby(['Store Location']).count()
rarestores = ~granposcount.index.isin(grancount.index)
rarestores = pd.Series(rarestores)  #index that we want to delete
rarestores = rarestores.rename('Bool')
storestodelete = rarestores.index[rarestores == True].tolist()   #get the storenums to delete from rarestores index
if len(storestodelete) != 0:
    randomsamplepos = randomsamplepos[~randomsamplepos['Store Location'].isin(storestodelete)] #deletes records that contains stores in storestodelete

#%%
matches = pd.DataFrame()

for i in gbpos:
    tempgran = gran.get_group(i)
    tempgranpos = granpos.get_group(i)
    tempgran = tempgran.sort_values(by=['Random Time Stamps'])
    tempgranpos = tempgranpos.sort_values(by = ['Time Stamp POS'])
    tempgransmerged = pd.merge_asof(tempgran,tempgranpos,left_on = 'Random Time Stamps', 
                                right_on = 'Time Stamp POS', tolerance=pd.Timedelta('1h'))
    matches = matches.append(tempgransmerged)
    matches = matches.dropna()
#%%
 
matchescleaned = pd.concat([matches['Time Stamp POS'],matches['Prod Code'],
                            matches['Store Location'],matches['Customer id']],axis = 1)
# also code for scenario where some stores have no records

#%%
matchescleaned.to_csv('matchescleaned.csv', index = False)

## get more data into this program

