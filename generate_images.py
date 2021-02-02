import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
from shapely.geometry import Point
from matplotlib import colors

gdf_data = gpd.read_file('sdcounty') #COVID data, ZIP codes as points
gdf_zip = gpd.read_file('zipcodes')  #ZIP codes as polygons

#fill null values with 0
gdf_data['case_count'] = gdf_data['case_count'].fillna(value=0)

#match CRS
gdf_data = gdf_data.to_crs(gdf_zip.crs)

output_path = 'timeseries/maps'

#create dataframe of dates
dates = gdf_data['updatedate'].drop_duplicates().reset_index()
dates = dates.loc[7:] #cut off first 6 dates because they're weird for some reason

#set min and max range for choropleth map
vmin,vmax = 0,int(gdf_data['case_count'].max())

#test_dates = ['2021-01-15','2021-01-30']

for date in dates['updatedate']:
    
    mask = gdf_data[gdf_data['updatedate'] == date]
    mask = gpd.sjoin(mask, gdf_zip, how='right', op='within')
    
    plt.style.use('dark_background')

    #create map
    fig = mask.plot(column='case_count', cmap = 'plasma', figsize = (9,6), 
            edgecolor='silver', lw=0.2, legend = True, vmin=vmin, vmax=vmax,
            norm=plt.Normalize(vmin=vmin, vmax=vmax, clip=True))
    fig.axis('off')

    # position the annotation to the bottom right
    fig.annotate(date,
            xy=(0.5, .130), xycoords='figure fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=28)
    fig.annotate('Total COVID cases by ZIP code',xy=(0.5,0.9), xycoords='figure fraction', fontsize=25,horizontalalignment='center')


    filepath = os.path.join(output_path, date+'_covid.jpg')
    chart = fig.get_figure()
    chart.savefig(filepath, dpi=300)
    print(date)