import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_comp, make_generator_ratio_comp

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

def make_W_plots(inputDir="inputs/"):

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
    
    ehad_cut = "cc==1"

    ## Loop over configs
    # for det in ["T2KND", "T2KSK_osc", "DUNEND", "DUNEFD_osc"]:
    for det in ["DUNEFD_osc"]:  
        for flux in ["FHC_numu", "RHC_numubar"]:

            targ = "Ar40"
            binning="100,0.5,3"
            if "T2K" in det:
                targ = "H2O"
                binning="100,0.5,2"
            
            ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                          ]

            make_generator_comp("new_plots/"+det+"_"+flux+"_"+targ+"_W_gencomp.pdf", inFileList, nameList, colzList, lineList, "W", binning, ehad_cut, \
                                "W (GeV); d#sigma/dW (#times 10^{-38} cm^{2}/GeV/nucleon)", withRebin=True, legDim=[0.65, 0.44, 0.93, 0.93])

            #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_W_gencomp_noratio.pdf", inFileList, nameList, colzList, lineList, "W", binning, ehad_cut, \
            #                    "W (GeV); d#sigma/dW (#times 10^{-38} cm^{2}/GeV/nucleon)", withRebin=True, include_ratio=False, legDim=[0.6, 0.5, 0.8, 0.93])


def make_W_ratio_plots(inputDir="inputs/"):

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

    ehad_cut = "cc==1"

    ## Loop over configs
    #for det in ["T2KND", "T2KSK_osc", "DUNEND", "DUNEFD_osc"]:
    for det in ["T2K", "DUNE"]:
        for flux in ["FHC_numu", "RHC_numubar"]:

            targ = "Ar40"
            detnd = det+"ND"
            detfd = det+"FD_osc"
            if "T2K" in det:
                targ = "H2O"
                detfd = det+"SK_osc"

            inFileNumList = [inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detfd+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                             ]

            inFileDenList = [inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                             inputDir+"/"+detnd+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                             ]

            ## def make_generator_ratio_comp(outPlotName, inFileNumList, inFileDenList, nameList, colzList, lineList, \
            ##                   plotVar="q0", binning="100,0,5", cut="cc==1", \
	    ##     	      labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", norm="enu_ensemble", \
            ##                   legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], lineStyle="C", \
            ##                   include_ratio=True, withRebin=False, cutDen=None):
            make_generator_ratio_comp("plots/"+det+"_"+flux+"_"+targ+"_W_NDFD_ratio_gencomp.pdf", inFileNumList, inFileDenList, \
                                      nameList, colzList, lineList, "W", "50,0.5,3", ehad_cut, norm="xsec", \
                                      labels="W (GeV); FD/ND", legDim=[0.22, 0.5, 0.42, 0.93], yLimits=[0.6, None], yRatLimits=[0.8, 1.2], include_ratio=True, lineStyle="][")

        ## make_generator_ratio_comp("plots/"+det+"_"+flux+"_"+targ+"_q0_NDFD_ratio_gencomp.pdf", inFileNumList, inFileDenList, \
        ##                           nameList, colzList, lineList, "q0", "60,0,3", ehad_cut, norm="xsec", \
	##                           labels="q_{0} (GeV); FD/ND", legDim=[0.22, 0.5, 0.42, 0.93], yLimits=[0.6, None], yRatLimits=[0.8, 1.2], include_ratio=True, lineStyle="][")

if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    # make_W_ratio_plots(inputDir)
    make_W_plots(inputDir)
