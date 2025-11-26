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

def make_flav_ratio_plots(inputDir="inputs/", flav1="nue", flav2="numu", targ="Ar40", sample="ccinc", yLimits=[0.65, 1.25], yRatLimits=[0.75, 1.25]):

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

    binning = [0, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.18, 0.2, 0.22, 0.24, 0.28, 0.32, 0.38, 0.44, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

    make_generator_ratio_comp("plots/XSEC_ratio_"+flav1+"_over_"+flav2+"_"+targ+"_enu_"+sample+"_gencomp.pdf", inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "Enu_true", binning, cut, \
                              "E_{#nu}^{true} (GeV); "+get_flav_label(flav1)+"/"+get_flav_label(flav2)+" "+get_targ_label(targ)+" "+sample_label+" ratio", \
                              legDim=[0.65, 0.06, 0.93, 0.45], yLimits=yLimits, yRatLimits=yRatLimits, norm="enu_ensemble", lineStyle="][")

    
def make_targ_ratio_plots(inputDir="inputs/", targ1="C8H8", targ2="H2O", flav="numu", sample="ccinc"):

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

    binning = [0, 0.13, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]

    make_generator_ratio_comp("plots/XSEC_ratio_"+targ1+"_over_"+targ2+"_"+flav+"_enu_"+sample+"_gencomp.pdf", inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "Enu_true", binning, cut, \
                              "E_{#nu}^{true} (GeV);"+get_flav_label(flav)+" "+get_targ_label(targ1)+"/"+get_targ_label(targ2)+" "+sample_label+" ratio", \
                              legDim=[0.65, 0.06, 0.93, 0.45], yLimits=[0.65, 1.35], yRatLimits=[0.8, 1.2], norm="enu_ensemble", lineStyle="][ ")
    

if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"

    targ = "Ar40"
    sample = "ccinc"
    #make_flav_ratio_plots(inputDir, "12", "14", targ, sample, [0.95, 1.8], [0.8, 1.1])
    #make_flav_ratio_plots(inputDir, "-12", "-14", targ, sample, [0.95, 1.8], [0.8, 1.1])
    make_flav_ratio_plots(inputDir, "-12", "12", targ, sample, [0, 0.55], [0.75, 1.5])
    make_flav_ratio_plots(inputDir, "-14", "14", targ, sample, [0, 0.55], [0.75, 1.5])

    targ = "O16"
    sample = "cc0pi"
    #make_flav_ratio_plots(inputDir, "12", "14", targ, sample, [0.95, 1.8], [0.8, 1.1])
    #make_flav_ratio_plots(inputDir, "-12", "-14", targ, sample, [0.95, 1.8], [0.8, 1.1])
    make_flav_ratio_plots(inputDir, "-12", "12", targ, sample, [0, 0.65], [0.75, 1.5])
    make_flav_ratio_plots(inputDir, "-14", "14", targ, sample, [0, 0.65], [0.75, 1.5])

    
    for flav in ["14", "-14"]:
        for sample in ["ccinc", "cc0pi"]: #, "cc1pi", "cc2pi"]:
            make_targ_ratio_plots(inputDir, "Ar40", "C12", flav, sample)
            make_targ_ratio_plots(inputDir, "O16", "C12", flav, sample)


