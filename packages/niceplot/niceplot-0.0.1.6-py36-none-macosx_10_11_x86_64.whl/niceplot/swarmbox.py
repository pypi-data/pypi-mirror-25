# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
import matplotlib
import sys
matplotlib.use('TKAgg')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
from niceplot.helper import get_multi

#### plotting
def stars(p):
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "ns"

def swarmbox(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
                dodge=False, orient=None, color=None, palette=None, table=False,
                size=5, edgecolor="gray", linewidth=0, colors=None, ax=None, **kwargs):
    # default parameters
    defs = {
                'ps':   2,          # pointsize for swarmplot (3)
                'pc':   '#666666',  # pointcolor for swarmplot
                'w':    .5,         # boxwidth for boxplot (0.35)
                'lw':   0.0,        # linewidth for boxplot
                'sat':  1.,         # saturation for boxplot
                'mlw':  0.3,        # width for median lines
    }

    # multiconditions
    data, sorted_x, sorted_order, unique_ones, plt_table = get_multi(data, x, order)

    # axis dimensions
    #ax.set_ylim([-2.,max_dur + 2.]) # this is needed for swarmplot to work!!!

    # actual plotting using seaborn functions
    # boxplot
    ax = sns.boxplot(x=sorted_x, y=y, hue=hue, data=data, order=sorted_order, hue_order=hue_order,
                        orient=orient, color=color, palette=colors, saturation=defs['sat'],
                        width=defs['w'], linewidth=defs['lw'], ax=ax, boxprops=dict(lw=0.0), showfliers=False, **kwargs)
    # swarmplot
    ax = sns.swarmplot(x=sorted_x, y=y, hue=hue, data=data, order=sorted_order, hue_order=hue_order,
                        dodge=dodge, orient=orient, color=defs['pc'], palette=palette, size=defs['ps'], ax=ax, **kwargs)
    # median lines
    medians = data.groupby(sorted_x)[y].median()
    dx = defs['mlw']
    for pos, median in enumerate(medians):
        ax.hlines(median, pos-dx, pos+dx, lw=1.5, zorder=10)

    ## figure aesthetics
    #ax.set_yticks(np.arange(0, max_dur+1, div))
    sns.despine(ax=ax, bottom=True, trim=True)
    ax.get_xaxis().set_visible(False)

    # Add a table at the bottom of the axes
    ### requires UNICODE encoding
    if plt_table:
        cells = []
        for ix, each_row in enumerate(x):
            if data[each_row].dtype == bool:
                #cells.append([ "⬤" if entry[ix] else "◯" for entry in unique_ones])
                cells.append([u"\u25CF" if entry[ix] else u"\u25CB" for entry in unique_ones])
            else:
                cells.append([str(entry[ix]) for entry in unique_ones])
        rows = x
        xtrarows = [each.count("\n") for each in rows]
        nrows = len(rows)
        for each in xtrarows:
            nrows += each
        print("#rows:", nrows)
        condition_table = ax.table(cellText=cells, cellLoc='center', rowLabels=rows, rowLoc = 'right', loc='bottom', fontsize=12, bbox=[0.00, -0.35, 1., 0.3])
        table_props = condition_table.properties()
        table_cells = table_props['celld']
        for pos, cell in table_cells.items():
            cell.set_height(xtrarows[pos[0]]+1)
            cell.set_linewidth(0.5)
            cell.set_edgecolor('#424242')
        acells = table_props['child_artists']

        # Adjust layout to make room for the table:
        plt.subplots_adjust(top=0.9, bottom=0.05*nrows, hspace=0.15*nrows, wspace=1.)
    return ax
