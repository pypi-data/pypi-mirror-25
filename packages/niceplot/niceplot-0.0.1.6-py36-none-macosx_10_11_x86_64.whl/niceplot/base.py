import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
sns.set_style("ticks")
from plot import plot

class NicePlot(object):
    def __init__(self, *args, **kwargs):
        self.lof = []

    def __getitem__(self, key):
        return self.lof[key-1]

    def add(self, *args, **kwargs):
        if "number" not in kwargs:
            kwargs["number"] = len(self.lof)+1
        newfig = Figure(*args, **kwargs)
        self.lof.append(newfig)

    def fig(self, number):
        return self.lof[number-1]

class Figure(matplotlib.figure.Figure):
    def __init__(self, *args, **kwargs):
        defaults = {"title": "",
                    "number": 1,
                    "width": 4,
                    "height": 2,
                    "styleset": {"dpi": 300}}

        self.props = {}
        for default in defaults:
            self.props[default] = defaults[default]
        for kwarg in kwargs:
            self.props[kwarg] = kwargs[kwarg]

        figtitle = "Fig. " + str(self.number)
        if len(self.title)>0:
            figtitle += ": " + self.title
        self = plt.figure(figtitle, figsize=(self.props["width"], self.props["height"]), dpi=self.styleset['dpi'], tight_layout=True)
        self.panels = False
        self.ax = None

    def __repr__(self):
        return self.ax

    def __str__(self):
        return "Fig {:} (w: {:}/h: {:})".format(self.props["number"], self.props["width"], self.props["height"])

    def __getattr__(self, name):
        try:
            return self.props[name]
        except KeyError:
            return None

    def draw(func):
        pass


def main():
    import numpy as np

    L = 2 * np.pi
    x = np.linspace(0, L)
    shift = np.linspace(0, L, 4, endpoint=False)
    """
    for s in shift:
        ax.plot(x, np.sin(x + s), '-')
    ax.set_xlim([x[0], x[-1]])
    """

    figs = NicePlot(units="inch")
    figs.add(title="Awesome plot")
    for s in shift:
        figs[1].ax = plot(x, np.sin(x + s), '-')
    plt.show()


if __name__ == '__main__':
    main()
