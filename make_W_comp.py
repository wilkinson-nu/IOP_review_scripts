from plotting_functions import make_generator_comp, make_generator_ratio_comp
import argparse

def make_W_comp(inputDir="inputs/", det="T2KND", flux="FHC_numu", outdir="plots/"):

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
    
    ehad_cut = "cc==1"

    targ = "Ar40"
    binning="100,0.5,3"
    if "T2K" in det:
        targ = "H2O"
        binning="100,0.5,2"
        
    inFileList = [inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUT580_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_NEUTDCC_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                  inputDir+"/"+det+"_"+flux+"_"+targ+"_GiBUU_1M_*_NUISFLAT.root"\
                  ]
    
    make_generator_comp(outdir+"/"+det+"_"+flux+"_"+targ+"_W_gencomp.pdf", inFileList, nameList, colzList, lineList, "W", binning, ehad_cut, \
                        "W (GeV); d#sigma/dW (#times 10^{-38} cm^{2}/GeV/nucleon)", withRebin=True, legDim=[0.65, 0.44, 0.93, 0.93])
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_W_comp")
    
    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det',    type=str, required=True)
    parser.add_argument('--flux',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))
    
    make_W_comp(args.input,
                args.det,
                args.flux,
                outdir=args.output)
    
