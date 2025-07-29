import ROOT
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory
from glob import glob

from plotting_functions import make_generator_comp
## def make_generator_comp(outPlotName, inFileList, nameList, colzList, \
## 			plotVar="q0", binning="100,0,5", cut="cc==1", \
##                         labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", \
##                         legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], \
##   			isShape=False, withRebin=True, isLog=False, include_ratio=True, rat_title_num="Model"):
    
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

def make_DUNE_Ekin_plots(inputDir="inputs/"):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro",\
                "GiBUU"\
                ]
    colzList = [9000, 9001, 9003, 9004, 9006, 9005, ROOT.kBlack]
    
    ## Ekin cut
    ekin = "E - sqrt(E*E - px*px - py*py - pz*pz)"

    mom = "sqrt(px*px - py*py - pz*pz)"
    
    ## Loop over configs
    for det in ["DUNEND", "DUNEFD_osc"]:

        targ = "Ar40"
        if det == "T2KND": targ="H2O"
        
        for flux in ["FHC_numu", "RHC_numubar"]:
            
            for pdg in [2112]: #[211, -211]: #[2212, -211, 211]: #211, -211, 13, -13, 2212, 11, -11, 111, 22, 321, -321, 311]:
                
                pdg_cut = "pdg=="+str(pdg)
                
                ## K0 is a special case
                if pdg == 311: pdg_cut = "(pdg==311|pdg==130|pdg==310)"
                
                ## These files can be found here (no login required): https://portal.nersc.gov/project/dune/data/2x2/simulation
                inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                              inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                              ]
                
                #make_generator_comp(det+"_"+flux+"_"+targ+"_"+str(pdg)+"_mom_gencomp.png", inFileList, nameList, colzList, mom, "100,0,1", pdg_cut, \
                #                    "p (GeV/c); d#sigma/dp (#times 10^{-38} cm^{2}/nucleon)")

                make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_ekin_CCall_gencomp.png", inFileList, nameList, colzList, ekin, "65,0,0.65", pdg_cut+"&&cc==1", \
                                    "E_{k} (GeV); d#sigma/dE_{k} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False)
                #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_ekin_CCall_gencomp_logy.png", inFileList, nameList, colzList, ekin, "65,0,0.65", pdg_cut+"&&cc==1", \
                #                    "E_{k} (GeV); d#sigma/dE_{k} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False, isLog=True)
                make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_ekin_CCleading_gencomp.png", inFileList, nameList, colzList, ekin, "65,0,0.65", pdg_cut + "&&pdg_rank==0&&cc==1", \
                                    "E_{k} (GeV); d#sigma/dE_{k} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False)
                #make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_ekin_CCleading_gencomp_logy.png", inFileList, nameList, colzList, ekin, "65,0,0.65", pdg_cut + "&&pdg_rank==0 &&cc==1", \
                #                    "E_{k} (GeV); d#sigma/dE_{k} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False, isLog=True)
                make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_n2112cc_gencomp.png", inFileList, nameList, colzList, "Sum$(pdg=="+str(pdg)+")", "10,0,10", "cc==1", \
                                    "N. neutron; d#sigma/dN (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False)

                ## make_generator_comp("plots/"+det+"_"+flux+"_"+targ+"_"+str(pdg)+"_ekin_gencomp.png", inFileList, nameList, colzList, ekin, "50,0,2", "cc==1 &&"+pdg_cut, \
                ##                     "E_{k} (GeV); d#sigma/dE_{k} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.6, 0.5, 0.85, 0.93], include_ratio=False) 
            
            
if __name__ == "__main__":

    inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    make_DUNE_Ekin_plots(inputDir)

#  LocalWords:  numubar
