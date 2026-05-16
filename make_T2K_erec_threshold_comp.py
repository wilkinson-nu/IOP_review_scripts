from plotting_functions import make_generator_ratio_comp
import argparse

def make_T2K_erec_threshold_comp(inputDir="inputs/", flux="FHC_numu", outdir="plots"):

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
    
    ## QE reco
    qe_cut = "cc==1 && Sum$( (abs(pdg)>100) * (abs(pdg)<2000) )==0 && Sum$( (abs(pdg)>2300) * (abs(pdg)<100000) )==0"

    ## Special pion < 100 MeV cut
    base_qe_cut = "cc==1 && Sum$(abs(pdg)==111)==0 && Sum$( (abs(pdg)>111) * (abs(pdg)<211) )==0 && Sum$( (abs(pdg)>211) * (abs(pdg)<2000) )==0 && Sum$( (abs(pdg)>2300) * (abs(pdg)<100000) )==0"
    pion_qe_cut = base_qe_cut + "&& Sum$( (abs(pdg)==211) * ((E - 0.1395703918)>0.100) )==0"
    
    ## Loop over configs
    det = "T2KSK_osc"
    targ = "H2O"

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
    
    make_generator_ratio_comp(outdir+"/"+det+"_"+flux+"_H2O_EnuQEbias_gencomp_threshold.pdf", inFileList, inFileList, nameList, colzList, lineList, \
                              "("+mod_enuqe+" - Enu_true)/Enu_true", "70,-0.9,0.5", pion_qe_cut, norm="xsec", \
                              labels="(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; #frac{CC0(#pi >100 MeV)}{CC0#pi}", lineStyle="][", \
                              legDim=[0.62, 0.3, 0.82, 0.93], yLimits=[1, None], yRatLimits=[0,2.2], cutDen=qe_cut, include_ratio=False)
    
    make_generator_ratio_comp(outdir+"/"+det+"_"+flux+"_H2O_EnuQEabsbias_gencomp_threshold.pdf", inFileList, inFileList, nameList, colzList, lineList, \
                              mod_enuqe+" - Enu_true", "70,-0.9,0.5", pion_qe_cut, norm="xsec", \
                              labels="E_{#nu}^{rec, QE} - E_{#nu}^{true} (GeV); #frac{CC0(#pi >100 MeV)}{CC0#pi}", lineStyle="][", \
                              legDim=[0.62, 0.3, 0.82, 0.93], yLimits=[1, None], yRatLimits=[0,2.2], cutDen=qe_cut, include_ratio=False)
    
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("make_T2K_erec_threshold_comp")
    
    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--flux',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))
    
    make_T2K_erec_threshold_comp(args.input,
                                 args.flux,
                                 outdir=args.output)
    
