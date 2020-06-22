#!/usr/bin/env python
# coding: utf-8

# # Analyzing the similarity of major German Cities

# ## Setup

# In[1]:


#pip install geopy
#pip install folium
#pip install shapely
#pip install pyproj


# In[2]:


import numpy as np
import pandas as pd

from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import folium # map rendering library

import re # for regular expressions

# for transforming geocoordinates
import shapely.geometry
import pyproj
import math

import requests # library to handle requests

from sklearn.cluster import KMeans # for clustering

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

from collections import Counter # to count repeated items in list

import warnings
warnings.simplefilter('ignore')

print('Libraries imported.')


# ### Generate neighborhoods

# In[3]:


address = 'Brandenburg Gate, Berlin, Germany'

geolocator = Nominatim(user_agent="hamburg_explorer")
location = geolocator.geocode(address)
berlin_lat = location.latitude
berlin_lon = location.longitude
print('The geograpical coordinates of Berlin are {}, {}.'.format(berlin_lat, berlin_lon))


# In[4]:


address = 'Außenalster, Hamburg, Germany'

geolocator = Nominatim(user_agent="hamburg_explorer")
location = geolocator.geocode(address)
hamburg_lat = location.latitude
hamburg_lon = location.longitude
print('The geograpical coordinates of Hamburg are {}, {}.'.format(hamburg_lat, hamburg_lon))


# In[5]:


def lonlat_to_xy(lon, lat):
    proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
    proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
    xy = pyproj.transform(proj_latlon, proj_xy, lon, lat)
    return xy[0], xy[1]

def xy_to_lonlat(x, y):
    proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
    proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
    lonlat = pyproj.transform(proj_xy, proj_latlon, x, y)
    return lonlat[0], lonlat[1]

def calc_xy_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)

print('Coordinate transformation check')
print('-------------------------------')
print('Hamburg center longitude={}, latitude={}'.format(hamburg_lon, hamburg_lat))
x, y = lonlat_to_xy(hamburg_lon, hamburg_lat)
print('Hamburg center UTM X={}, Y={}'.format(x, y))
lo, la = xy_to_lonlat(x, y)
print('Hamburg center longitude={}, latitude={}'.format(lo, la))


# In[6]:


berlin_center_x, berlin_center_y = lonlat_to_xy(berlin_lon, berlin_lat) # City center in Cartesian coordinates
hamburg_center_x, hamburg_center_y = lonlat_to_xy(hamburg_lon, hamburg_lat)

k = math.sqrt(3) / 2 # Vertical offset for hexagonal grid cells
square_width = 10000
neigborhood_radius = 1500
x_step = neigborhood_radius
y_step = neigborhood_radius * k

x_min = berlin_center_x - square_width/2
y_min = berlin_center_y - square_width/2 - (int(21/k)*k*neigborhood_radius - square_width)/2
berlin_latitudes = []
berlin_longitudes = []
berlin_distances_from_center = []
xs = []
ys = []
for i in range(0, int(21/k)):
    y = y_min + i * y_step
    x_offset = neigborhood_radius/2 if i%2==0 else 0
    for j in range(0, 21):
        x = x_min + j * x_step + x_offset
        berlin_distance_from_center = calc_xy_distance(berlin_center_x, berlin_center_y, x, y)
        if (berlin_distance_from_center <= square_width/2+1):
            lon, lat = xy_to_lonlat(x, y)
            berlin_latitudes.append(lat)
            berlin_longitudes.append(lon)
            berlin_distances_from_center.append(berlin_distance_from_center)
            xs.append(x)
            ys.append(y)
            
x_min = hamburg_center_x - square_width/2
y_min = hamburg_center_y - square_width/2 - (int(21/k)*k*neigborhood_radius - square_width)/2
hamburg_latitudes = []
hamburg_longitudes = []
hamburg_distances_from_center = []
xs = []
ys = []
for i in range(0, int(21/k)):
    y = y_min + i * y_step
    x_offset = neigborhood_radius/2 if i%2==0 else 0
    for j in range(0, 21):
        x = x_min + j * x_step + x_offset
        hamburg_distance_from_center = calc_xy_distance(hamburg_center_x, hamburg_center_y, x, y)
        if (hamburg_distance_from_center <= square_width/2+1):
            lon, lat = xy_to_lonlat(x, y)
            hamburg_latitudes.append(lat)
            hamburg_longitudes.append(lon)
            hamburg_distances_from_center.append(hamburg_distance_from_center)
            xs.append(x)
            ys.append(y)

print(len(berlin_latitudes), 'Berlin neighborhood centers generated.')
print(len(hamburg_latitudes), 'Hamburg neighborhood centers generated.')


# In[7]:


map_berlin = folium.Map(location=[berlin_lat, berlin_lon], zoom_start=12)

# add markers to map
for lat, lng in zip(berlin_latitudes, berlin_longitudes):
    label = '{}, {}'.format(lat, lng)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=neigborhood_radius/40,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.5,
        parse_html=False).add_to(map_berlin)  
    
map_berlin


# In[8]:


map_hamburg = folium.Map(location=[hamburg_lat, hamburg_lon], zoom_start=12)

# add markers to map
for lat, lng in zip(hamburg_latitudes, hamburg_longitudes):
    label = '{}, {}'.format(lat, lng)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=neigborhood_radius/40,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.5,
        parse_html=False).add_to(map_hamburg)  
    
map_hamburg


# In[9]:


hamburg_neighborhoods = []

for i in range(0,len(hamburg_latitudes)):
    reverse = geolocator.reverse((hamburg_latitudes[i],hamburg_longitudes[i]))
    address = reverse[0] 
    address_n = re.findall(".*, (.*),.*,.*,.*", address)[0]
    geo_lat = reverse[1][0]
    geo_lon = reverse[1][1]
    city = "Hamburg"
    hamburg_neighborhoods.append([address, geo_lat, geo_lon, address_n, city])

hamburg_neighborhoods = pd.DataFrame(hamburg_neighborhoods)
hamburg_neighborhoods.rename(columns={0:"Neighborhood",1:"Latitude",2:"Longitude",3:"Borough",4:"City"}, inplace=True)


# In[10]:


berlin_neighborhoods = []

for i in range(0,len(berlin_latitudes)):
    reverse = geolocator.reverse((berlin_latitudes[i],berlin_longitudes[i]))
    address = reverse[0] 
    try:
        address_n = re.findall(".*, (.*),.*,.*,.*", address)[0]
    except:
        address_n = re.findall("(.*),.*,.*,.*", address)[0]
    
    geo_lat = reverse[1][0]
    geo_lon = reverse[1][1]
    city = "Berlin"
    berlin_neighborhoods.append([address, geo_lat, geo_lon, address_n, city])

berlin_neighborhoods = pd.DataFrame(berlin_neighborhoods)
berlin_neighborhoods.rename(columns={0:"Neighborhood",1:"Latitude",2:"Longitude",3:"Borough",4:"City"}, inplace=True)


# In[11]:


hamburg_neighborhoods.head()


# In[12]:


berlin_neighborhoods.head()


# In[13]:


neighborhoods = pd.concat([hamburg_neighborhoods, berlin_neighborhoods])


# In[14]:


hamburg_neighborhoods.to_csv("Data/hamburg_neighborhoods.csv", index=False)
berlin_neighborhoods.to_csv("Data/berlin_neighborhoods.csv", index=False)
neighborhoods.to_csv("Data/neighborhoods.csv", index=False)


# ### Get venue data

# In[15]:


hamburg_neighborhoods = pd.read_csv("Data/hamburg_neighborhoods.csv")
hamburg_neighborhoods.head()


# In[16]:


berlin_neighborhoods = pd.read_csv("Data/berlin_neighborhoods.csv")
berlin_neighborhoods.head()


# In[17]:


print("There are", berlin_neighborhoods.shape[0], "neighborhoods in Berlin and",
      hamburg_neighborhoods.shape[0], "in Hamburg.")
print("They belong to",
      berlin_neighborhoods.Borough.unique().shape[0],
      "and",
      hamburg_neighborhoods.Borough.unique().shape[0],
      "boroughs respectively."
     )


# In[18]:


limit = 100
radius = 1500 # see neighbourhood radius above

VERSION = '20180605' # Foursquare API version


# In[19]:


get_ipython().run_line_magic('run', 'credentials.py # client_id and client_secret for Foursquare')


# In[44]:


def getNearbyVenues(neighborhoods, latitudes, longitudes, boroughs, cities):
    
    venues_list=[]
    for neigh, lat, lng, bor, city in zip(neighborhoods, latitudes, longitudes, boroughs, cities):
        #print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            limit)
            
        # make the GET request
        try:
            results = requests.get(url).json()["response"]['groups'][0]['items']
        except:
            results = []
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            neigh,
            lat,
            lng,
            bor,
            city,
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Address Latitude', 
                  'Address Longitude',
                  'Borough',
                  'City',
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# In[45]:


hamburg_venues = getNearbyVenues(
    neighborhoods = hamburg_neighborhoods['Neighborhood'],
    latitudes = hamburg_neighborhoods['Latitude'],
    longitudes = hamburg_neighborhoods['Longitude'],
    boroughs = hamburg_neighborhoods['Borough'],
    cities = hamburg_neighborhoods['City']
)


# In[46]:


berlin_venues = getNearbyVenues(
    neighborhoods = berlin_neighborhoods['Neighborhood'],
    latitudes = berlin_neighborhoods['Latitude'],
    longitudes = berlin_neighborhoods['Longitude'],
    boroughs = berlin_neighborhoods['Borough'],
    cities = berlin_neighborhoods['City']
)


# In[47]:


all_venues = pd.concat([berlin_venues, hamburg_venues], ignore_index=True)


# In[48]:


all_venues.shape


# In[49]:


# exclude neighborhoods that are too small or too big
a_count = all_venues.groupby("Neighborhood").count()
a_incl = a_count[a_count["Venue"] >= 100].reset_index().Neighborhood
all_venues = all_venues[all_venues.Neighborhood.isin(a_incl)]

all_venues.shape


# In[50]:


all_venues.head()


# In[51]:


all_venues.to_csv("Data/all_venues.csv", index=False)


# ### Find Top 10 venue types for each neighborhood and borough

# In[52]:


all_venues = pd.read_csv("Data/all_venues.csv")
all_venues.head()


# In[53]:


venue_cat_onehot = pd.get_dummies(all_venues[['Venue Category']], prefix="", prefix_sep="")
venue_cat_onehot['Neighborhood'] = all_venues['Neighborhood'] 
venue_cat_onehot['Borough'] = all_venues['Borough'] 


# In[54]:


boroughs_grouped = venue_cat_onehot.groupby('Borough').mean().reset_index()
boroughs_grouped.head()


# In[55]:


neighborhoods_grouped = venue_cat_onehot.groupby('Neighborhood').mean().reset_index()
neighborhoods_grouped.head()


# In[56]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# In[57]:


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted['Neighborhood'] = neighborhoods_grouped['Neighborhood']

for ind in np.arange(neighborhoods_grouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(neighborhoods_grouped.iloc[ind, :], num_top_venues)

neighborhoods_venues_sorted.head()


# In[58]:


columns = ['Borough']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
boroughs_venues_sorted = pd.DataFrame(columns=columns)
boroughs_venues_sorted['Borough'] = boroughs_grouped['Borough']

for ind in np.arange(boroughs_grouped.shape[0]):
    boroughs_venues_sorted.iloc[ind, 1:] = return_most_common_venues(boroughs_grouped.iloc[ind, :], num_top_venues)

boroughs_venues_sorted.head()


# In[59]:


boroughs = all_venues[["Borough","City"]]
boroughs.drop_duplicates(inplace=True)
boroughs.index = range(0,len(boroughs))
boroughs.head()


# In[60]:


boroughs_loc = []
geolocator = Nominatim(user_agent="hamburg_explorer")

for i in range(0,len(boroughs)):
    borough = boroughs["Borough"][i]
    city = boroughs["City"][i]
    address = '{}, {}'.format(borough, city)
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    boroughs_loc.append([borough, city, lat, lon])

boroughs_loc = pd.DataFrame(boroughs_loc)
boroughs_loc.rename(columns={0:"Borough",1:"City",2:"Latitude",3:"Longitude"}, inplace=True)
boroughs_loc.head()


# In[61]:


venues_loc = all_venues[["Neighborhood","Address Latitude","Address Longitude","Borough","City"]]
venues_loc = venues_loc.drop_duplicates()
venues_loc.index = range(0, venues_loc.shape[0])


# In[62]:


neighborhoods_grouped.to_csv("Data/neighborhoods_grouped.csv", index=False)
boroughs_grouped.to_csv("Data/boroughs_grouped.csv", index=False)
neighborhoods_venues_sorted.to_csv("Data/neighborhoods_venues_sorted.csv", index=False)
boroughs_venues_sorted.to_csv("Data/boroughs_venues_sorted.csv", index=False)
boroughs_loc.to_csv("Data/boroughs_loc.csv", index=False)
venues_loc.to_csv("Data/venues_loc.csv", index=False)


# ### Cluster neighborhoods and boroughs

# I want to have realtively small clusters with an average of 4 neighborhoods or boroughs.

# In[63]:


neighborhoods_grouped = pd.read_csv("Data/neighborhoods_grouped.csv")
boroughs_grouped = pd.read_csv("Data/boroughs_grouped.csv")
neighborhoods_venues_sorted = pd.read_csv("Data/neighborhoods_venues_sorted.csv")
boroughs_venues_sorted = pd.read_csv("Data/boroughs_venues_sorted.csv")
all_venues = pd.read_csv("Data/all_venues.csv")
boroughs_loc = pd.read_csv("Data/boroughs_loc.csv")
venues_loc = pd.read_csv("Data/venues_loc.csv")


# In[64]:


kclusters_n = round(neighborhoods_grouped.shape[0]/4)
kclusters_b = round(boroughs_grouped.shape[0]/4)

neighborhood_clustering = neighborhoods_grouped.drop('Neighborhood', 1)
borough_clustering = boroughs_grouped.drop('Borough', 1)


# In[65]:


kmeans_n = KMeans(n_clusters=kclusters_n, random_state=0).fit(neighborhood_clustering)
kmeans_b = KMeans(n_clusters=kclusters_b, random_state=0).fit(borough_clustering)


# In[66]:


#neighborhoods_venues_sorted.drop("Cluster Labels",1, inplace=True)
#boroughs_venues_sorted.drop("Cluster Labels",1, inplace=True)

neighborhoods_venues_sorted.insert(0, 'Cluster Labels', kmeans_n.labels_)
boroughs_venues_sorted.insert(0, 'Cluster Labels', kmeans_b.labels_)


# In[67]:


neighborhoods_merged = venues_loc
neighborhoods_merged = neighborhoods_merged.merge(neighborhoods_venues_sorted.set_index('Neighborhood'), left_on='Neighborhood', right_on="Neighborhood")
neighborhoods_merged.head()


# In[68]:


boroughs_merged = boroughs_loc
boroughs_merged = boroughs_merged.merge(boroughs_venues_sorted.set_index('Borough'), left_on='Borough', right_on="Borough")
boroughs_merged.head()


# In[69]:


neighborhoods_merged.to_csv("Data/neighborhoods_merged.csv", index=False)
boroughs_merged.to_csv("Data/boroughs_merged.csv", index=False)


# ### Map neighborhood clusters

# In[70]:


# set color scheme for the clusters
x = np.arange(kclusters_n)
ys = [i + x + (i*x)**2 for i in range(kclusters_n)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# create map
map_clusters = folium.Map(location=[hamburg_lat, hamburg_lon], zoom_start=12)

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(neighborhoods_merged['Address Latitude'],
                                  neighborhoods_merged['Address Longitude'],
                                  neighborhoods_merged['Neighborhood'],
                                  neighborhoods_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=35, # neighborhood_radius/40
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.5,
        parse_html=False
    ).add_to(map_clusters)
       
map_clusters


# In[71]:


map_clusters


# ### Map borough clusters

# In[72]:


# set color scheme for the clusters
x = np.arange(kclusters_b)
ys = [i + x + (i*x)**2 for i in range(kclusters_b)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# create map
map_clusters_b = folium.Map(location=[hamburg_lat, hamburg_lon], zoom_start=12)

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(boroughs_merged['Latitude'],
                                  boroughs_merged['Longitude'],
                                  boroughs_merged['Borough'],
                                  boroughs_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=35, # neighborhood_radius/40
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.5,
        parse_html=False
    ).add_to(map_clusters_b)
       
map_clusters_b


# In[73]:


map_clusters_b


# ### Explore neighborhood clusters

# The boroughs are clearly too large to be in any way distinct. I will therefore continue exploring the neighborhoods.

# In[74]:


cluster_neigh_num = []
for i in range(0,kclusters_n):
    city_group = neighborhoods_merged[neighborhoods_merged["Cluster Labels"] == i].groupby("City").count()["Neighborhood"]
    city_group = pd.DataFrame(city_group).reset_index()
    
    try:
        hamburg = city_group[city_group.City == "Hamburg"]["Neighborhood"][1]
    except:
        try: 
            hamburg = city_group[city_group.City == "Hamburg"]["Neighborhood"][0]
        except:
            hamburg = 0
    
    try:
        berlin = city_group[city_group.City == "Berlin"]["Neighborhood"][0]
    except:
        berlin = 0
    
    cluster_neigh_num.append({"Cluster Labels": i, "Hamburg": hamburg, "Berlin": berlin})
    print("Cluster", i, "has", hamburg, "Hamburg neighborhoods and", berlin, "Berlin neighborhoods.")
    
cluster_neigh_num = pd.DataFrame(cluster_neigh_num)


# I'm only interested in those clusters that have both Hamburg and Berlin neighbordhoods.

# In[75]:


cluster_neigh_num[(cluster_neigh_num.Hamburg > 0) & (cluster_neigh_num.Berlin > 0)]


# In[76]:


cluster_list = cluster_neigh_num[(cluster_neigh_num.Hamburg > 0) & (cluster_neigh_num.Berlin > 0)]["Cluster Labels"].tolist()

venues_list = [[]]*len(cluster_list)

for i in range(0,len(cluster_list)):
    j = cluster_list[i]
    venues = neighborhoods_merged[neighborhoods_merged["Cluster Labels"] == j].iloc[:, 6:16].values.tolist()
    venues_list[i] = []
    for sublist in venues:
        for item in sublist:
            venues_list[i].append(item)


# In[77]:


for i in range(0,len(cluster_list)):
    venues_count = Counter(venues_list[i])
    venues_count = pd.DataFrame.from_dict(venues_count, orient='index').reset_index()
    j = cluster_list[i]
    print("Top 5 venues types in Cluster", j)
    display(venues_count.sort_values(0, ascending=False).head())
    display(neighborhoods_merged[neighborhoods_merged["Cluster Labels"] == j].Neighborhood.values.tolist())
    print("\n")

