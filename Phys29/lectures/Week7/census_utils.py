import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

def plot_census_data(outfile=None):
    """
    Plots the distribution of household income in the US in 2022 using the American 
    Community Survey data.
    """

    # Load the data
    df = pd.read_csv('../../homework/HW5/data/census_income_data_2022.csv')

    # Filter out all people with incomes less than or equal to zero
    filtered_df = df[df['HINCP'] > 0]

    # Construct the bins
    bin_width = 10000
    bins = np.array([i for i in range(0, 300000-bin_width + 1, bin_width)] + [300000, 350000, np.inf], dtype=float)

    bins_for_plot = np.arange(0, 300000 + 2*bin_width+1, bin_width)

    # Compute the histogram using np.histogram
    hist, bin_edges = np.histogram(filtered_df['HINCP'], bins=bins, weights=filtered_df['WGTP'])

    # Normalize the histogram by the total weight
    total_weight = np.sum(hist)
    hist_normalized = (hist / total_weight)*100.0

    # Create a figure and axes
    figsize = (12, 6) if outfile is not None else (9, 4.5)
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the histogram as a bar chart
    ax.bar(bins_for_plot[:-1], hist_normalized, width=np.diff(bins_for_plot), align='edge', color='orange', alpha=1.0, edgecolor='black', zorder=10)

    # Set labels and title
    ax.set_xlabel('Income', fontsize=18)
    ax.set_ylabel('Percentage of Households', fontsize=18)
    ax.set_title('Distribution of US Household Income in 2022', fontsize=20)

    # Create labels for the bins
    labels = ['${:,}-{:,}'.format(int(bin_edges[i]), int(bin_edges[i+1])) for i in range(len(bin_edges)-3)] + ['$300,000-350,000', '>$350,000']

    bins_for_plot_center = (bins_for_plot[1:] + bins_for_plot[:-1]) / 2
    # Set the x-ticks and x-tick labels
    ax.set_xticks(bins_for_plot_center)
    ax.set_xticklabels(labels, rotation='vertical')

    # Force the y-axis major ticks to be one unit apart
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # Add minor ticks to the y-axis
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    # Set ticks on both sides of the y-axis
    ax.yaxis.set_ticks_position('both')
    # Hide the labels of the second y-axis
    ax.yaxis.set_tick_params(labelleft=True, labelright=False)
    ax.set_xlim((-10000, 300000 + 3*bin_width))
    ax.set_ylim((0,1.1*max(hist_normalized)))

    # Manually draw the grid lines
    for y in ax.get_yticks():
           ax.hlines(y, xmin=ax.get_xlim()[0], xmax=ax.get_xlim()[1], colors='black', linestyles='solid', linewidth=0.5, alpha=0.3, zorder=0)

    # Set the x-ticks and x-tick labels
    ax.set_xticks(bins_for_plot_center)
    ax.set_xticklabels(labels, rotation='vertical')

    # Increase the font size of the x-tick labels
    ax.tick_params(axis='x', labelsize=12)
    # Increase the font size of the y-tick labels
    ax.tick_params(axis='y', labelsize=16)

    # Save the figure to a file
    if outfile is not None:
        plt.savefig(outfile, dpi=1000, bbox_inches='tight')

    return     


def generate_fake_census_data(n_samples=1000000, seed=42, plot=False):
    """
    Creates a fake dataset of household income in the US in 2022 by sampling the distribution
    of household income from the American Community Survey data.
 
    Parameters
    ----------
    n_samples : int
        The number of samples to generate.
    seed : int, optional
        The random seed to use. The default is 42.
    plot : bool, optional
        If True, plot the histogram of the samples on top of the histogram of the real data to 
        very that the code is working
        
    Returns
    -------
    income_samples : ndarray
        An array of shape=(n_samples,) containing the sampled household incomes (in dollars). 
    """

    # Load the data
    df = pd.read_csv('../../homework/HW5/data/census_income_data_2022.csv')

    # Filter out all people with incomes less than or equal to zero
    filtered_df = df[df['HINCP'] > 0]
    incomes = filtered_df['HINCP'].values
    weights = filtered_df['WGTP'].values

    # Sort the incomes
    idx = np.argsort(incomes)
    sw = weights[idx]
    # Compute the CDF(>I)
    cdf = np.float64(np.cumsum(sw[::-1])[::-1])
    cdf /= cdf[0]
    # Now sample this distribution 

    rng = np.random.default_rng(seed)
    percenties = rng.uniform(0, 1, n_samples)
    income_samples = np.interp(percenties, 1.0 - cdf, incomes[idx])

    # Construct the bins
    bin_width = 10000
    # Maximum value is 2,481,200, so go up to 2.5 million
    bins = np.arange(0, 2500000, bin_width)
    counts_real, _ = np.histogram(incomes, bins=bins, weights=weights)
    N_tot  = np.sum(weights)
    counts_sample, _ = np.histogram(income_samples, bins=bins)

    # Create a figure and axes
    if plot: 
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(bins[:-1], counts_real/N_tot, width=np.diff(bins), align='edge', color='orange', alpha=0.5, edgecolor='black', zorder=10)
        ax.bar(bins[:-1], counts_sample/n_samples, width=np.diff(bins), align='edge', color='blue', alpha=0.5, edgecolor='black', zorder=2)
        plt.yscale('log')

    return income_samples