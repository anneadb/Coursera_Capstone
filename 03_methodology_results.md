## Methodology

### Generate neighbourhood dataset 

* get geo coordinates for the centers of berlin and hamburg
	* Addresses -> Nominatim
* generate neighbourhood centers
	* transform latitude and longitute of city centers into UTM coordinates
	* 5km radius around city centers
	* each neighbourhood has a radius of 1.5km
	* loop generates UTM coordinates for neighbourhood centers in a hexagonal grid
	* these are transformed back into latitude and longitude
	* results in 39 neighbourhoods in each city

-> map locations to check accuracy

![Map of Hamburg neighbourhoods (unclustered)](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_unclustered.png)

* get neighbourhood addresses
	* nominatim geolocator reverse
	* extract borough name from address
	* berlin has 14 boroughs and hamburg 13

-> Dataset with address, latitude, longitude, borough and city

![Table with neighbourhood data](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_neighbourhoods.png)

### Get venue data from Foursquare

* Foursquare Places API allows me to get venue recommendation using "explore"
	* get 100 most popular venues within 1.5km of neighbourhood center
	* Foursquare also gives information on the category of each venue, e.g. Café or Italian restaurant.
* Exlude neighbourhoods with less than 100 venues
* Identify top 10 venue categories for each neighbourhood and borough
	* one hot encoding, calculate mean per category, sort by value
* Get borough geocordinates and simplify tables for further analysis

![Table with Top 10 venue categories](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_top10_categories.png)

### Cluster neighbourhoods and boroughs

* For clustering I used the Kmeans algorithm from sklearn
* I specified a high number of clusters (15 for the neighbourhoods and 5 for the boroughs) because I wanted very specific clusters with an average of 4 neighbourhoods or boroughs.
* Further analysis is limited to the neighbourhoods because the boroughs are too large to be distinct from one another.

![Map of Hamburg borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_b.png)

![Map of Berlin borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_b.png)

## Results

* The neighbourhoods in Berlin and Hamburg are very different from one another. Out of 14 clusters only two include neighbourhoods in both cities. All others are limited to one city.
* In Hamburg you can see a strong regional effect. The neighbourhoods in each cluster are all next to one another.

![Map of Hamburg neighbourhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_n.png)

* In Berlin this is also the case but not as strongly, e.g. cluster two is made up of several neighbourhoods that are farther away from the city center but in different directions.

![Map of Berlin neighbourhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_n.png)

* For the original question of where to move in the new city based on your former neighbourhood I can therefore only look at two clusters.
* Cluster 2:
	* the most common venues categories in cluster 2 are Café, Bakery, Coffee Shop, Italian Restaurant and Bar.
	* In Berlin this includes neighbourhoods in Schöneberg, Friedrichshain and Prenzlauer Berg.
	* In Hamburg this includes neighbourhoods in Altona-Nord and Eimsbüttel.
* Cluster 3:
	* the most common venues categories in cluster 3 are Hotel, Coffee Shop, Theater, Café and French Restaurant
	* In Berlin this includes a neighbourhood in Schöneberg.
	* In Hamburg this includes neighbourhoods in Hamburg-Mitte, Altstadt, Hammerbrook, Neustadt, St. Georg and Hohenfelde.
