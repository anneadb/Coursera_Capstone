# Data

For this analysis I will be using foursquare data to analyze different neighborhoods in two major German cities: Hamburg and Berlin.

One concern is that data for Germany may not be as extensive as it would be for the U.S. and the analysis may therefore not be as comprehensive.

I will be looking mainly at venue data which will enable me to identify neighborhoods that share certain traits such as having many cafés or restaurants.

Because the official neighborhoods in Hamburg are sized very differently (e.g. there are seven boroughs that range from 50 km^2 to 155 km^2 which are in turn split into localities of different sizes) I decided to use a regularly spaced grid of locations, centered around each city center, to define the neighborhoods.

The foollowing data sources will be needed to extract/generate the required information:

* Geopy Nominatim will be used to obtain the city centers, using the Außenalster for Hamburg and the Brandenburg Gate for Berlin.

* The neighborhoods will be generated algorithmically and approximate addresses of centers of those areas will be obtained using geopy Nominatim reverse geocoding.

* The number of venues and their category in every neighborhood will be obtained using the Foursquare API.
