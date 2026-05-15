import argparse
import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_ratio_comp

def get_flav_label(flav):
    if flav == "-14": return "#bar{#nu}_{#mu}"
    if flav == "-12": return "#bar{#nu}_{e}"
    if flav == "14": return "#nu_{#mu}"
    if flav == "12": return "#nu_{e}"
    return "#nu"

## In this case, ignore hydrogen...
def get_targ_label(targ):
    if targ == "Ar40": return "^{40}Ar"
    if targ == "C8H8": return "^{12}C"
    if targ == "H2O": return "^{16}O"
    if targ == "C12": return "^{12}C"
    if targ == "O16": return "^{16}O"
    print("Unknown target", targ)
    return targ


def make_targ_ratio_plots(inputDir="inputs/", targ1="C8H8", targ2="H2O", flav="numu", sample="ccinc", outdir="plots"):

    nameList = ["GENIE 10a",\
                "CRPA",\
                "NEUT",\
		"NEUT DCC",\
                "NuWro 19",\
		"NuWro 25",\
                "GiBUU"\
		]
    colzList = [8000, 8003, 8004, 8005, 8006, 8007, 8001]
    lineList = [1, 1, 1, 7, 1, 7, 1]
    
    cut = "cc==1 && nfsp > 0 && Enu_true > 0.13"
    # if "nue" in flav: cut += "&& Enu_true > 0.11"

    sample_label = "CCINC"
    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"
    if sample == "cc1pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(abs(pdg)==211 || pdg==111)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC1#pi"
    if sample == "cc2pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==2 && Sum$(abs(pdg)==211 || pdg==111)==2 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC2#pi"

    inFileNumList = [inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ1+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                     ]

    inFileDenList = [inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav+"_"+targ2+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                     ]

    binning = [0, 0.13, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]

    make_generator_ratio_comp(outdir+"/XSEC_ratio_"+targ1+"_over_"+targ2+"_"+flav+"_enu_"+sample+"_gencomp.pdf", inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "Enu_true", binning, cut, \
                              "E_{#nu}^{true} (GeV);"+get_flav_label(flav)+" "+get_targ_label(targ1)+"/"+get_targ_label(targ2)+" "+sample_label+" ratio", \
                              legDim=[0.65, 0.04, 0.93, 0.43], yLimits=[0.62, 1.28], yRatLimits=[0.75, 1.25], norm="enu_ensemble", lineStyle="][ ")
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_targ_ratio_comp")

    # Add arguments
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--targ1', type=str, required=True)
    parser.add_argument('--targ2', type=str, required=True)
    parser.add_argument('--flav', type=str, required=True)
    parser.add_argument('--sample', type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    make_targ_ratio_plots(args.input,
                          args.targ1,
                          args.targ2,
                          args.flav,
                          args.sample,
                          outdir=args.output)
    


