import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_ratio_comp

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

def make_T2K_erec_threshold_plots(inputDir="inputs/"):

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
    qe_cut = "cc==1 && Sum$( (abs(pdg)>100) * (abs(pdg)<2000) )==0 && Sum$( (abs(pdg)>2300) * (abs(pdg)<100000) )==0"

    ## Special pion < 100 MeV cut
    base_qe_cut = "cc==1 && Sum$(abs(pdg)==111)==0 && Sum$( (abs(pdg)>111) * (abs(pdg)<211) )==0 && Sum$( (abs(pdg)>211) * (abs(pdg)<2000) )==0 && Sum$( (abs(pdg)>2300) * (abs(pdg)<100000) )==0"
    pion_qe_cut = base_qe_cut + "&& Sum$( (abs(pdg)==211) * ((E - 0.1395703918)>0.100) )==0"
    
    ## Loop over configs
    det = "T2KSK_osc"
    targ = "H2O"

    for flux in ["FHC_numu", "RHC_numubar"]:
        
        ## Change to Enu_QE to use a binding energy of 27 MeV! Not 34 like the NUISANCE default...
        binding = 27/1000.
        m1 = 0.93956536
        m2 = 0.93827203
        ml = 0.10565837
        
        ## For antineutrino the nucleons are reversed
        if "numubar" in flux:
            m2 = 0.93956536
            m1 = 0.93827203
            
        mod_enuqe = "(2*("+str(m1)+"-"+str(binding)+")*ELep -"+str(ml)+"*"+str(ml)+" + "+str(m2)+"*"+str(m2)+" - ("+str(m1)+"-"+str(binding)+")*("+str(m1)+"-"+str(binding)+"))/" \
            +"(2*(("+str(m1)+"-"+str(binding)+") - ELep + sqrt(ELep*ELep - "+str(ml)+"*"+str(ml)+")*CosLep))"
        
        
        ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        ## def make_generator_ratio_comp(outPlotName, inFileNumList, inFileDenList, nameList, colzList, lineList, \
        ##                       plotVar="q0", binning="100,0,5", cut="cc==1", \
        ##                       labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", norm="enu_ensemble", \
        ##                       legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], lineStyle="C", \
        ##                       include_ratio=True, withRebin=False, cutDen=None):
        
        make_generator_ratio_comp("plots/"+det+"_"+flux+"_H2O_EnuQEbias_gencomp_threshold.pdf", inFileList, inFileList, nameList, colzList, lineList, \
                                  "("+mod_enuqe+" - Enu_true)/Enu_true", "70,-0.9,0.5", pion_qe_cut, norm="xsec", \
                                  labels="(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; #frac{CC0(#pi >100 MeV)}{CC0#pi}", lineStyle="][", \
                                  legDim=[0.62, 0.5, 0.82, 0.93], yLimits=[1, None], yRatLimits=[0,2.2], cutDen=qe_cut, include_ratio=False)
        
        make_generator_ratio_comp("plots/"+det+"_"+flux+"_H2O_EnuQEabsbias_gencomp_threshold.pdf", inFileList, inFileList, nameList, colzList, lineList, \
                                  mod_enuqe+" - Enu_true", "70,-0.9,0.5", pion_qe_cut, norm="xsec", \
                                  labels="E_{#nu}^{rec, QE} - E_{#nu}^{true} (GeV); #frac{CC0(#pi >100 MeV)}{CC0#pi}", lineStyle="][", \
                                  legDim=[0.62, 0.5, 0.82, 0.93], yLimits=[1, None], yRatLimits=[0,2.2], cutDen=qe_cut, include_ratio=False)
        
        
if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    make_T2K_erec_threshold_plots(inputDir)

