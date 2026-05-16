import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob
from plotting_functions import make_generator_comp

## Use double precision for TTree draw                                                                                                                                                   
gEnv.SetValue("Hist.Precision.1D", "double")

## No need to see the plots appear here                                                                                                                                                  
gROOT.SetBatch(1)
gStyle.SetLineWidth(3)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(4)

gStyle.SetTextSize(0.06)
gStyle.SetLabelSize(0.06,"xyzt")
gStyle.SetTitleSize(0.07,"xyzt")

gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetNdivisions(505, "XY")
gStyle.SetLineStyleString(11,"40 20 40 20")
gStyle.SetLineStyleString(12,"20 10 20 10")

gROOT .ForceStyle()

TH1.SetDefaultSumw2()
gStyle.SetLineWidth(3)

## Sort out the position of the y axis exponent...                                                                                                                                       
TGaxis.SetExponentOffset(-0.06, 0., "y")


kkMuted0  = TColor(8000,  51/255.,  34/255., 136/255.)
kkMuted1  = TColor(8001, 136/255., 204/255., 238/255.)
kkMuted2  = TColor(8002,  68/255., 170/255., 153/255.)
kkMuted3  = TColor(8003,  17/255., 119/255.,  51/255.)
kkMuted4  = TColor(8004, 153/255., 153/255.,  51/255.)
kkMuted5  = TColor(8005, 221/255., 204/255., 119/255.)
kkMuted6  = TColor(8006, 204/255., 102/255., 119/255.)
kkMuted7  = TColor(8007, 136/255.,  34/255.,  85/255.)
kkMuted8  = TColor(8008, 170/255.,  68/255., 153/255.)
kkMuted9  = TColor(8009, 221/255., 221/255., 221/255.)


def make_xsec_energy_comp_plots(inputDir="inputs/", flav="numu", targ="Ar40", sample="ccinc", legDim=[0.65, 0.06, 0.93, 0.45]):

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
    
    cut = "cc==1 && Enu_true > 0.13 && nfsp > 0" ## && tgta != 1 && tgt != 1000010010" ## && Enu_true > 0.2"
    sample_label = "CCINC"
    
    binning = [0, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0]

    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"
        binning = [0, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]
    if sample == "ccqe":
        cut += "&& abs(Mode)==1"
        sample_label = "CCQE"
    if sample == "2p2h":
        cut += "&& abs(Mode)==2"
        sample_label = "2p2h"

    if sample == "ATM":
        binning = [0, 0.13, 0.17, 0.21, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

        
    ## Use the ensemble files
    inFileList = [inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                  inputDir+"/MONOENSEMBLE_"+flav+"_"+targ+"_*GeV_GiBUU_100k_*_NUISFLAT.root"\
                  ]
    
    make_generator_comp("plots/XSEC_"+targ+"_"+flav+"_Enu_"+sample+"_gencomp.pdf", inFileList, \
                        nameList, colzList, lineList, "Enu_true", binning, cut, \
                        "E_{#nu}^{true} (GeV); #sigma(E_{#nu}^{true}) (#times 10^{-38} cm^{2}/nucleon)", \
                        legDim=legDim, yRatLimits=[0.5, 2.2], norm="enu_ensemble", lineStyle="L")
    
if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"

    ## for flav in ["14", "-14"]:
    ##     make_xsec_energy_comp_plots(inputDir, flav, "Ar40", "ccinc", legDim=[0.25, 0.5, 0.45, 0.93])
    ##     make_xsec_energy_comp_plots(inputDir, flav, "O16", "cc0pi", legDim=[0.65, 0.06, 0.93, 0.45])
    ##     make_xsec_energy_comp_plots(inputDir, flav, "C12", "cc0pi", legDim=[0.65, 0.06, 0.93, 0.45])


    for flav in ["14", "-14", "12", "-12"]:
        make_xsec_energy_comp_plots(inputDir, flav, "O16", "ATM", legDim=[0.25, 0.5, 0.45, 0.93])

            

