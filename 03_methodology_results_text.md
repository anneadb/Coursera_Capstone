## Methodology

### Generate neighborhood dataset

To generate the dataset of the neighborhood locations, the city centers of Hamburg and Berlin were used as starting points. For Hamburg the Außenalster and for Berlin the Brandenburg Gate was used as the center address. From these addresses the geocoordinates were derived using the geocode function from Nominatum.

These latitude and longitude coordinates needed to be transformed into UTM coordinates to enable defining a radius around the city center and a smaller radius for each neighborhood. For the cities this was set to 5 km and for the neighborhoods to 1.5 km. Looping over this radius in a hexagonal grid generated UTM coordinates for each neighborhood. These were transformed back into geocoordinates resulting in a list of 39 neighborhoods for each city.

To check whether the neighborhoods were generated correctly, folium was used to map their locations.

![Map of Hamburg neighborhoods (unclustered)](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_unclustered.png)

The Foursquare Places API uses addresses as search entries. Therefore, the reverse function from Nominatim was used to generate neighborhood addresses from the latitude and longitute values. In addition, from the resulting addresses the borough names could be extracted. For Berlin this resulted in 14 boroughs vs. 13 boroughs in Hamburg. 

Cleaned up, the dataset includes the neighborhood address, latitude, longitude, borough and city.

![Table with neighborhood data](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_neighborhoods.png)

### Get venue data from Foursquare

The Foursquare Places API provides venue recommendations using "explore". It was used to request the 100 most popular venues within 1.5 km of each neighborhood center. Along with the venue name, Foursquare proviced many additional details on the venue such as the category (e.g. bakery or theater).

Those neighborhoods for which less than 100 venues were found were exluded from the dataset.

For each remaining neighborhood and borough the top 10 venue categories were identified. This was done using one hot encoding and then calculating the mean per category.

![Table with Top 10 venue categories](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_top10_categories.png)

For the following analysis the resulting tables were simplified and geocoordinates generated for each borough.

### Cluster neighborhoods and boroughs

The neighborhoods and boroughs were clustered using the Kmeans algorithm from sklearn. Kmeans groups each observation (in this case each neighborhood or borough) into clusters minimizing the within-cluster variance. Important to note is that it converges to a local optimum, so each computation may lead to different results.

A high number of clusters were specified (15 for the neighborhoods and 5 for the boroughs) with the aim of getting very specific clusters with an average of 4 neighborhoods or boroughs.

The results for the neighborhood clustering will be dicussed in more detail in the next section. The clustering of the boroughs, however, led to inconclusive results because they appear to be too large to be distinct from one another or base a recommendation on.

![Map of Hamburg borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_b.png)

![Map of Berlin borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_b.png)

## Results

The neighborhoods in Berlin and Hamburg are very different from one another. Out of 14 clusters only two include neighborhoods in both cities. All others are limited to one city.

In Hamburg a strong regional effect is visible. For each cluster the neighborhoods are located adjacent to one another.

![Map of Hamburg neighborhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_n.png)

In Berlin this is also the case but the grouping is not as strong. For example, cluster 2 is made up of several neighborhoods that are farther away from the city center but in different directions.

![Map of Berlin neighborhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_n.png)

Therefore, for the original question of where to move to in the new city based on your former neighborhood only two clusters are suitable for analysis.

Cluster 2:

The most common venues categories in cluster 2 are Café, Bakery, Coffee Shop, Italian Restaurant and Bar. In Berlin this includes neighborhoods in Schöneberg, Friedrichshain and Prenzlauer Berg. In Hamburg this includes neighborhoods in Altona-Nord and Eimsbüttel.

Cluster 3:

The most common venues categories in cluster 3 are Hotel, Coffee Shop, Theater, Café and French Restaurant. In Berlin this includes a neighborhood in Schöneberg. In Hamburg this includes neighborhoods in Hamburg-Mitte, Altstadt, Hammerbrook, Neustadt, St. Georg and Hohenfelde.
