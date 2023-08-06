from io import StringIO  # StringIO behaves like a file object

import numpy as np
from matplotlib import pyplot as plt


def plot_data(df, elements, property, thickness, e_min, e_max, n_points, file_name='data', x_label=None,
              figsize=(10, 6), show_plot=False):
    thickness = ', thickness={} [$\mathrm{{\mu}}$m]'.format(thickness) if property == 'transmission' else ''

    fig = plt.figure(figsize=figsize)
    axes = fig.add_subplot(111)
    ax = df.plot(x_label, grid=True, ax=axes)
    ax.set_title(r'{}: {} ({}-{} eV, {} points{})'.format(
        property.capitalize(),
        ', '.join(elements),
        e_min,
        e_max,
        n_points,
        thickness,
    ))
    ax.set_xlabel(x_label)
    ax.set_ylabel('{}'.format(property.capitalize()))
    plt.savefig('{}.png'.format(file_name))
    if show_plot:
        plt.show()


def save_to_csv(df, file_name='data', index=False):
    df.to_csv('{}.csv'.format(file_name), index=index)


def to_dataframe(d, elements):
    """Convert a list of strings, each representing the read data, to a Pandas DataFrame object.

    :param d: a list of strings, each representing the read data.
    :param elements: Chemical elements of interest.
    :return: a tuple of DataFrame and the parsed columns.
    """
    import pandas as pd
    df = None
    columns = None
    for i, str_data in enumerate(d):
        element = elements[i]
        c = StringIO(str_data)
        title, columns = str_data.split('\n')[0:2]
        columns = [x.strip() for x in columns.strip().split(',')]
        columns[1] = '{} {}'.format(columns[1], element) if len(elements) > 1 else columns[1]
        data = np.loadtxt(c, skiprows=2)
        if df is None:
            df = pd.DataFrame(data[:, :2], columns=columns[:2])
        else:
            df[columns[1]] = data[:, 1]
    return df, columns
