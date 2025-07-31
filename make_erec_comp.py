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

def make_T2K_erec_plots(inputDir="inputs/"):

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
    qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"

    ## Special pion < 100 MeV cut
    base_qe_cut = "cc==1 && Sum$(abs(pdg) == 111)==0 && Sum$(abs(pdg)>111 && abs(pdg) < 211)==0 && Sum$(abs(pdg)>211 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
    pion_qe_cut = base_qe_cut + "&& Sum$(abs(pdg)==211 && (E - 0.1395703918)>0.100)==0"

    
    ## Loop over configs
    for det in ["T2KND", "T2KSK_osc"]:
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
            targ = "H2O"
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                          ]
            
            make_generator_comp("plots/"+det+"_"+flux+"_H2O_EnuQE_gencomp.pdf", inFileList, nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
                                "E_{#nu}^{rec, QE} (GeV); d#sigma/dE_{#nu}^{rec, QE} (#times 10^{-38} cm^{2}/nucleon)")

            make_generator_comp("plots/"+det+"_"+flux+"_H2O_EnuQEbias_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+mod_enuqe+" - Enu_true)/Enu_true", "60,-0.9,0.5", qe_cut, \
                                "(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.5, 0.42, 0.93], yRatLimits=[0,2.2])

            make_generator_comp("plots/"+det+"_"+flux+"_H2O_EnuQEabsbias_gencomp.pdf", inFileList, nameList, colzList, lineList, mod_enuqe+" - Enu_true", "60,-0.9,0.5", qe_cut, \
				"E_{#nu}^{rec, QE} - E_{#nu}^{true} (GeV); Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.5, 0.42, 0.93], yRatLimits=[0,2.2])

            ## Add a pion cut
            if det == "T2KSK_osc":
                make_generator_comp("plots/"+det+"_"+flux+"_H2O_EnuQEbias_gencomp_pion100MeV.pdf", inFileList, nameList, colzList, lineList, "("+mod_enuqe+" - Enu_true)/Enu_true", "60,-0.9,0.5", pion_qe_cut, \
                                    "(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.5, 0.42, 0.93], yRatLimits=[0,2.2])
                
                make_generator_comp("plots/"+det+"_"+flux+"_H2O_EnuQEabsbias_gencomp_pion100MeV.pdf", inFileList, nameList, colzList, lineList, mod_enuqe+" - Enu_true", "60,-0.9,0.5", pion_qe_cut, \
                                    "E_{#nu}^{rec, QE} - E_{#nu}^{true} (GeV); Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.5, 0.42, 0.93], yRatLimits=[0,2.2])
                
            
def make_DUNE_erec_plots(inputDir="inputs/"):


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
    ehad_cut = "cc==1"
    enuhad = "ELep + Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"

    ## Loop over configs
    for det in ["DUNEND", "DUNEFD_osc"]:
        for flux in ["FHC_numu", "RHC_numubar"]:
            ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
            targ = "Ar40"
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                          ]
            
            make_generator_comp("plots/"+det+"_"+flux+"_Ar40_Enurec_gencomp.pdf", inFileList, nameList, colzList, lineList, enuhad, "80,0,8", ehad_cut, \
                                "E_{#nu}^{rec, had} (GeV); d#sigma/dE_{#nu}^{rec, had} (#times 10^{-38} cm^{2}/nucleon)")

            make_generator_comp("plots/"+det+"_"+flux+"_Ar40_Enurecbias_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+enuhad+" - Enu_true)/Enu_true", "60,-0.5,0.1", ehad_cut, \
                                "(E_{#nu}^{rec, had} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.",  [0.25, 0.5, 0.45, 0.93], yRatLimits=[0,2.2], norm="shape", lineStyle="][")

            make_generator_comp("plots/"+det+"_"+flux+"_Ar40_Enurecabsbias_gencomp.pdf", inFileList, nameList, colzList, lineList, enuhad+" - Enu_true", "60,-0.5,0.1", ehad_cut, \
                                "E_{#nu}^{rec, had} - E_{#nu}^{true} (GeV); Arb. norm.",  [0.25, 0.5, 0.45, 0.93], yRatLimits=[0,2.2], norm="shape", lineStyle="][")


if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    # inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    make_T2K_erec_plots(inputDir)
    make_DUNE_erec_plots(inputDir)

