from utils import give_ax

def plot(*args, **kwargs):
    ax, args, kwargs = give_ax(*args, **kwargs)
    #show_ticks = kwargs.pop('show_ticks', False)

    lines = ax.plot(*args, **kwargs)
    #remove_chartjunk(ax, ['top', 'right'], show_ticks=show_ticks)
    return lines
