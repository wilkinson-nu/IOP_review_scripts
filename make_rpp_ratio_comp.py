import argparse
from plotting_functions import make_generator_ratio_comp

def get_flav_label(flav):
    if flav == "-14": return "#bar{#nu}_{#mu}"
    if flav == "-12": return "#bar{#nu}_{e}"
    if flav == "14": return "#nu_{#mu}"
    if flav == "12": return "#nu_{e}"
    return "#nu"

## In this case, ignore hydrogen...
def get_targ_label(targ):
    if targ == "Ar40": return "^{40}Ar"
    if targ == "C8H8": return "^{12}C"
    if targ == "H2O": return "^{16}O"
    if targ == "C12": return "^{12}C"
    if targ == "O16": return "^{16}O"
    print("Unknown target", targ)
    return targ

def get_cut_from_sample(sample):
    cut = "nfsp > 0 && Enu_true > 0.13"
    sample_label = "NONE"

    if sample == "ccinc":
        cut += "&& cc==1"
        sample_label = "CCINC"
    if sample == "cc1pi":
        cut += "&& cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(abs(pdg)==211 || pdg==111)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC1#pi"
    if sample == "cc1pip":
        cut += "&& cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==211)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC1#pi^{+}"
    if sample == "cc1pi0":
        cut += "&& cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==111)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC1#pi^{0}"
    if sample == "cc1pim":
        cut += "&& cc==1 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==-211)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC1#pi^{-}"
    if sample == "nc1pip":
        cut += "&& cc==0 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==211)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "NC1#pi^{+}"
    if sample == "nc1pi0":
        cut += "&& cc==0 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==111)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "NC1#pi^{0}"
    if sample == "ncnpi0":
        cut += "&& cc==0 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==Sum$(pdg==111) && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "NCN#pi^{0}"
    if sample == "nc1pim":
        cut += "&& cc==0 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==1 && Sum$(pdg==-211)==1 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "NC1#pi^{-}"

    return cut, sample_label

def make_nc_over_ccrpp_ratio_plots(inputDir="inputs/",
                                   targ="C8H8",
                                   flavNum="14",
                                   flavDen="14",
                                   sampleNum="ncpi0",
                                   sampleDen="ccpip",
                                   yLimits=[0.65, 1.25],
                                   yRatLimits=[0.5, 1.5],
                                   outdir="plots"):

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

    cut_num, label_num = get_cut_from_sample(sampleNum)
    cut_den, label_den = get_cut_from_sample(sampleDen)

    inFileNumList = [inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_GENIEv3_G18_10b_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_GENIEv3_G18_10c_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavNum+"_"+targ+"_*GeV_GiBUUwithNC_100k_*_NUISFLAT.root"\
                     ]

    inFileDenList = [inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_GENIEv3_G18_10a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_GENIEv3_G18_10b_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_GENIEv3_G18_10c_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_GENIEv3_CRPA21_04a_00_000_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_NEUT580_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_NEUTDCC_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_NUWRO_LFGRPA_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_NUWROv25.3.1_100k_*_NUISFLAT.root",\
                     inputDir+"/MONOENSEMBLE_"+flavDen+"_"+targ+"_*GeV_GiBUUwithNC_100k_*_NUISFLAT.root"\
                     ]

    binning = [0, 0.13, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]


    outName = outdir+"/XSEC_ratio_"+sampleNum+"_"+flavNum+"_over_"+sampleDen+"_"+flavDen+"_"+targ+"_gencomp.pdf"
    titles  = "E_{#nu}^{true} (GeV);("+get_flav_label(flavNum)+" " + label_num+"/"+get_flav_label(flavDen)+" "+label_den+")-"+get_targ_label(targ)+" ratio"

    ## Simplify the titles and name if the flavour is the same
    if flavNum == flavDen:
        outName = outdir+"/XSEC_ratio_"+sampleNum+"_over_"+sampleDen+"_"+flavNum+"_"+targ+"_gencomp.pdf"
        titles  = "E_{#nu}^{true} (GeV);"+get_flav_label(flavNum)+"-"+get_targ_label(targ)+" " + label_num+"/"+label_den+" ratio"
    
    make_generator_ratio_comp(outName, inFileNumList, inFileDenList, \
                              nameList, colzList, lineList, "Enu_true", binning, cut_num, \
                              titles, \
                              legDim=[0.65, 0.44, 0.93, 0.93], legCols=1, yLimits=yLimits, yRatLimits=yRatLimits, norm="enu_ensemble", lineStyle="][ ",
                              cutDen=cut_den, topMidLine=False)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_rpp_ratio_plots")

    # Add arguments
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--targ', type=str, required=True)
    parser.add_argument('--flav_num', type=str, required=True)
    parser.add_argument('--flav_den', type=str, required=True)
    parser.add_argument('--sample_num', type=str, required=True)
    parser.add_argument('--sample_den', type=str, required=True)
    parser.add_argument('--y_limits', type=float, nargs=2, required=True)
    parser.add_argument('--y_rat_limits', type=float, nargs=2, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    make_rpp_ratio_plots(args.input,
                         args.targ,
                         args.flav_num,
                         args.flav_den,
                         args.sample_num,
                         args.sample_den,
                         args.y_limits,
                         args.y_rat_limits,
                         outdir=args.output)
    


