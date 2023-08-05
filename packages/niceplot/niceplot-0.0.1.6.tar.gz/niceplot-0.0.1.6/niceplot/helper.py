import numpy as np
import pandas as pd

def merge(a,b):
    for ax, bx in zip(a,b):
        yield ax + bx

def get_multi(data, x, order):
    if type(x) is str:
        return data, x, order, unique_ones, False
    elif type(x) is list:
        if len(x) > 1:
            all_combins = data[x].apply(tuple, axis=1)
            unique_ones = np.unique(all_combins)
            extra = []
            for each_tuple in unique_ones:
                number = 0.0
                if type(order) is list:
                    for lvl, orders in enumerate(order):
                        for index, item in enumerate(orders):
                            if each_tuple[lvl] == item:
                                number += index*10**(-lvl)
                    extra.append((number,))
            merged = list(merge(unique_ones, extra))
            merged = sorted(merged, key=lambda x: x[2])
            unique_ones = [each[:-1] for each in merged]
            print("Swarmbox plot for multiple categories:", merged)
            data['metacat'] = [-1]*len(data.index)
            for ix, cat in enumerate(merged):
                data.loc[all_combins==cat[:-1], 'metacat'] = ix
            return data, 'metacat', None, unique_ones, True
        else:
            return data, x, order, unique_ones, False
