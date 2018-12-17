import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file


def visualize_heatmap_hit_ratio(profit_heatmap, hit_heatmap):
    """
    Plots two heatmaps together
    We look at areas which both give us satisfactory returns and hit ratio
    """
    fig, (ax, ax2) = plt.subplots(ncols=2)
    fig.subplots_adjust(wspace=0.01)
    sns.heatmap(profit_heatmap, cmap='RdYlGn_r', ax=ax, cbar=False)
    fig.colorbar(ax.collections[0], ax=ax, location="left", use_gridspec=False, pad=0.2)
    sns.heatmap(hit_heatmap, cmap='RdYlGn_r', ax=ax2, cbar=False)
    fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.2)
    ax2.yaxis.tick_right()
    ax2.tick_params(rotation=0)
    plt.show()
    return True


def visualize_heatmap_hit_ratio(pnl_data):
    """
    Plots cumulative returns
    """
    plt.plot(pnl_data['filtered_signals_pnl'].cumsum())
    plt.plot(pnl_data['rsi_signal_pnl'].cumsum())
    plt.plot(pnl_data['macd_signal_pnl'].cumsum())
    plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    return True


def bokeh_cumulative_return(pnl_data):
    pnl_data.index.name = 'Date'
    pnl_data.index = pd.to_datetime(pnl_data.index)
    pnl_data.sort_index(inplace=True)
    pnl_data['cumulative_filtered_pnl'] = pnl_data['filtered_signals_pnl'].cumsum()
    pnl_data['rsi_pnl'] = pnl_data['rsi_signal_pnl'].cumsum()
    pnl_data['macd_pnl'] = pnl_data['macd_signal_pnl'].cumsum()
    source = ColumnDataSource(pnl_data)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=350)
    p.line('Date', 'cumulative_filtered_pnl', source=source, legend="filtered")
    p.line('Date', 'macd_pnl', source=source, legend="macd", color="orange")
    p.line('Date', 'rsi_pnl', source=source, legend="rsi", color="green")

    output_file("ts.html")
    show(p)
