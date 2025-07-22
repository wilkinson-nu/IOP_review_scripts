import ROOT
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory
from glob import glob

from plotting_functions import make_generator_comp

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

# evt_cut = "Sum$(abs(pdg)==411 || abs(pdg)==421 || abs(pdg)==431 || abs(pdg)==3122 || abs(pdg)==3212 || abs(pdg)==3222 || abs(pdg)==3112)==0"

not_h_cut = "tgta != 1 && tgt != 1000010010"

def make_multiplicity_plots(inputDir="inputs/"):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]
    
    ## Loop over configs
    for det in ["DUNEND", "T2KND"]: #"DUNEFD_osc"]:

        targ = "Ar40"
        if det == "T2KND": targ="H2O"
        
        for flux in ["FHC_numu", "RHC_numubar"]:
            
            ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                          ]
            
            for pdg in [2212, -211, 211, 2112, 11, -11, 111, 22, 321, -321, 311, -13, 13]:
                npdg_var = "Sum$(pdg=="+str(pdg)+")"
                make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_n"+str(pdg)+"_gencomp.png", inFileList, nameList, colzList, npdg_var, "10,0,10", not_h_cut, \
                                    "N(pdg == "+str(pdg)+"); d#sigma/dN (#times 10^{-38} cm^{2}/nucleon)", withRebin=False, isLog=True)

            nabove_var  = "Sum$(pdg==2212 && sqrt(px*px+py*py+pz*pz)>0.1)"
            nbelow_var  = "Sum$(pdg==2212 && sqrt(px*px+py*py+pz*pz)<0.1)"
            pabove_var  = "Sum$((pdg==2212 && sqrt(px*px+py*py+pz*pz)>0.1)*sqrt(px*px+py*py+pz*pz))"
            pbelow_var  = "Sum$((pdg==2212 && sqrt(px*px+py*py+pz*pz)<0.1)*sqrt(px*px+py*py+pz*pz))"

            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_n2212above_gencomp.png", inFileList, nameList, colzList, nabove_var, "10,0,10", not_h_cut, \
                                "N. protons (p > 0.1 GeV); d#sigma/dN (#times 10^{-38} cm^{2}/nucleon)", withRebin=False, isLog=True)
            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_n2212below_gencomp.png", inFileList, nameList, colzList, nbelow_var, "10,0,10", not_h_cut,
                                "N. protons (p < 0.1 GeV); d#sigma/dN (#times 10^{-38} cm^{2}/nucleon)", withRebin=False, isLog=True)
            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_sumpbelow_gencomp.png", inFileList, nameList, colzList, pbelow_var, "50,0,2", not_h_cut,
                                "#Sigma |p_{pr}| (GeV); d#sigma/d(#Sigma |p_{pr}|) (#times 10^{-38} cm^{2}/nucleon)", withRebin=False, isLog=True)
            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_sumpabove_gencomp.png", inFileList, nameList, colzList, pabove_var, "50,0,2", not_h_cut,
				"#Sigma |p_{pr}| (GeV); d#sigma/d(#Sigma |p_{pr}|) (#times 10^{-38} cm^{2}/nucleon)", withRebin=False, isLog=True)            


                
def make_mom_plots(inputDir="inputs/"):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]
    
    ## Ekin cut
    ekin = "E - sqrt(E*E - px*px - py*py - pz*pz)"

    mom = "sqrt(px*px+py*py+pz*pz)"
    
    ## Loop over configs
    for det in ["DUNEND", "T2KND"]: #"DUNEFD_osc"]:

        targ = "Ar40"
        if det == "T2KND": targ="H2O"
        
        for flux in ["FHC_numu", "RHC_numubar"]:
            
            for pdg in [2212, -211, 211, 111]: #211, -211, 13, -13, 2212, 11, -11, 111, 22, 321, -321, 311]:
                
                pdg_cut = "pdg=="+str(pdg)
                
                ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
                inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                              ]
                
                make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_mom_gencomp.png", inFileList, nameList, colzList, mom, "100,0,1", not_h_cut+"&&"+pdg_cut, \
                                    "p (GeV/c); d#sigma/dp (#times 10^{-38} cm^{2}/nucleon)")


def make_EM_plots(inputDir="inputs/"):

    nameList = ["GENIE 10a",\
		"GENIE 10b",\
		"GENIE 10c",\
		"CRPA",\
		"SuSAv2",\
		"NEUT",\
		"NuWro"\
		]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]

    ## Ekin cut                                                                                                                                                                          
    ekin = "E - sqrt(E*E - px*px - py*py - pz*pz)"

    mom = "sqrt(px*px - py*py - pz*pz)"
    
    sumE = "Sum$((pdg==22 || abs(pdg)==11)*E)"

    for det in ["DUNEND", "T2KND"]: #"DUNEFD_osc"]:                                                                                                                                     

	targ = "Ar40"
        if det == "T2KND": targ="H2O"

	for flux in ["FHC_numu", "RHC_numubar"]:

	    ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation                                                          
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                          ]
            
	    make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_epm_E_gencomp.png", inFileList, nameList, colzList, "E", "60,0,1.2", not_h_cut+"&& abs(pdg)==11",\
                                "E (GeV); d#sigma/dE (#times 10^{-38} cm^{2}/nucleon)")

            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_gamma_E_gencomp.png", inFileList, nameList, colzList, "E", "60,0,1.2", not_h_cut+"&& abs(pdg)==22",\
                                "E (GeV); d#sigma/dE (#times 10^{-38} cm^{2}/nucleon)", isLog=True)

            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_EM_sumE_gencomp.png", inFileList, nameList, colzList, sumE, "50,0,2", not_h_cut,
                                "Total EM energy (GeV); d#sigma/d#Sigma E (#times 10^{-38} cm^{2}/nucleon)", isLog=True)

            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_EM_Eoverq0_gencomp.png", inFileList, nameList, colzList, sumE+"/q0", "60,0,1.2", not_h_cut,
                                "Total EM energy/q_{0}; d#sigma/d(#Sigma E/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", isLog=True)



                
def make_photon_sumE(inputDir="inputs/"):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]
    
    ## Ekin cut
    sumE = "Sum$((pdg==22)*E)"
    
    ## Loop over configs
    for det in ["DUNEND", "T2KND"]: #"DUNEFD_osc"]:

        targ = "Ar40"
        if det == "T2KND": targ="H2O"
        
        for flux in ["FHC_numu", "RHC_numubar"]:

            ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
            inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                          inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                          ]
            
            make_generator_comp("omnifold_plots/"+det+"_"+flux+"_"+targ+"_sumEgamma_gencomp.png", inFileList, nameList, colzList, sumE, "100,0,1", not_h_cut, \
                                "#Sigma E_{#gamma} (GeV); d#sigma/d(#sigmaE_{#gamma}) (#times 10^{-38} cm^{2}/nucleon)", isLog=True)
            


                
            
if __name__ == "__main__":

    inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    make_mom_plots(inputDir)
    make_photon_sumE(inputDir)
    make_multiplicity_plots(inputDir)
    make_EM_plots(inputDir)
