import matplotlib as mpl
import matplotlib.pyplot as plt

class Unit():

    def __init__(_val, _unit):
        self.v = _val
        self.u = _unit

    def __str__(self):
        return str(self.v)+" "+self.u



def give_ax(*args, **kwargs):
    """
    Get ax from args or kwargs
    """

    if 'ax' in kwargs:
        ax = kwargs.pop('ax')
    elif 'axes' in kwargs:
        ax = kwargs.pop('axes')
    elif len(args) == 0:
        fig = plt.gcf()
        ax = plt.gca()
    elif isinstance(args[0], mpl.axes.Axes):
        ax = args[0]
        args = args[1:]
    else:
        ax = plt.gca()
    return ax, args, dict(kwargs)
