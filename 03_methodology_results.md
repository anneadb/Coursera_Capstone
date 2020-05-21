## Methodology

### Generate neighborhood dataset 

* get geo coordinates for the centers of berlin and hamburg
	* Addresses -> Nominatim
* generate neighborhood centers
	* transform latitude and longitute of city centers into UTM coordinates
	* 5km radius around city centers
	* each neighborhood has a radius of 1.5km
	* loop generates UTM coordinates for neighborhood centers in a hexagonal grid
	* these are transformed back into latitude and longitude
	* results in 39 neighborhoods in each city

-> map locations to check accuracy

![Map of Hamburg neighborhoods (unclustered)](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_unclustered.png)

* get neighborhood addresses
	* nominatim geolocator reverse
	* extract borough name from address
	* berlin has 14 boroughs and hamburg 13

-> Dataset with address, latitude, longitude, borough and city

![Table with neighborhood data](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_neighborhoods.png)

### Get venue data from Foursquare

* Foursquare Places API allows me to get venue recommendation using "explore"
	* get 100 most popular venues within 1.5km of neighborhood center
	* Foursquare also gives information on the category of each venue, e.g. Café or Italian restaurant.
* Exlude neighborhoods with less than 100 venues
* Identify top 10 venue categories for each neighborhood and borough
	* one hot encoding, calculate mean per category, sort by value
* Get borough geocordinates and simplify tables for further analysis

![Table with Top 10 venue categories](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/table_top10_categories.png)

### Cluster neighborhoods and boroughs

* For clustering I used the Kmeans algorithm from sklearn
* I specified a high number of clusters (15 for the neighborhoods and 5 for the boroughs) because I wanted very specific clusters with an average of 4 neighborhoods or boroughs.
* Further analysis is limited to the neighborhoods because the boroughs are too large to be distinct from one another.

![Map of Hamburg borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_b.png)

![Map of Berlin borough clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_b.png)

## Results

* The neighborhoods in Berlin and Hamburg are very different from one another. Out of 14 clusters only two include neighborhoods in both cities. All others are limited to one city.
* In Hamburg you can see a strong regional effect. The neighborhoods in each cluster are all next to one another.

![Map of Hamburg neighborhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_hamburg_clustered_n.png)

* In Berlin this is also the case but not as strongly, e.g. cluster two is made up of several neighborhoods that are farther away from the city center but in different directions.

![Map of Berlin neighborhood clusters](https://github.com/anneadb/Coursera_Capstone/blob/master/Screenshots/map_berlin_clustered_n.png)

* For the original question of where to move in the new city based on your former neighborhood I can therefore only look at two clusters.
* Cluster 2:
	* the most common venues categories in cluster 2 are Café, Bakery, Coffee Shop, Italian Restaurant and Bar.
	* In Berlin this includes neighborhoods in Schöneberg, Friedrichshain and Prenzlauer Berg.
	* In Hamburg this includes neighborhoods in Altona-Nord and Eimsbüttel.
* Cluster 3:
	* the most common venues categories in cluster 3 are Hotel, Coffee Shop, Theater, Café and French Restaurant
	* In Berlin this includes a neighborhood in Schöneberg.
	* In Hamburg this includes neighborhoods in Hamburg-Mitte, Altstadt, Hammerbrook, Neustadt, St. Georg and Hohenfelde.
