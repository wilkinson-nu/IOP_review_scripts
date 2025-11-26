import ROOT
import os
from array import array
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_double_ratio_comp

## def get_flav_label(flav):
##     label = "#nu"
##     if "bar" in flav: label = "#bar{"+label+"}"
##     if "mu" in flav: label += "_{#mu}"
##     if "tau" in flav: label += "_{#tau}"
##     if "e" in flav: label += "_{e}"
##     return label

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
    print("Unknown target", targ)
    return targ


def make_flav_double_ratio_plots(inputDir="inputs/", flavA="nuebar", flavB="numubar", \
                                 flavC="nue", flavD="numu", targ="Ar40", sample="ccinc", yLimits=[0,None]):

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
    
    cut = "cc==1 && nfsp > 0" # && tgta != 1 && tgt != 1000010010 && Enu_true > 0.12"
    sample_label = "CCINC"
    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"
        
    ## As FSI doesn't make any difference, use all GENIEv3_G18 models as one...
    inFileListA = [inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavA+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                   ]
    
    inFileListB = [inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavB+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                   ]

    inFileListC = [inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavC+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                   ]
    
    inFileListD = [inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                   inputDir+"/MONOENSEMBLE_"+flavD+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                   ]

    ## Input fluxes generated with:
    ## E_MONO_FINE=( 0.105 0.115 0.125 0.135 0.145 0.155 0.165 0.175 \
    ##           0.185 0.195 0.205 0.215 0.225 0.235 0.245 0.255 \
    ##           0.265 0.275 0.285 0.295 0.305 0.315 0.325 0.335 \
    ##           0.345 0.355 0.365 0.375 0.385 0.395 0.405 0.415 \
    ##           0.425 0.435 0.445 0.455 0.465 0.475 0.485 0.495 \
    ##           0.525 0.575 0.625 0.675 0.725 0.775 0.825 0.875 \
    ##           0.925 0.975 1.025 1.075 1.125 1.175 1.225 1.275 \
    ##           1.325 1.375 1.425 1.475 1.525 1.575 1.625 1.675 \
    ##           1.725 1.775 1.825 1.875 1.925 1.975 )

    binning = [0, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.18, 0.2, 0.22, 0.24, 0.28, 0.32, 0.38, 0.44, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

    make_generator_double_ratio_comp("plots/XSEC_double_flav_ratio_"+targ+"_enu_"+sample+"_gencomp.pdf",
                                     inFileListA, inFileListB, inFileListC, inFileListD, \
                                     nameList, colzList, lineList, "Enu_true", binning, cut, \
                                     "E_{#nu}^{true} (GeV); ("+get_flav_label(flavA)+"/"+get_flav_label(flavB)+")/("+get_flav_label(flavC)+"/"+\
                                     get_flav_label(flavD)+") "+ get_targ_label(targ)+" "+sample_label+" ratio",
                                     legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0.65, 1.65], yRatLimits=[0.5, 1.1], lineStyle="][ ")
    
if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"

    targ="Ar40"
    sample="ccinc"
    make_flav_double_ratio_plots(inputDir, "-12", "-14", "12", "14", targ, sample, [0.75, 1.35])

    targ="O16"
    sample="cc0pi"
    make_flav_double_ratio_plots(inputDir, "-12", "-14", "12", "14", targ, sample, [0.75, 1.35])

    targ="O16"
    sample="ccinc"
    make_flav_double_ratio_plots(inputDir, "-12", "-14", "12", "14", targ, sample, [0.75, 1.35])


