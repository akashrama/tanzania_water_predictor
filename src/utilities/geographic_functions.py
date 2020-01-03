import pandas as pd 
import numpy as np 
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import descartes
import rasterio
import rasterio.plot
import matplotlib.colors as colors

def map_pumps(df_train):
    """
    This function maps the pumps, with their status, across Tanzania.
    You must install/import the following libraries:
    
        import geopandas as gpd
        from shapely.geometry import Point, Polygon
        import matplotlib.pyplot as plt
        import descartes
    """
                  
    #import a Tanzania shape files
    tanz_base = gpd.read_file('../../../data/raw/geographic/tza_admbnda_adm0_20181019.shp')
    regions = gpd.read_file('../../../data/raw/geographic/tza_admbnda_adm1_20181019.shp')
    ward = gpd.read_file('../../../data/raw/geographic/tza_admbnda_adm2_20181019.shp')
    county = gpd.read_file('../../../data/raw/geographic/tza_admbnda_adm3_20181019.shp')

    #set the WGS84 projection
    crs = {'init':'espg:4326'}

    #create geometric points for projecting
    geometry = [Point(xy) for xy in zip( df_train['longitude'], df_train['latitude'])]
    geo_df_train = gpd.GeoDataFrame(df_train, crs = crs, geometry = geometry)
    df_train = df_train.drop('geometry', axis=1)

    #remove geographic outliers/NaNs for visualization clarity 
    #(there were ~1800 points with longitude = 0 (Earlier test-mapping showed this))
    geo_df_train = geo_df_train[geo_df_train.longitude != 0]

    #plot the points over the Tanz base map
    fig,ax = plt.subplots(figsize = (25,25))
    # tanz_base.plot(ax = ax, alpha = .4, color = 'grey')
    ward.plot(ax=ax, color = 'grey', alpha = .2, linewidth=1, edgecolor = 'black')
    geo_df_train[geo_df_train['status_group']=='functional'].plot(ax = ax, markersize = 10, 
                                                                  color = 'blue', alpha = .1, marker = 'o', 
                                                                  label = 'functional')
    geo_df_train[geo_df_train['status_group']=='non functional'].plot(ax = ax, markersize = 10, 
                                                                      color = 'red', alpha = .1, marker = 'o', 
                                                                      label = 'non functional')
    geo_df_train[geo_df_train['status_group']=='functional needs repair'].plot(ax = ax, markersize = 10,
                                                                               color = 'yellow', alpha = .5, marker = 'o', 
                                                                        label = 'functional needs repair')
    plt.title('Water Pumps Across Tanzania',fontdict=
                              {'fontsize': 25})
                            
    plt.legend(prop = {'size':25}, markerscale=5)
    plt.savefig("../../../reports/figures/pump_geo_distribution.png", dpi=300)
    plt.show()



def pop_den_raster():
    """
    This function maps the Tanzania Populatin Density, people per 100m, across Tanzania.
    You must install/import the following libraries:
    
    import rasterio
    import rasterio.plot
    import matplotlib.colors as colors
    """

    # countries = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    raster = rasterio.open('../../../data/raw/geographic/TZA_popmap15adj_v2b.tif')

    fig, ax = plt.subplots(figsize=(15, 15))
    rasterio.plot.show(raster, title='Tanzania Population Density \n 100m Resolution', ax=ax, cmap='Blues', norm = colors.LogNorm(vmin=.01, vmax=393))
    plt.savefig("../../../reports/figures/pop_den_map.png", dpi=300)

    plt.show()
    