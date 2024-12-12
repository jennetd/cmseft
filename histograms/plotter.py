import os
import pickle
import gzip
import argparse
import matplotlib.pyplot as plt
import topcoffea.modules.utils as utils

import hist
from topcoffea.modules.histEFT import HistEFT

WCPT_EXAMPLES = {
    "nonsm" : {
        'cHudIm' : 1.0,
        'cuBIm' : 1.0, 
        'cHWBtil' : 1.0,
        'cHbox' : 1.0,
        'cHd' : 1.0,
        'cHDD' : 1.0,
        'cuBRe' : 1.0,
        'cuWIm' : 1.0,
        'cHW' : 1.0,
        'cHBtil' : 1.0,
        'cHu' : 1.0,
        'cdWIm' : 1.0,
        'cHWB' : 1.0,
        'cdBIm' : 1.0,
        'cHWtil' : 1.0,
        'cuWRe' : 1.0,
        'cdWRe' : 1.0,
        'cdBRe' : 1.0,
        'cHB' : 1.0,
        'cHj1' : 1.0,
        'cHudRe' : 1.0,
        'cHj3' : 1.0
    },
    "sm" : {
        'cHudIm' : 0.0,
        'cuBIm' : 0.0,
        'cHWBtil' : 0.0,
        'cHbox' : 0.0,
        'cHd' : 0.0,
        'cHDD' : 0.0,
        'cuBRe' : 0.0,
        'cuWIm' : 0.0,
        'cHW' : 0.0,
        'cHBtil' : 0.0,
        'cHu' : 0.0,
        'cdWIm' : 0.0,
        'cHWB' : 0.0,
        'cdBIm' : 0.0,
        'cHWtil' : 0.0,
        'cuWRe' : 0.0,
        'cdWRe' : 0.0,
        'cdBRe' : 0.0,
        'cHB' : 0.0,
        'cHj1' : 0.0,
        'cHudRe' : 0.0,
        'cHj3' : 0.0
    }
}


# Takes a hist with one sparse axis and one dense axis, overlays everything on the sparse axis
def make_single_fig(histo):
    fig, ax = plt.subplots(1, 1, figsize=(7,7))
    histo.plot1d(
        stack=False,
    )
    ax.autoscale(axis='y')
    plt.legend()
    return fig


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_histo_file")
    args = parser.parse_args()

    histo_in = args.input_histo_file

    # Get the histograms
    hin_dict = pickle.load(gzip.open(histo_in))

    # Grab the one we want to plot
    #variable = "j0pt"
    variable = "hpt"
    histo = hin_dict[variable]

    # Print some values
    print("\nValues: SM",histo.eval(None))
    print("\nValues EFT:",histo.eval(WCPT_EXAMPLES["nonsm"]))

    # Make plots at a few wc points
    for wcpt_name, wcpt_dict in WCPT_EXAMPLES.items():
        wc_pt = WCPT_EXAMPLES[wcpt_name]
        histo_to_plot = histo.as_hist(wc_pt)
        fig = make_single_fig(histo_to_plot)
        title = f"vbf_{wcpt_name}.png"
        fig.savefig(os.path.join(".",title))



main()

