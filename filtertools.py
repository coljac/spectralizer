import glob
import numpy as np
import sedpy
import glob
import pathlib
FILTER_DIR = str(pathlib.Path(sedpy.__file__).parent) + "/data/filters"

telescopes = ["JWST", "HST", "SLOAN", "DECAM"]

class Filter(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

def get_telescopes():
    return ["JWST"]

def get_instruments():
    instr = set([x.split("/")[-1].split("_")[0] for x in glob.glob(f"{FILTER_DIR}/*.par")])
    return sorted(list(instr))


def get_all_filters():
    filters = glob.glob(f"{FILTER_DIR}/*.par")
    filters = sorted([f.replace(FILTER_DIR + "/", "")[:-4] for f in filters])
    return [x + " all" for x in get_instruments()] + filters

def load_filter(fname):
    filts = []
    if "all" in fname:
        scope = fname.replace(" all", "")
        filter_files = glob.glob(f"{FILTER_DIR}/{scope}*.par")
        for ff in filter_files:
            data = np.loadtxt(ff)
            filts.append(Filter(ff.split("/")[-1].replace(".par", ""), data))
    else:
        filts.append(Filter(fname, np.loadtxt(f"{FILTER_DIR}/{fname}.par")))
    return filts

def get_filters_by_telescope(telescope, instrument=""):
    filters = [f for f in get_all_filters() if f.startswith(telescope.upper())]
    filters = [f for f in filters if instrument in f]
    return filters


