import argparse
from plotting_functions import make_generator_comp

ccinc = "cc==1 && nfsp>0"
cc0pi = ccinc + "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
ehad = "Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"

def make_ehad_plots(inputDir="inputs/", det="DUNEND", targ="Ar40", flux="FHC_numu", outdir="plots/"):

    cut = ccinc
    if "T2K" in det:
        cut = cc0pi

    cut += "&& ("+ehad+")/q0 > 1E-4"
    
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
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_"+targ+"_ehadoverq0_gencomp.pdf", inFileList, nameList, colzList, lineList, "("+ehad+")/q0", "40,0,1.2", cut, \
                        "E_{had}^{rec}/q_{0}; d#sigma/d(E_{had}^{rec}/q_{0}) (#times 10^{-38} cm^{2}/nucleon)", [0.2, 0.3, 0.45, 0.93], 1, [0, None], [0,2.6])

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_ehad_over_q0_comp")
    
    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det',    type=str, required=True)
    parser.add_argument('--targ',   type=str, required=True)
    parser.add_argument('--flux',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))
    
    make_ehad_plots(args.input,
                    args.det,
                    args.targ,
                    args.flux,
                    outdir=args.output)
    
