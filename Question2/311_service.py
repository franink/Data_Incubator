
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[2]:

db = pd.read_csv('311_Service_Requests_from_2010_to_Present.csv')


# In[3]:

db.head()


# In[4]:

db.keys()


# In[8]:

db['Created Date'].head()


# In[14]:

quest1 = db.groupby('Agency', sort=False).count()
quest1


# In[17]:

sizes = db.groupby('Agency', sort=False).size()


# In[21]:

sizes.sort(ascending=0)


# In[24]:

agency2_compl = sizes[1]


# In[25]:

complaints = sizes.sum()
complaints


# In[31]:

resp1 = agency2_compl/float(complaints)
print 'The second mos popular agence has a complaint fraction of: %.10f' %resp1


# In[36]:

quest2 = db.groupby('Complaint Type', sort=False).size()


# In[37]:

uncond_prob = quest2/float(complaints)
uncond_prob


# In[126]:

bors = db.Borough[db.Borough!='Unspecified'].unique()
bors


# In[ ]:

uncond_prob = uncond_prob.dropna()


# In[171]:

res = {}
dat = {}
for b in bors:
    tmp_db = db[db['Borough'] == b].groupby('Complaint Type', sort=False).size()
    tmp_cond_prob = tmp_db/float(tmp_db.sum())
    tmp_cond_prob = tmp_cond_prob.dropna()
    res[b] = {}
    dat[b] = tmp_cond_prob/uncond_prob
    dat[b] = dat[b].dropna()
    dat[b].sort(ascending=False)
    res[b] = {'Complaint': dat[b].index[0], 'Ratio':dat[b][0]}
res    


# In[172]:

res_db = pd.DataFrame.from_dict(res, orient='index')
res_db.sort('Ratio', ascending=False)


# In[173]:

print 'The most surprising complaint is: %s in %s and ratio is %.10f' %(res_db.Complaint[0],res_db.index[0],res_db.Ratio[0])


# In[176]:

lat = db.Latitude.dropna()
lat


# In[177]:

lat.quantile(.1)


# In[178]:

lat.quantile(.9)


# In[179]:

print 'The distance in degrees between the 90th and 10th percentiles in latitude is: %.10f', lat.quantile(.9)-lat.quantile(.1)


# In[180]:

mean_lat = lat.mean()
mean_lat


# In[181]:

lon = db.Longitude.dropna()
lon


# In[182]:

mean_lon = lon.mean()
mean_lon


# In[183]:

sd_lat = lat.std()
sd_lon = lon.std()
print sd_lat, sd_lon


# In[184]:

from globalmaptiles import GlobalMercator


# In[185]:

merc = GlobalMercator()


# In[186]:

meanX, meanY = merc.LatLonToMeters(mean_lat,mean_lon)
print meanX, meanY


# In[187]:

lat_sdMet = merc.LatLonToMeters(mean_lat+sd_lat,mean_lon)
lon_sdMet = merc.LatLonToMeters(mean_lat,mean_lon+sd_lon)
print lat_sdMet, lon_sdMet


# In[188]:

import scipy.spatial as sp


# In[191]:

lat_dist = sp.distance.euclidean([meanX,meanY],lat_sdMet)/1000.0
lat_dist


# In[192]:

lon_dist = sp.distance.euclidean([meanX,meanY],lon_sdMet)/1000.0
lon_dist


# In[193]:

area = (lat_dist/2.0)*(lon_dist/2)*np.pi
print 'Area of single standard deviation ellipse is: %.10f', area


# In[ ]:



