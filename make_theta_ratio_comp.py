import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob
import argparse

from plotting_functions import make_generator_comp, make_generator_ratio_comp

def make_theta_ratio_plots(inputDir="inputs/",
                           det="T2K",
                           flux="FHC_numu",
                           sample="ccinc",
                           outdir="plots"):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "NEUT",\
                "NEUT DCC",\
                "NuWro 19",\
                "NuWro 25",\
                "GiBUU"\
		]
    colzList = [8000, 8008, 8002, 8003, 8004, 8005, 8006, 8007, 8001]
    lineList = [1, 12, 7, 1, 1, 7, 1, 7, 1]

    cut = "cc==1 && nfsp > 0"
    sample_label = "CCINC"
    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"

    theta_binning = [0, 3, 6, 9, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 180]
    
    targ = "Ar40"
    detnd = det+"ND"
    detfd = det+"FD_osc"
    
    if "T2K" in det:
        targ = "H2O"
        detfd = det+"SK_osc"

    inFileNumList = [inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                     ]
    
    inFileDenList = [inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                     ]
    
    make_generator_ratio_comp(outdir+"/"+det+"_"+flux+"_"+targ+"_theta_NDFD_ratio_gencomp.pdf", inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "acos(CosLep)*180/pi", theta_binning, cut, norm="xsec", \
                              labels="#theta_{#mu} (degrees); FD/ND", legDim=[0.5, 0.58, 0.95, 0.93], legCols=2, yLimits=[0.6, None], yRatLimits=[0.5, 1.5], include_ratio=True, lineStyle="][")
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_theta_ratio_comp")

    # Add arguments
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det', type=str, required=True)
    parser.add_argument('--flux', type=str, required=True)
    parser.add_argument('--sample', type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    make_theta_ratio_plots(args.input,
                           det=args.det,
                           flux=args.flux,
                           sample=args.sample,
                           outdir=args.output)
