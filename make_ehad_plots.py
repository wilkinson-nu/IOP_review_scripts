import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_generator_comp, make_breakdown_comp, get_chain
## def make_generator_comp(outPlotName, inFileList, nameList, colzList, \
##                         plotVar="q0", binning="100,0,5", cut="cc==1", \
##                         labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
##                         legDim=[0.65, 0.5, 0.85, 0.93], ratLimits=[0.4, 1.6], maxVal=None, isShape=False)


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

## Use double precision for TTree draw
gEnv.SetValue("Hist.Precision.1D", "double")
gEnv.SetValue("Hist.Precision.2D", "double")

gStyle.SetNumberContours(255)
gStyle.SetPalette(57)


ccinc = "cc==1"
cc0pi = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
# ehad = "Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + Sum$((abs(pdg)==2212)*(E - 0.938))"
ehad = "Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"

def make_2D_hist(inFileNames, labels, xVar, yVar, xBins, yBins, cut_string):

    ## Modify to use glob                                                                                                                                                                                          
    inTree, inFlux, inEvt, nFiles, norm = get_chain(inFileNames)
    inTree .Draw(yVar+":"+xVar+">>this_hist("+xBins+","+yBins+")", str(norm)+"*fScaleFactor*InputWeight*1E38*("+cut_string+")")
    inHist = gDirectory.Get("this_hist")
    inHist .SetDirectory(0)
    inHist .SetNameTitle("this_hist", "this_hist;"+labels)

    return inHist

def make_2D_plot(outPlotName, inFileNames, xVar, yVar, xBins, yBins, cut_string, \
                    labels, isLog=False):

    inHist = make_2D_hist(inFileNames, labels, xVar, yVar, xBins, yBins, cut_string)
    maxVal = inHist.GetMaximum()*1.1
    
    can = TCanvas("can", "can", 800, 800)
    can .cd()

    can    .cd()
    inHist .Draw("COLZ")
    inHist .GetZaxis().RotateTitle(1)
    inHist .GetZaxis().SetTitleOffset(1.6)
    gPad   .SetTopMargin(0.05)
    gPad   .SetRightMargin(0.22)
    gPad   .SetLeftMargin(0.17)
    gPad   .SetBottomMargin(0.15)
    gPad   .Update()
    if isLog:
        gPad .SetLogz(1)
        inHist .SetMaximum(0.5)
        inHist .SetMinimum(1E-5)
    can    .SaveAs(outPlotName)
    gPad .SetLogz(0)


def make_q0_plots(inputDir="inputs/"):

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

    ## DUNE plots
    det   = "DUNEND"
    targ  = "Ar40"
    for flux in ["FHC_numu", "RHC_numubar"]:
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_q0_gencomp.pdf", inFileList, nameList, colzList, lineList, "q0", "60,0,3", ccinc, \
                            "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/GeV/nucleon)", [0.65, 0.45, 0.85, 0.93])

    ## Now T2K
    det   = "T2KND"
    targ  = "H2O"
    for flux in ["FHC_numu", "RHC_numubar"]:
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_q0_gencomp.pdf", inFileList, nameList, colzList, lineList, "q0", "50,0,1", cc0pi, \
                            "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/GeV/nucleon)", [0.65, 0.45, 0.85, 0.93])


def make_ehad_plots(inputDir="inputs/"):

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
    
    ## DUNE plots
    det   = "DUNEND"
    targ  = "Ar40"
    for flux in ["FHC_numu", "RHC_numubar"]:
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_ehad_gencomp.pdf", inFileList, nameList, colzList, ehad, "100,0,2", ccinc, \
        #                    "E_{had} (GeV); d#sigma/dE_{had} (#times 10^{-38} cm^{2}/GeV/nucleon)")
                
        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_ehadoverq0_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+ehad+")/q0", "60,0,1.1", ccinc, \
                            "E_{had}^{rec}/q_{0}; d#sigma/d(E_{had}^{rec}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.2, 0.3, 0.45, 0.93], [0, None], [0,2.2])

        #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_eavoverq0_gencomp.pdf", inFileList, nameList, colzList, "(Eav)/q0", "220,0,1.1", ccinc, \
        #                    "E_{avail}/q_{0}; d#sigma/d(E_{avail}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93], [0, None], [0,2.2])


    ## Now T2K
    det   = "T2KND"
    targ  = "H2O"
    for flux in ["FHC_numu", "RHC_numubar"]:
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                      ]

        #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_ehad_gencomp.pdf", inFileList, nameList, colzList, ehad, "100,0,1", cc0pi, \
        #                    "E_{had} (GeV); d#sigma/dE_{had} (#times 10^{-38} cm^{2}/GeV/nucleon)")

        make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_ehadoverq0_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+ehad+")/q0", "60,0,1.2", cc0pi, \
                            "E_{had}^{rec}/q_{0}; d#sigma/d(E_{had}^{rec}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.2, 0.3, 0.45, 0.93], [0, None], [0,2.2])

        #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_eavoverq0_gencomp.pdf", inFileList, nameList, colzList, "(Eav)/q0", "120,0,1.2", cc0pi, \
        #                    "E_{avail}/q_{0}; d#sigma/d(E_{avail}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93], [0, None], [0,2.2])

        
def make_ehad_breakdown_plots(inputDir="inputs/"):
    cc0pi = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0 && Sum$(pdg==2212) > 0"
    
    nameList = ["CC-INC",\
                "CC-1p1h",\
		"CC-2p2h",\
                "CC-RPP",\
                "CC-SIS",\
                "CC-DIS"]
    colzList = [9000, 9001, 9002, 9003, 9006, 9005]
    cutList = ["cc==1", \
	       "cc==1 && abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
	       "cc==1 && abs(Mode) == 2", \
               "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
               "cc==1 && abs(Mode)==21",\
	       "cc==1 && abs(Mode)==26"]

    cc0pi_cutList = [cc0pi, \
                     cc0pi+"&& abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
                     cc0pi+"&& abs(Mode) == 2", \
                     cc0pi+"&& (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
	             cc0pi+"&& abs(Mode)==21",\
                     cc0pi+"&& abs(Mode)==26"]
    
    ## DUNE plots
    det   = "DUNEND"
    targ  = "Ar40"
    for flux in ["FHC_numu", "RHC_numubar"]:
    
        ## Make some breakdowns
        for generator in ["NEUT562", "GENIEv3_G18_10a_00_000"]:

            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          ]
            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_ehad_"+generator+".pdf", inFileList, nameList, colzList, ehad, "100,0,2", cutList, \
                                "E_{had} (GeV); d#sigma/dE_{had} (#times 10^{-38} cm^{2}/GeV/nucleon)")

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_ehadoverq0_"+generator+".pdf", inFileList, nameList, colzList, "("+ehad+")/q0", "124,0.79,1.1", cutList, \
                                "E_{had}^{rec}/q_{0}; d#sigma/d(E_{had}^{rec}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93])

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_eavoverq0_"+generator+".pdf", inFileList, nameList, colzList, "(Eav)/q0", "124,0.79,1.1", cutList, \
                                "E_{avail}/q_{0}; d#sigma/d(E_{avail}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93])


    det   = "T2KND"
    targ  = "H2O"
    for flux in ["FHC_numu", "RHC_numubar"]:
        for generator in ["NEUT562", "GENIEv3_G18_10a_00_000"]:
            
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root",\
                          ]

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_ehad_"+generator+".pdf", inFileList, nameList, colzList, ehad, "100,0,1", cc0pi_cutList, \
                                "E_{had} (GeV); d#sigma/dE_{had} (#times 10^{-38} cm^{2}/GeV/nucleon)")

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_ehadoverq0_"+generator+".pdf", inFileList, nameList, colzList, "("+ehad+")/q0", "120,0,1.2", cc0pi_cutList, \
                                "E_{had}^{rec}/q_{0}; d#sigma/d(E_{had}^{rec}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93])

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_eavoverq0_"+generator+".pdf", inFileList, nameList, colzList, "(Eav)/q0", "120,0,1.2", cc0pi_cutList, \
                                "E_{avail}/q_{0}; d#sigma/d(E_{avail}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.25, 0.5, 0.45, 0.93])

def make_q0_vs_ehad(inputDir):
    
    for generator in ["GiBUU", "NEUTDCC", "NUWROv25.3.1", "NEUT580", "GENIEv3_G18_10a_00_000", \
                      "GENIEv3_G18_10b_00_000", "GENIEv3_G18_10c_00_000", "GENIEv3_G18_10d_00_000", \
                      "GENIEv3_CRPA21_04a_00_000", "GENIEv3_G21_11a_00_000", "NUWRO_LFGRPA"]:


        det   = "DUNEND"
        targ  = "Ar40"
        for flux in ["FHC_numu", "RHC_numubar"]:

            inFileNames=inputDir+"/"+det+"_"+flux+"_"+targ+"_"+generator+"_1M_*_NUISFLAT.root"

            xVar = "q0"
            yVar =  ehad
            
            xBins = "100,0,5"
            yBins = "100,0,5"
            labels = "q_{0} (GeV); E_{had} (GeV); Arb. units."
            make_2D_plot("plots/"+det+"_"+flux+"_"+targ+"_"+generator+"_q0_vs_ehad.png", \
                         inFileNames, xVar, yVar, xBins, yBins, ccinc, labels, True)
        
if __name__ == "__main__":
    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    # inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    make_q0_plots(inputDir)
    make_ehad_plots(inputDir)
    make_q0_vs_ehad(inputDir)
    # make_ehad_breakdown_plots(inputDir)
    
