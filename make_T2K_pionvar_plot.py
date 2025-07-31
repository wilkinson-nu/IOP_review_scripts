import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_breakdown_comp

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


def make_pionvar_plots(inputDir, model):

    nameList = ["K.E. > 0 MeV",\
                "K.E. > 25 MeV",\
                "K.E. > 50 MeV",\
                "K.E. > 75 MeV",\
                "K.E. > 100 MeV"]
    colzList = [9000, 9005, 9002, 9003, 9004, 9005]
    lineList = [7, 1, 1, 1, 1, 1]

    targ = "H2O"
    base_qe_cut = "cc==1 && Sum$(abs(pdg) == 111)==0 && Sum$(abs(pdg)>111 && abs(pdg) < 211)==0 && Sum$(abs(pdg)>211 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"

    ekpi_cut_list = [base_qe_cut + "&& Sum$(abs(pdg)==211)==0",\
                     base_qe_cut + "&& Sum$(abs(pdg)==211 && (E - 0.1395703918)>0.025)==0",\
                     base_qe_cut + "&& Sum$(abs(pdg)==211 && (E - 0.1395703918)>0.050)==0",\
                     base_qe_cut + "&& Sum$(abs(pdg)==211 && (E - 0.1395703918)>0.075)==0",\
                     base_qe_cut + "&& Sum$(abs(pdg)==211 && (E - 0.1395703918)>0.100)==0"]

    det="T2KSK_osc"
    flux="FHC_numu"
    flux_string = "#nu_{#mu}"
    if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"	

    inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]
    
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
        
    make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_"+model+"_EnuQEbias_pionKEcomp.pdf", inFileList, "#pi^{#pm} threshold", \
                        nameList, colzList, lineList, "("+mod_enuqe+" - Enu_true)/Enu_true", "70,-0.9,0.5", ekpi_cut_list, \
                        "(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.", legDim=[0.22, 0.5, 0.42, 0.93], rat_title_num="Alt. threshold",
                        yRatLimits=[1,1.9], lineStyle="][")
    
            
if __name__ == "__main__":
                
    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"

    for model in ["GiBUU", "NEUTDCC", "NUWROv25.3.1", "NEUT580", "GENIEv3_G18_10a_00_000", \
                  "GENIEv3_G18_10b_00_000", "GENIEv3_G18_10c_00_000", "GENIEv3_G18_10d_00_000", \
                  "GENIEv3_CRPA21_04a_00_000", "GENIEv3_G21_11a_00_000", "NUWRO_LFGRPA"]:

        make_pionvar_plots(inputDir, model)
 
    
