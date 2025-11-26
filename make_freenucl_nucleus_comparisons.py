import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

from plotting_functions import make_breakdown_comp

def make_q0_breakdown_CC_DUNE(inputDir="inputs/", model="GENIEv3_G18_10a_00_000"):

    nameList = ["CCINC",\
                "CCQE",\
                "CC2p2h",\
                "CCRPP",\
                "CCSIS",\
                "CCDIS"]
    colzList = [9000, 9005, 9002, 9003, 9001, 9004]
    lineList = [7, 1, 1, 1, 1, 1]
    cutList = ["cc==1", \
	       "cc==1 && abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
               "cc==1 && abs(Mode) == 2", \
               "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
               "cc==1 && abs(Mode)==21",\
               "cc==1 && abs(Mode)==26"]
    targ = "Ar40"
    binning="50,0,2.5"

    var_list=["q0", "q0", "q0", "q0", "q0", "q0"]
    
    ## DUNE ND
    det = "DUNEND"
    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"	
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]
        
        make_breakdown_comp("plots/"+det+"_"+flux+"_Ar40_CC_"+model+"_q0_noratio.pdf", inFileList, flux_string+"-^{40}Ar", \
                            nameList, colzList, lineList, "q0", binning, cutList, \
                            "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", include_ratio=False, legDim=[0.7, 0.45, 0.9, 0.93])
        
def make_W_breakdown_CC_DUNE(inputDir="inputs/"):

    nameList = ["CCINC",\
                "CCQE",\
                "CC2p2h",\
		"CCRPP",\
                "CCSIS",\
                "CCDIS"]
    colzList = [9000, 9005, 9002, 9003, 9001, 9004]
    lineList = [7, 1, 1, 1, 1, 1]
    cutList = ["cc==1", \
	       "cc==1 && abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
	       "cc==1 && abs(Mode) == 2", \
	       "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
	       "cc==1 && abs(Mode)==21",\
               "cc==1 && abs(Mode)==26"]
    targ = "Ar40"
    binning="80,0,4"

    var_list=["W", "W", "W", "W", "W", "W"]

    det = "DUNEND"
    model="GENIEv3_G18_10a_00_000"
    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"
        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]

        make_generator_comp_noratio(det+"_"+flux+"_Ar40_CC_"+model+"_W_noratio.pdf", inFileList, flux_string+"-^{40}Ar", \
                                    nameList, colzList, lineList, var_list, binning, cutList, \
                                    "W (GeV); d#sigma/dW (#times 10^{-38} cm^{2}/nucleon)", False)

        
def make_q0_breakdown_NC_DUNE(inputDir="inputs/"):

    nameList = ["NCINC", \
                "NCEL", \
                "NC2p2h", \
                "NCRPP", \
                "NCDIS"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9005]
    lineList = [1, 1, 1, 1, 1]
    cutList = ["cc==0", \
               "cc==0 && (abs(Mode)==51 || abs(Mode)==52)",\
               "cc==0 && abs(Mode)==53",\
               "cc==0 && (abs(Mode)==31 || abs(Mode)==32 || abs(Mode)==33 || abs(Mode)==34)",\
               "cc==0 && (abs(Mode)==41 || abs(Mode)==46)"\
               ]
    targ = "Ar40"
    binning="100,0,2.5"

    var_list=["q0", "q0", "q0", "q0", "q0"]

    ## DUNE ND
    det = "DUNEND"
    model="GENIEv3_G18_10a_00_000"
    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"

        inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                      inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"\
                      ]

        make_generator_comp_noratio(det+"_"+flux+"_Ar40_NC_"+model+"_q0_noratio.pdf", inFileList, flux_string+"-^{40}Ar",
                                    nameList, colzList, lineList, var_list, binning, cutList, \
                                    "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", False)
        
def make_W_breakdown_CC_nucl(inputDir="inputs/", model="GENIEv3_G18_10a_00_000"):

    nameList = ["CCINC",\
	        "CCQE",\
	        "CCRPP",\
                "CCDIS"]
    colzList = [9000, 9001,9003, 9005]
    lineList = [1, 1, 1, 1, 1]
    cutList = ["cc==1", \
               "cc==1 && abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
               "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
               "cc==1 && (abs(Mode)==21 || abs(Mode) == 26)"]
    binning="80,0,4"
    det = "DUNEND"

    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string = "#bar{#nu}_{#mu}"
        
        for targ in ["proton"]:
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_CC_"+model+"_W_noratio.pdf", inFileList, flux_string+"-"+str(targ), \
                            nameList, colzList, lineList, "W", binning, cutList, \
                            "W (GeV); d#sigma/dW (#times 10^{-38} cm^{2}/nucleon)", include_ratio=False, legDim=[0.7, 0.45, 0.9, 0.93])


def make_q0_breakdown_CC_nucl(inputDir="inputs/", model="GENIEv3_G18_10a_00_000"):

    nameList = ["CCINC",\
                "CCQE",\
		"CCRPP",\
                "CCSIS",\
                "CCDIS"]
    colzList = [9000, 9005, 9003, 9001, 9004]
    lineList = [7, 1, 1, 1, 1]
    cutList = ["cc==1", \
               "cc==1 && abs(Mode) == 1 && Sum$(abs(pdg) > 3000 && abs(pdg) < 5000)==0", \
               "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
               "cc==1 && abs(Mode)==21", \
               "cc==1 && abs(Mode)==26"]
    binning="50,0,2.5"
    det = "DUNEND"

    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"

        for targ in ["proton"]:
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_CC_"+model+"_q0_noratio.pdf", inFileList, flux_string+"-"+str(targ), \
                            nameList, colzList, lineList, "q0", binning, cutList, \
                            "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", include_ratio=False, legDim=[0.7, 0.45, 0.9, 0.93])

            
def make_q0_breakdown_NC_nucl(inputDir="inputs/"):

    nameList = ["NCINC", \
                "NCEL", \
                "NCRPP", \
                "NCDIS"\
		]
    colzList = [9000, 9001, 9003, 9005]
    lineList = [1, 1, 1, 1, 1]
    cutList = ["cc==0", \
               "cc==0 && (abs(Mode)==51 || abs(Mode)==52)",\
               "cc==0 && (abs(Mode)==31 || abs(Mode)==32 || abs(Mode)==33 || abs(Mode)==34)",\
	       "cc==0 && (abs(Mode)==41 || abs(Mode)==46)"\
	       ]
    binning="100,0,2.5"
    var_list=["q0", "q0", "q0", "q0", "q0"]
    det = "DUNEND"
    model="GENIEv3_G18_10a_00_000"
    
    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"
        
        for targ in ["neutron", "proton"]:
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"\
                          ]

            make_generator_comp_noratio(det+"_"+flux+"_"+targ+"_NC_"+model+"_q0_noratio.pdf", inFileList, flux_string+"-"+str(targ), \
                                        nameList, colzList, lineList, var_list, binning, cutList, \
                                        "q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", False)

def make_Enu_breakdown_CC_nucl(inputDir="inputs/", model="GENIEv3_G18_10a_00_000"):

    nameList = ["CCINC",\
                "CCQE",\
                "CCRPP",\
		"CCDIS"]
    colzList = [9000, 9001,9003, 9005]
    lineList = [1, 1, 1, 1, 1]
    cutList = ["cc==1", \
               "cc==1 && abs(Mode) == 1", \
               "cc==1 && (abs(Mode)==11 || abs(Mode)==12 || abs(Mode)==13)", \
	       "cc==1 && (abs(Mode)==21 || abs(Mode) == 26)"]
    binning="40,0,8"
    det = "DUNEND"

    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"

        for targ in ["proton"]:
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"]

            make_breakdown_comp("plots/"+det+"_"+flux+"_"+targ+"_CC_"+model+"_Enu_noratio.pdf", inFileList, flux_string+"-"+str(targ), \
                                nameList, colzList, lineList, "Enu_true", binning, cutList, \
                                "E_{#nu} (GeV); d#sigma/dE_{#nu} (#times 10^{-38} cm^{2}/nucleon)", include_ratio=False, legDim=[0.7, 0.45, 0.9, 0.93])

def make_Enu_breakdown_NC_nucl(inputDir="inputs/"):

    nameList = ["NCINC", \
                "NCEL", \
                "NCRPP", \
                "NCDIS"\
                ]
    colzList = [9000, 9001, 9003, 9005]
    lineList = [1, 1, 1, 1, 1]
    cutList = ["cc==0", \
               "cc==0 && (abs(Mode)==51 || abs(Mode)==52)",\
               "cc==0 && (abs(Mode)==31 || abs(Mode)==32 || abs(Mode)==33 || abs(Mode)==34)",\
               "cc==0 && (abs(Mode)==41 || abs(Mode)==46)"\
               ]
    binning="80,0,4"
    var_list=["Enu_true", "Enu_true", "Enu_true", "Enu_true", "Enu_true"]
    det = "DUNEND"
    model="GENIEv3_G18_10a_00_000"

    for flux in ["FHC_numu", "RHC_numubar"]:
        flux_string = "#nu_{#mu}"
        if flux == "RHC_numubar": flux_string =	"#bar{#nu}_{#mu}"
        
        for targ in ["neutron", "proton"]:

            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_"+model+"_1M_*_NUISFLAT.root"\
                          ]

            make_generator_comp_noratio(det+"_"+flux+"_"+targ+"_NC_"+model+"_Enu_noratio.pdf", inFileList, flux_string+"-"+str(targ), \
                                        nameList, colzList, lineList, var_list, binning, cutList, \
					"E_{#nu} (GeV); d#sigma/dE_{#nu} (#times 10^{-38} cm^{2}/nucleon)", False)

            
if __name__ == "__main__":

    inputDir="/pscratch/sd/c/cwilk/MC_IOP_review/*/"
    # make_q0_breakdown_CC_DUNE(inputDir)
    # make_q0_breakdown_NC_DUNE(inputDir)

    for model in ["GENIEv3_G18_10a_00_000", "NUWROv25.3.1", "NUWRO_LFGRPA", "GiBUU"]:
        make_q0_breakdown_CC_DUNE(inputDir, model)
        make_q0_breakdown_CC_nucl(inputDir, model)
        make_Enu_breakdown_CC_nucl(inputDir, model)
        make_W_breakdown_CC_nucl(inputDir, model)

    ## make_W_breakdown_CC_DUNE(inputDir)
    ## make_W_breakdown_CC_nucl(inputDir)
    
    ## make_Enu_breakdown_CC_nucl(inputDir)
    ## make_Enu_breakdown_NC_nucl(inputDir)
