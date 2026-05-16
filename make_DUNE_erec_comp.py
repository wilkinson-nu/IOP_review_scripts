import argparse
from plotting_functions import make_generator_comp

def make_DUNE_erec_comp(inputDir="inputs/", det="DUNEND", flux="FHC_numu", outdir="plots/"):    

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
    ehad_cut = "cc==1"
    enuhad = "ELep + Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"
    targ = "Ar40"

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
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_Ar40_Enurec_gencomp.pdf", inFileList, nameList, colzList, lineList, enuhad, "80,0,8", ehad_cut, \
                        "E_{#nu}^{rec, had} (GeV); d#sigma/dE_{#nu}^{rec, had} (#times 10^{-38} cm^{2}/nucleon)", legDim=[0.65, 0.3, 0.85, 0.93])
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_Ar40_Enurecbias_gencomp.pdf", inFileList, nameList, colzList, \
                        lineList, "("+enuhad+" - Enu_true)/Enu_true", "60,-0.5,0.1", ehad_cut, \
                        "(E_{#nu}^{rec, had} - E_{#nu}^{true})/E_{#nu}^{true}; Arb. norm.",  [0.25, 0.3, 0.45, 0.93], yRatLimits=[0,2.2], norm="shape", lineStyle="][")
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_Ar40_Enurecabsbias_gencomp.pdf", inFileList, nameList, colzList, lineList, enuhad+" - Enu_true", "60,-0.5,0.1", ehad_cut, \
                        "E_{#nu}^{rec, had} - E_{#nu}^{true} (GeV); Arb. norm.",  [0.25, 0.3, 0.45, 0.93], yRatLimits=[0,2.2], norm="shape", lineStyle="][")
    
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_DUNE_erec_comp")

    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det',    type=str, required=True)
    parser.add_argument('--flux',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    make_DUNE_erec_comp(args.input,
                        det=args.det,
                        flux=args.flux,
                        outdir=args.output)
    

