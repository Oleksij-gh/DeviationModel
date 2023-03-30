import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def get_data(df,  group, row, count_rows):
    """
    df: dataframe
    group: group data name (min, mean, max)
    row: line number from which data slice is required
    count_rows: the number of lines shown on the plot
    """

    columns = [group, 'floor_' + group, 'ceiling_' + group, 'name']
    for column in columns:
        data = np.array(df[column][count_rows * row: count_rows * (row + 1)])
        yield data


def draw_plot(path, count_rows=10):
    """
    path: path to .json dataframe
    count_rows: the number of lines shown on the plot
    """

    df = pd.read_json(path)  # pandas dataframe
    len_df = df.shape[0]  # count rows in dataframe
    height = 0.25  # The heights of the bars
    groups = ['min', 'mean', 'max']  # parts of column names
    root = os.getcwd()  # script directory

    if len_df % count_rows == 0:
        count_plots = len_df // count_rows
    else:
        count_plots = (len_df // count_rows) + 1

    if not os.path.exists(root + '\\plots'):
        os.makedirs(root + '\\plots')
    print('Plots are saved in: ' + root + '\\plots')

    for group in groups:
        for row in range(count_plots):
            truth, floor, ceiling, name = get_data(df, group, row, count_rows)
            index = np.arange(len(truth))
            fig, ax = plt.subplots(figsize=(12, 8))
            plt.title(group.upper(), fontsize=20)
            truth_hist = ax.barh(index, truth, height, color='#f9d946')
            floor_hist = ax.barh(index + height, floor, height, color='#ff9c4b')
            ceiling_hist = ax.barh(index + 2 * height, ceiling, height, color='#ed6a02')
            for hist in [truth_hist, floor_hist, ceiling_hist]:
                ax.bar_label(hist)
            plt.yticks(index + 1.5 * height, name, rotation=60, fontsize=12)
            plt.legend(['truth', 'floor', 'ceiling'])
            ax.grid()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.savefig('plots/'+str(group)+'_'+str(row*count_rows)+'-'+str((row+1)*count_rows)+'.png')
            plt.show()
