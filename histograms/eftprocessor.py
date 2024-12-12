#!/usr/bin/env python
import numpy as np
import awkward as ak
np.seterr(divide='ignore', invalid='ignore', over='ignore')
from coffea import processor
from coffea.analysis_tools import PackedSelection

# silence warnings due to using NanoGEN instead of full NanoAOD
from coffea.nanoevents import NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False

import hist
from topcoffea.modules.histEFT import HistEFT

# Get the lumi for the given year
def get_lumi(year):
    lumi_dict = {
        "2016APV": 19.52,
        "2016": 16.81,
        "2017": 41.48,
        "2018": 59.83
    }
    if year not in lumi_dict.keys():
        raise Exception(f"(ERROR: Unknown year \"{year}\".")
    else:
        return(lumi_dict[year])

# Clean objects
def is_clean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)

# Main analysis processor
class AnalysisProcessor(processor.ProcessorABC):
    def __init__(self, samples, wc_names_lst=[]):
        self._samples = samples
        self._wc_names_lst = wc_names_lst
        
        # Create the histograms with new scikit hist
        self._histo_dict = {
            "hpt": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="hpt",label="Higgs $p_{T}$ (GeV)", bins=100, start=0, stop=1000, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "q1pt": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="q1pt",label="Quark 1 $p_{T}$ (GeV)", bins=100, start=0, stop=1000, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "q2pt": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="q2pt",label="Quark 2 $p_{T}$ (GeV)", bins=100, start=0, stop=1000, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "mqq": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="mqq",label="Higgs $p_{T}$ (GeV)", bins=100, start=0, stop=5000, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "detaqq": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="detaqq",label="$\Delta\eta_{qq}$", bins=100, start=-6, stop=6, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "dphiqq": HistEFT(
                #hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="dphiqq",label="$\Delta\phi_{qq}$", bins=100, start=-3.15, stop=3.15, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            ),
            "SumOfWeights": processor.value_accumulator(float),
            "EventCount": processor.value_accumulator(int),
        }


    @property
    def columns(self):
        return self._columns

    def process(self, events):

        # Dataset parameters
        dataset = events.metadata['dataset']
        hist_axis_name = self._samples[dataset]["histAxisName"]
        #year   = self._samples[dataset]['year']
        #xsec   = self._samples[dataset]['xsec']
        #sow    = self._samples[dataset]['nSumOfWeights' ]

        # Extract the EFT quadratic coefficients and optionally use them to calculate the coefficients on the w**2 quartic function
        # eft_coeffs is never Jagged so convert immediately to numpy for ease of use.
        eft_coeffs = ak.to_numpy(events['EFTfitCoefficients']) if hasattr(events, "EFTfitCoefficients") else None

        # Initialize objects
        genpart = events.GenPart
        is_final_mask = genpart.hasFlags(["fromHardProcess","isLastCopy"])

        outgoing = events.LHEPart[events.LHEPart.status==1]
        higgs = ak.firsts(outgoing[outgoing.pdgId == 25])
        quarks = outgoing[outgoing.pdgId<=6]

        q1 = ak.firsts(quarks[:,0:1])
        q2 = ak.firsts(quarks[:,1:2])

        ######## Jet selection  ########
        #jets = events.GenJet
        #jets = jets[(jets.pt>30) & (abs(jets.eta)<2.5)]
        #j0 = jets[ak.argmax(jets.pt,axis=-1,keepdims=True)]

        ######## Event selections ########

        #njets = ak.num(jets)
        #at_least_one_jet = ak.fill_none(njets>=1,False)
        #selections = PackedSelection()
        #selections.add('1j', at_least_one_jet)

        ######## Normalization ########

        # Normalize by (xsec/sow)
        #lumi = 1000.0*get_lumi(year)
        #norm = (xsec/sow)*lumi
        #wgts = norm*np.ones_like(events['event'])
        wgts = events.genWeight

        #print(lumi)
        ######## Fill histos ########

        hout = self._histo_dict

        variables_to_fill = {
            "hpt" : higgs.pt,
            "q1pt" : q1.pt,
            "q2pt" : q2.pt,
            "mqq" : (q1+q2).mass,
            "detaqq" : q1.eta - q2.eta,
            "dphiqq" : q1.delta_phi(q2)
        }

        #event_selection_mask = selections.all("2j")

        for var_name, var_values in variables_to_fill.items():

            fill_info = {
                var_name    : var_values,#[event_selection_mask],
                #"process"   : hist_axis_name,
                "weight"    : wgts,#[event_selection_mask],
                "eft_coeff" : eft_coeffs,#[event_selection_mask],
            }

            hout[var_name].fill(**fill_info)

        hout["SumOfWeights"] = np.sum(wgts)
        hout["EventCount"] = len(events)

        return hout

    def postprocess(self, accumulator):
        return accumulator

