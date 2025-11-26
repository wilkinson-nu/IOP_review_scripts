import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_comp, get_chain, make_two_panel_plot

## Use double precision for TTree draw
gEnv.SetValue("Hist.Precision.1D", "double")

## No need to see the plots appear here
gROOT.SetBatch(1)
gStyle.SetLineWidth(3)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(4)

gStyle.SetTextSize(0.05)
gStyle.SetLabelSize(0.05,"xyzt")
gStyle.SetTitleSize(0.05,"xyzt")

gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetNdivisions(505, "XY")

gROOT .ForceStyle()

TH1.SetDefaultSumw2()
gStyle.SetLineWidth(3)

## Sort out the position of the y axis exponent...
TGaxis.SetExponentOffset(-0.06, 0., "y")

def make_T2K_theta_plots(inputDir="inputs/"):

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
    
    ## QE reco
    # qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0 && Sum$(pdg==2212) > 0"
    qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0 && nfsp > 0"
    ## qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"

    qe_cut_o16 = qe_cut + "&& tgta != 1 && tgt != 1000010010"
    qe_cut_h1  = qe_cut + "&& !(tgta != 1 && tgt != 1000010010)"
    
    ## Because the binning is a bit funky
    # custom_binning = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]
    custom_binning = [0, 3, 6, 9, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 180]
    
    ## Loop over configs
    det = "T2KND"
    targ = "H2O"
    for flux in ["FHC_numu", "RHC_numubar"]:
        ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]
        
        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_theta_scaled_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut, \
                            "#theta_{#mu} (degrees); Scaled cross section", [0.65, 0.45, 0.85, 0.93], norm="theta", lineStyle="C", yRatLimits=[0, 2.1])
        
        make_generator_comp("plots/"+det+"_"+flux+"_O16_theta_scaled_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut_o16, \
                            "#theta_{#mu} (degrees); Scaled cross section", [0.65, 0.45, 0.85, 0.93], norm="theta", lineStyle="C", yRatLimits=[0, 2.1])

        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_theta_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut, \
                            "#theta_{#mu} (degrees); d#sigma/d#theta_{#mu} (#times 10^{-38} cm^{2}/nucleon)", [0.65, 0.45, 0.85, 0.93], norm=None, lineStyle="C", yRatLimits=[0, 2.1])

        make_generator_comp("plots/"+det+"_"+flux+"_O16_theta_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut_o16, \
                            "#theta_{#mu} (degrees); d#sigma/d#theta_{#mu} (#times 10^{-38} cm^{2}/nucleon)", [0.65, 0.45, 0.85, 0.93], norm=None, lineStyle="C", yRatLimits=[0, 2.1])

        
        if flux == "RHC_numubar":
            make_generator_comp("plots/"+det+"_"+flux+"_H1_theta_scaled_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut_h1, \
                                "#theta_{#mu} (degrees); Scaled cross section", [0.65, 0.45, 0.85, 0.93], norm="theta", lineStyle="C", yRatLimits=[0, 2.1])

            make_generator_comp("plots/"+det+"_"+flux+"_H1_theta_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, qe_cut_h1, \
                                "#theta_{#mu} (degrees); d#sigma/d#theta_{#mu} (#times 10^{-38} cm^{2}/nucleon)", [0.65, 0.45, 0.85, 0.93], norm=None, lineStyle="C", \
                                yRatLimits=[0, 2.1])

            make_generator_comp("plots/"+det+"_"+flux+"_H1_theta_CCINC_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, \
                                "cc==1 && nfsp > 0 && !(tgta != 1 && tgt != 1000010010)", \
                                "#theta_{#mu} (degrees); d#sigma/d#theta_{#mu} (#times 10^{-38} cm^{2}/nucleon)", [0.65, 0.45, 0.85, 0.93], norm=None, lineStyle="C", \
                                yRatLimits=[0, 2.1])


            
def make_DUNE_theta_plots(inputDir="inputs/"):

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
    
    ## CCinclusive
    ccinc = "cc==1"

    ## Funky binning
    custom_binning = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110, 120]

    ## Loop over configs
    det = "DUNEND"
    targ = "Ar40"
    for flux in ["FHC_numu", "RHC_numubar"]:
        ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        make_generator_comp("plots/"+det+"_"+flux+"_Ar40_theta_scaled_gencomp.pdf", inFileList, nameList, colzList, lineList, "acos(CosLep)*180/pi", custom_binning, ccinc, \
                            "#theta_{#mu} (degrees); Scaled cross section", [0.65, 0.45, 0.85, 0.93], norm="theta", lineStyle="C", yRatLimits=[0, 2.1])

if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    make_T2K_theta_plots(inputDir)
    # make_DUNE_theta_plots(inputDir)

