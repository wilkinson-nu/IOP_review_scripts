from plotting_functions import make_A_over_BC_comp
import argparse

def make_SK_wrongsign_ratio_plots(inputDir="inputs/", flav="numu", legDim=[0.2, 0.58, 0.75, 0.93], outdir="plots/"):

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
    qe_cut = "cc==1 && nfsp>0 && Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0" # && Sum$(pdg==-2212)==0 && Sum$(pdg==-2112)==0"

    ## Change to Enu_QE to use a binding energy of 27 MeV! Not 34 like the NUISANCE default...                                                                                   
    binding = 27/1000.
    m2 = 0.93956536
    m1 = 0.93827203
    ml = 0.10565837

    if "nue" in flav: ml = 0.000511
    
    mod_enuqe = "(2*("+str(m1)+"-"+str(binding)+")*ELep -"+str(ml)+"*"+str(ml)+" + "+str(m2)+"*"+str(m2)+" - ("+str(m1)+"-"+str(binding)+")*("+str(m1)+"-"+str(binding)+"))/" \
        +"(2*(("+str(m1)+"-"+str(binding)+") - ELep + sqrt(ELep*ELep - "+str(ml)+"*"+str(ml)+")*CosLep))"

    sample_label = "CC0#pi"

    ## These plots need to be RHC numu / (RHC numu + RHC numubar)    
    inFileListNu = [inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NEUT580_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NEUTDCC_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*NUWROv25.3.1_1M_*_NUISFLAT.root",\
                    inputDir+"/T2KSK_osc_RHC_"+flav+"_H2O_*GiBUU_1M_*_NUISFLAT.root"\
                    ]

    inFileListNub = [inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/T2KSK_osc_RHC_"+flav+"bar_H2O_*GiBUU_1M_*_NUISFLAT.root"\
                     ]

    make_A_over_BC_comp(outdir+"/T2KSK_osc_"+flav+"wrongsign_EnuQE_gencomp.pdf", inFileListNu, inFileListNub, inFileListNu, \
                        nameList, colzList, lineList, mod_enuqe, "40,0,2", qe_cut, \
                        "E_{#nu}^{rec, QE} (GeV); Wrong-sign/total", yLimits=[0,1.05], withRebin=True, legDim=legDim, legCols=2)

def make_DUNE_wrongsign_ratio_plots(inputDir="inputs/", flav="numu", legDim=[0.4, 0.58, 0.95, 0.93], outdir="plots/"):

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

    ehad_cut = "cc==1 && nfsp > 0"
    enuhad = "ELep + Sum$((abs(pdg)==11 || (abs(pdg)>17 && abs(pdg)<2000))*E) + Sum$((abs(pdg)>2300 &&abs(pdg)<10000)*E) + \
    Sum$((abs(pdg)==2212)*(E - sqrt(E*E - px*px - py*py - pz*pz)))"

    inFileListNu = [inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NEUT580_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NEUTDCC_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                    inputDir+"/DUNEFD_osc_RHC_"+flav+"_Ar40_GiBUU_1M_*_NUISFLAT.root"\
                    ]

    inFileListNub = [inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NEUT580_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NEUTDCC_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NUWRO_LFGRPA_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_NUWROv25.3.1_1M_*_NUISFLAT.root",\
                     inputDir+"/DUNEFD_osc_RHC_"+flav+"bar_Ar40_GiBUU_1M_*_NUISFLAT.root"\
                     ]

    make_A_over_BC_comp(outdir+"/DUNEFD_osc_"+flav+"wrongsign_Enurec_gencomp.pdf", inFileListNu, inFileListNub, inFileListNu, \
                        nameList, colzList, lineList, enuhad, "80,0,8", ehad_cut, \
                        "E_{#nu}^{rec, had} (GeV); Wrong-sign/total", yLimits=[0,1.05], withRebin=True, legDim=legDim, legCols=2)

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser("make_wrongsign_ratio_comp")
    
    # Add arguments
    parser.add_argument('--input',  type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--det',    type=str, required=True)
    parser.add_argument('--flav',   type=str, required=True)

    ## Parse arguments from command line
    args = parser.parse_args()

    ## Report arguments
    for arg in vars(args): print(arg, getattr(args, arg))

    if "DUNE" in args.det:
        make_DUNE_wrongsign_ratio_plots(args.input,
                                        args.flav,
                                        outdir=args.output)
    else:
        make_SK_wrongsign_ratio_plots(args.input,
                                      args.flav,
                                      outdir=args.output)
