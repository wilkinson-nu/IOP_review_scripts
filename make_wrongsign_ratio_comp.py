import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_ratio_comp, make_generator_comp, make_A_over_BC_comp

## Use double precision for TTree draw
gEnv.SetValue("Hist.Precision.1D", "double")

## No need to see the plots appear here
gROOT.SetBatch(1)
gStyle.SetLineWidth(3)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(4)
gStyle.SetLineStyleString(11,"40 20 40 20")
gStyle.SetLineStyleString(12,"20 10 20 10")

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

def make_SK_wrongsign_ratio_plots(inputDir="inputs/", flav="numu"):

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
    qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0 && Sum$(pdg==-2212)==0 && Sum$(pdg==-2112)==0"


    ## Change to Enu_QE to use a binding energy of 27 MeV! Not 34 like the NUISANCE default...                                                                                   
    binding = 27/1000.
    m2 = 0.93956536
    m1 = 0.93827203
    ml = 0.10565837

    if "nue" in flav: ml = 0.000511
    
    mod_enuqe = "(2*("+str(m1)+"-"+str(binding)+")*ELep -"+str(ml)+"*"+str(ml)+" + "+str(m2)+"*"+str(m2)+" - ("+str(m1)+"-"+str(binding)+")*("+str(m1)+"-"+str(binding)+"))/" \
        +"(2*(("+str(m1)+"-"+str(binding)+") - ELep + sqrt(ELep*ELep - "+str(ml)+"*"+str(ml)+")*CosLep))"

    # mod_enuqe = "Enu_QE"
    
    ## Allow hydrogen
    # qe_cut += "&& tgta != 1 && tgt != 1000010010"
    sample_label = "CC0#pi"

    ## These plots need to be RHC numu / (RHC numu + RHC numubar)    
    inFileListNu = [inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NEUT580_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NEUTDCC_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NUWROv25.3.1_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GiBUU_1M_*_NUISFLAT.root"\
                    ]

    inFileListNub = [inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GiBUU_1M_*_NUISFLAT.root"\
                     ]

    ## make_generator_comp("plots/T2KSK_osc_wrongsign_"+flav+"_EnuQE_gencomp.pdf", inFileListNu, \
    ##                     nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
    ##                     "E_{#nu}^{rec, QE} (GeV); XSEC", lineStyle="", fluxAverage=False)
    ## 
    ## make_generator_comp("plots/T2KSK_osc_wrongsign_numubar_EnuQE_gencomp.pdf", inFileListNumub, \
    ##                           nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
    ##                           "E_{#nu}^{rec, QE} (GeV); XSEC", lineStyle="", fluxAverage=False)    

    make_A_over_BC_comp("plots/T2KSK_osc_"+flav+"wrongsign_EnuQE_gencomp.pdf", inFileListNu, inFileListNub, inFileListNu, \
                        nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
                        "E_{#nu}^{rec, QE} (GeV); Wrong-sign/total", yLimits=[0,1.2], withRebin=True)

    #make_A_over_BC_comp("plots/T2KSK_osc_wrongsign_EnuQE_neutron_gencomp.pdf", inFileListNu, inFileListNub, inFileListNu, \
    #                    nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut + "&& Sum$(pdg==2112)>0", \
    #                    "E_{#nu}^{rec, QE} (GeV); Wrong-sign/total", yLimits=[0, 0.9], withRebin=True)


def make_DUNE_wrongsign_ratio_plots(inputDir="inputs/", flav="numu", legDim=[0.65, 0.5, 0.85, 0.93]):

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

    ehad_cut = "cc==1 && nfsp > 0"
    enuhad = "ELep + Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + \
    Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"



    inFileListNu = [inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NEUT580_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NEUTDCC_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GiBUU_1M_*_NUISFLAT.root"\
                    ]

    inFileListNub = [inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GiBUU_1M_*_NUISFLAT.root"\
                     ]

    make_A_over_BC_comp("plots/DUNEFD_osc_"+flav+"wrongsign_Enurec_gencomp.pdf", inFileListNu, inFileListNub, inFileListNu, \
                        nameList, colzList, lineList, enuhad, "80,0,8", ehad_cut, \
                        "E_{#nu}^{rec, had} (GeV); Wrong-sign/total", yLimits=[0,0.9], withRebin=False, legDim=legDim)

    
if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    
    make_SK_wrongsign_ratio_plots(inputDir, "numu")
    make_SK_wrongsign_ratio_plots(inputDir, "nue")

    make_DUNE_wrongsign_ratio_plots(inputDir, "numu", legDim=[0.25, 0.5, 0.45, 0.93])
    make_DUNE_wrongsign_ratio_plots(inputDir, "nue", legDim=[0.65, 0.5, 0.85, 0.93])
