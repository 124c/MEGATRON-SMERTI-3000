import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

