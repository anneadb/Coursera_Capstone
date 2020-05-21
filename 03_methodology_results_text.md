## Methodology

### Generate neighbourhood dataset

To generate the dataset of the neighbourhood locations, the city centers of Hamburg and Berlin were used as starting points. For Hamburg the Außenalster and for Berlin the Brandenburg Gate was used as the center address. From these addresses the geocoordinates were derived using the geocode function from Nominatum.

These latitude and longitude coordinates needed to be transformed into UTM coordinates to enable defining a radius around the city center and a smaller radius for each neighbourhood. For the cities this was set to 5 km and for the neighbourhoods to 1.5 km. Looping over this radius in a hexagonal grid generated UTM coordinates for each neighbourhood. These were transformed back into geocoordinates resulting in a list of 39 neighbourhoods for each city.

To check whether the neighbourhoods were generated correctly, folium was used to map their locations.

![Map of Hamburg neighbourhoods (unclustered)](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_unclustered.png)

The Foursquare Places API uses addresses as search entries. Therefore, the reverse function from Nominatim was used to generate neighbourhood addresses from the latitude and longitute values. In addition, from the resulting addresses the borough names could be extracted. For Berlin this resulted in 14 boroughs vs. 13 boroughs in Hamburg. 

Cleaned up, the dataset includes the neighbourhood address, latitude, longitude, borough and city.

![Table with neighbourhood data](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_neighbourhoods.png)

### Get venue data from Foursquare

The Foursquare Places API provides venue recommendations using "explore". It was used to request the 100 most popular venues within 1.5 km of each neighbourhood center. Along with the venue name, Foursquare proviced many additional details on the venue such as the category (e.g. bakery or theater).

Those neighbourhoods for which less than 100 venues were found were exluded from the dataset.

For each remaining neighbourhood and borough the top 10 venue categories were identified. This was done using one hot encoding and then calculating the mean per category.

![Table with Top 10 venue categories](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_top10_categories.png)

For the following analysis the resulting tables were simplified and geocoordinates generated for each borough.

### Cluster neighbourhoods and boroughs

The neighbourhoods and boroughs were clustered using the Kmeans algorithm from sklearn. Kmeans groups each observation (in this case each neighbourhood or borough) into clusters minimizing the within-cluster variance. Important to note is that it converges to a local optimum, so each computation may lead to different results.

A high number of clusters were specified (15 for the neighbourhoods and 5 for the boroughs) with the aim of getting very specific clusters with an average of 4 neighbourhoods or boroughs.

The results for the neighbourhood clustering will be dicussed in more detail in the next section. The clustering of the boroughs, however, led to inconclusive results because they appear to be too large to be distinct from one another or base a recommendation on.

![Map of Hamburg borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_b.png)

![Map of Berlin borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_b.png)

## Results

The neighbourhoods in Berlin and Hamburg are very different from one another. Out of 14 clusters only two include neighbourhoods in both cities. All others are limited to one city.

In Hamburg a strong regional effect is visible. For each cluster the neighbourhoods are located adjacent to one another.

![Map of Hamburg neighbourhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_n.png)

In Berlin this is also the case but the grouping is not as strong. For example, cluster 2 is made up of several neighbourhoods that are farther away from the city center but in different directions.

![Map of Berlin neighbourhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_n.png)

Therefore, for the original question of where to move to in the new city based on your former neighbourhood only two clusters are suitable for analysis.

Cluster 2:

The most common venues categories in cluster 2 are Café, Bakery, Coffee Shop, Italian Restaurant and Bar. In Berlin this includes neighbourhoods in Schöneberg, Friedrichshain and Prenzlauer Berg. In Hamburg this includes neighbourhoods in Altona-Nord and Eimsbüttel.

Cluster 3:

The most common venues categories in cluster 3 are Hotel, Coffee Shop, Theater, Café and French Restaurant. In Berlin this includes a neighbourhood in Schöneberg. In Hamburg this includes neighbourhoods in Hamburg-Mitte, Altstadt, Hammerbrook, Neustadt, St. Georg and Hohenfelde.
