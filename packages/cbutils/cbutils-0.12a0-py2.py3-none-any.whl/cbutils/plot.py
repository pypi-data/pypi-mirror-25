

def set_pct_to_bars(ax, total=None, bars=None, **kwargs):
    """

    Set percentage text to bars.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        axis to annotate the text
    total_count: int
        total count of anything used to calculate percentage

    kwargs: keyword arguments

    Returns
    -------
    matplotlib.axes.Axes

    """


    # If bar patches is not passed uses patches found in axes.
    # This propably leads to weird text if other patches besides
    # the bars of count exists
    patches = bars if bars else ax.patches

    if total is None or total <= 0:
        total = sum([p.get_height() for p in patches])

    # Setup some keywords parameter if exists else set default
    x_offset = kwargs['x_offset'] if 'x_offset' in kwargs else 0
    y_offset = kwargs['y_offset'] if 'y_offset' in kwargs else 0
    x_factor = kwargs['x_factor'] if 'x_factor' in kwargs else 1
    y_factor = kwargs['y_factor'] if 'y_factor' in kwargs else 1
    fmt = kwargs['fmt'] if 'fmt' in kwargs else '%.2f%%'
    va = kwargs['va'] if 'va' in kwargs else 'center'
    ha = kwargs['ha'] if 'ha' in kwargs else 'center'
    fontsize = kwargs['fontsize'] if 'fontsize' in kwargs else 12
    fontweight = kwargs['fontweight'] if 'fontweight' in kwargs else 'normal'
    rotation = kwargs['rotation'] if 'rotation' in kwargs else 'horizontal'


    for p in patches:

        y = p.get_height()  # Same as value
        x = p.get_x() + p.get_width() / 2  # Center of the bar

        ax.text(
            (x + x_offset) * x_factor,
            (y + y_offset) * y_factor,
            fmt % (100 * y / total),
            va=va,
            ha=ha,
            fontsize=fontsize,
            fontweight=fontweight,
            rotation=rotation
        )
    return ax