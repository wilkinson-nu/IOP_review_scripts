import argparse
from plotting_functions import make_generator_comp

def make_T2K_erec_comp(inputDir="inputs/", det="T2KND", flux="FHC_numu"):


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
    qe_cut = "cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
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
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_H2O_EnuQE_gencomp.pdf", inFileList, nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
                        "E_{#nu}^{rec, QE} (GeV); d#sigma/dE_{#nu}^{rec, QE} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.65, 0.3, 0.85, 0.93])
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_H2O_EnuQEbias_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+mod_enuqe+" - Enu_true)/Enu_true", "60,-0.9,0.5", qe_cut, \
                        "(E_{#nu}^{rec, QE} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.3, 0.42, 0.93], yRatLimits=[0,2.2])
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_H2O_EnuQEabsbias_gencomp.pdf", inFileList, nameList, colzList, lineList, mod_enuqe+" - Enu_true", "60,-0.9,0.5", qe_cut, \
	                "E_{#nu}^{rec, QE} - E_{#nu}^{true} (GeV); Arb. norm.", norm="shape", lineStyle="][", legDim=[0.22, 0.3, 0.42, 0.93], yRatLimits=[0,2.2])

if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_T2K_erec_comp")

    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det',    type=str, required=True)
    parser.add_argument('--flux',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    make_T2K_erec_comp(args.input,
                       det=args.det,
                       flux=args.flux,
                       outdir=args.output)
    

