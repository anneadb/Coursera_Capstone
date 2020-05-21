## Data

For this analysis I will be using foursquare data to analyze different neighbourhoods in two major German cities: Hamburg and Berlin.

One concern is that data for Germany may not be as extensive as it would be for the U.S. and the analysis may therefore not be as comprehensive.

I will be looking mainly at venue data which will enable me to identify neighbourhoods that share certain traits such as having many cafés or restaurants.

Because the official neighbourhoods in Hamburg are sized very differently (e.g. there are seven boroughs that range from 50 km^2 to 155 km^2 which are in turn split into localities of different sizes) I decided to use a regularly spaced grid of locations, centred around each city center, to define the neighbourhoods. But I will also look at the boroughs to confirm my assumption that they are not suitable for clustering.

The following data sources will be needed to extract/generate the required information:

* Geopy Nominatim will be used to obtain the city centres, using the Außenalster for Hamburg and the Brandenburg Gate for Berlin.

* The neighbourhoods will be generated algorithmically with a fixed radius. Approximate addresses of the centres of those areas will be obtained using geopy Nominatim reverse geocoding.

* The number of venues and their category in every neighbourhood will be obtained using the Foursquare API.
