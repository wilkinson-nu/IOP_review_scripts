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

def make_flav_ratio_plots(inputDir="inputs/", flav1="nue", flav2="numu", targ="Ar40", sample="ccinc", yLimits=[0.65, 1.25], \
                          yRatLimits=[0.75, 1.25], legDim=[0.65, 0.06, 0.93, 0.45], binning=None, outdir="plots"):

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
    
    cut = "cc==1 && nfsp > 0"
    
    # if "nue" in flav1 or "nue" in flav2:
    #     cut += "&& Enu_true > 0.11"
    
    sample_label = "CCINC"

    ## Add a default binning
    if binning == None:
        binning = [0, 0.10, 0.12, 0.14, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0]

    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"
        
    inFileNumList = [inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav1+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                     ]

    inFileDenList = [inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flav2+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                     ]

    make_generator_ratio_comp(outdir+"/XSEC_ratio_"+flav1+"_over_"+flav2+"_"+targ+"_enu_"+sample+"_gencomp.pdf", inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "Enu_true", binning, cut, \
                              "E_{#nu}^{true} (GeV); "+get_flav_label(flav1)+"/"+get_flav_label(flav2)+" "+get_targ_label(targ)+" "+sample_label+" ratio", \
                              legDim=legDim, yLimits=yLimits, yRatLimits=yRatLimits, norm="enu_ensemble", lineStyle="][")

if __name__ == "__main__":

    # Parse some args
    parser = argparse.ArgumentParser("make_flav_ratio_comp")

    # Add arguments
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--flav1', type=str, required=True)
    parser.add_argument('--flav2', type=str, required=True)
    parser.add_argument('--targ', type=str, required=True)
    parser.add_argument('--sample', type=str, required=True)
    parser.add_argument('--y_limits', type=float, nargs=2, required=True)
    parser.add_argument('--y_rat_limits', type=float, nargs=2, required=True)
    parser.add_argument('--leg_dim', type=float, nargs=4, required=True)

    ## Optional
    parser.add_argument('--lowe', type=int, choices=[0,1], default=0)

    ## Parse arguments from command line
    args = parser.parse_args()
    
    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))
    
    ## Sort binning
    binning = [0, 0.10, 0.12, 0.14, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0]
    if args.lowe == 1:
        binning = [0.2, 0.22, 0.24, 0.28, 0.32, 0.38, 0.44, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

    make_flav_ratio_plots(args.input,
                          args.flav1,
                          args.flav2,
                          args.targ,
                          args.sample,
                          yLimits=args.y_limits,
                          yRatLimits=args.y_rat_limits,
                          legDim=args.leg_dim,
                          binning=binning,
                          outdir=args.output)

