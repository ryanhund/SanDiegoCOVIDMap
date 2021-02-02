import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors
from pandas import DataFrame, Series
from shapely.geometry import Point

gdf_data = gpd.read_file('sdcounty') #COVID data, ZIP codes as points
gdf_zip = gpd.read_file('zipcodes')  #ZIP codes as polygons

gdf_data['case_count'] = gdf_data['case_count'].fillna(value=0)

#match CRS
gdf_data = gdf_data.to_crs(gdf_zip.crs)

output_path = 'timeseries/maps'

#create dataframe of dates
dates = gdf_data['updatedate'].drop_duplicates().reset_index()
dates = dates.loc[7:] #cut off first 6 dates because they're weird for some reason

#pull out weeks from days
weeks = dates.loc[7::7,:].reset_index()
prev = gdf_data[gdf_data['updatedate'] == weeks['updatedate'].loc[0]].reset_index()
vmin,vmax = 0,1000

for week in weeks['updatedate']:

    mask = gdf_data[gdf_data['updatedate'] == week]
    mask = gpd.sjoin(mask, gdf_zip, how='right', op='within')

    mask['new_cases'] = mask['case_count'] - prev['case_count']
    prev = gdf_data[gdf_data['updatedate'] == week].reset_index()

    plt.style.use('dark_background')

    #create map
    fig = mask.plot(column='new_cases', cmap = 'plasma', figsize = (9,6), 
            edgecolor='silver', lw=0.2, legend = True, vmin=vmin, vmax=vmax,
            norm=plt.Normalize(vmin=vmin, vmax=vmax, clip=True))
    fig.axis('off')

    # position the annotation to the bottom right
    fig.annotate(week,
            xy=(0.5, .130), xycoords='figure fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=28)
    fig.annotate('Weekly COVID Cases by ZIP Code',xy=(0.5,0.9), xycoords='figure fraction', fontsize=25,horizontalalignment='center')


    filepath = os.path.join(output_path, week+'_covid.jpg')
    chart = fig.get_figure()
    chart.savefig(filepath, dpi=300)
    print(week)

print("Done :>")