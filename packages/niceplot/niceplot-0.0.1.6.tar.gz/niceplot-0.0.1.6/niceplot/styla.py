import os, sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.table as mpl_table
import matplotlib.text as mpl_text

def set_font(name, ax=None):
    if ax is None:
        ax = plt.gca()
    for sites in sys.path:
        if os.path.isdir(sites):
            if "fonts" in [folder for folder in os.listdir(sites) if os.path.isdir(os.path.join(sites,folder))]:
                fontfile = os.path.join(sites, "fonts", name+".ttf")

    if os.path.exists(fontfile):
        print("Loading font:", fontfile)
        textprop = fm.FontProperties(fname=fontfile)
        ### find all text objects
        texts = ax.findobj(match=mpl_text.Text)
        for eachtext in texts:
            eachtext.set_fontproperties(textprop)
        ### find all table objects (these contain further text objects)
        tables = ax.findobj(match=mpl_table.Table)
        for eachtable in tables:
            for k, eachcell in eachtable._cells.items():
                this_text = eachcell._text.get_text()
                if this_text == u"\u25CF" or this_text == u"\u25CB":
                    eachcell._text.set_fontname("Arial Unicode MS")
                else:
                    eachcell._text.set_fontproperties(textprop)
    else:
        print(fontfile, os.getcwd())
        print("[ERROR]: selected font does not exist.")
        raise FileNotFoundError
    return ax


### table
"""

"""
