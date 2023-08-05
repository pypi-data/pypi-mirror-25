This library is an abstraction layer, with its own classes, to access mapping functions, regardless
of which version of ArcGIS you are using. Think of it as the "six" package, but for arcpy.mapping/arcpy.mp. If you
write your mapping code against this pacakge, it will work no matter which version of ArcGIS your end users are
running. In general, the API adheres closely to the ArcGIS Pro api, since that has a cleaner, object-oriented design,
but it may included differences. Further, methods are lowercased and underscored instead of camelcased, partially to
make it easy to see at a glance that it's not the same code, and partially due to author preference.

Documentation can be found at http://amaptor.readthedocs.io


