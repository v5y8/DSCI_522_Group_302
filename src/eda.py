# author: Carlina Kim
# date: 2020-01-23

"""This script creates exploratory data visualiztions and tables that help readers understand the Hong Kong horse racing data. 

Usage: eda.py <file_path_in> <file_path_out>

Arguments:
<file_path_in>  Name of cleaned .csv files to download that were preprocessed from the wrangle_data_py, must be within the /data directory.
<file_path_out> Name of directory for figures to be saved in, 'img' folder recommended.

"""

import pandas as pd
import altair as alt
import numpy as np
import pandas_profiling as pandas_profiling
import seaborn as sns
from docopt import docopt

opt = docopt(__doc__)

def main(file_path_in, file_path_out):

    # import training dataset for plotting
    
    data_train = pd.read_csv(f"{file_path_in}/data_train.csv", index_col=0)
    
    
    #Checking to see the null values in the data set, to be preprocessed in the analysis
    
    heat_map= sns.set(rc= {'figure.figsize':(10, 9)})
    heat_map = sns.heatmap(data_train.isnull(), cmap='viridis', cbar=False)
    heat_map.figure.savefig(f"{file_path_out}/heatmap_null.png")
    
    
    
    #Create correlation plot to look at features 
    
    vehicles_corr = data_train.corr().reset_index().rename(columns ={'index':'Var1'}).melt(id_vars = ['Var1'],
                                                                                    value_name = 'Correlation',
                                                                                    var_name = 'Var2')
    base = alt.Chart(vehicles_corr).encode(
        alt.Y('Var1:N'), alt.X('Var2:N'))  
    heatmap = base.mark_rect().encode(
        alt.Color('Correlation:Q',
                  scale=alt.Scale(scheme='viridis')))
    text = base.mark_text(baseline='middle').encode(
        text=alt.Text('Correlation:Q', format='.2'),
        color=alt.condition(
        alt.datum.Correlation >= 0.90,
        alt.value('black'),
        alt.value('white')))    
    total_heatmap =(heatmap + text).properties(
        width = 500, height = 500,
        title = "Pearson's correlation")
    total_heatmap.save(f"{file_path_out}/correlation_plot.png")
    
    
    #Distribution of Age of horses
    
    age_dist= alt.Chart(data_train).mark_bar().encode(
        alt.X("age", bin=True),
        y='count()', ).properties(
        title= 'Distribution of Age')
    
    age_dist.save(f"{file_path_out}/age_dist.png")

    
    # Country where hroses are from distribution plot
    
    #remove null values
    data_train = data_train[~data_train['country'].isnull()]

    country_dist= alt.Chart(data_train).mark_boxplot().encode(
        x=alt.X('country:N', title = "Country"),
        y=alt.Y('plc:Q', title = "Placement")
        ).properties(height=300, width= 500, 
                     title="Distribution of numerical placement values of horses by Country"
                    ).configure_axis(titleFontSize=15, labelFontSize=15
                    ).configure_title(fontSize=16)
    
    country_dist.save(f"{file_path_out}/country_dist.png")

    
    #Horse Weight Distribution plot
    
    weight_dist = alt.Chart(data_train).mark_boxplot().encode(
        x=alt.X('declarwt:Q', scale=alt.Scale(zero=False), title="Weight"),
        y=alt.Y('plc:N', title="Placement")
        ).properties(height=750, width= 500, title="Distribution of all placement values of horses by weight"
        ).configure_axis(titleFontSize=15, labelFontSize=15
    ).configure_title(fontSize=16)
    
    weight_dist.save(f"{file_path_out}/weight_dist.png")

    
# script entry point
if __name__ == '__main__':
    main(opt["<file_path_in>"], opt["<file_path_out>"])


