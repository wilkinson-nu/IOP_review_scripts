import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob

## Use double precision for TTree draw
gEnv.SetValue("Hist.Precision.1D", "double")

## No need to see the plots appear here
gROOT.SetBatch(1)
gStyle.SetLineWidth(3)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(4)
gStyle.SetLineStyleString(11,"40 20 40 20")
gStyle.SetLineStyleString(12,"20 10 20 10")

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

## Make some colorblind friendly objects
## From: https://personal.sron.nl/~pault/#sec:qualitative
kkBlue    = TColor(9000,   0/255., 119/255., 187/255.)
kkCyan    = TColor(9001,  51/255., 187/255., 238/255.)
kkTeal    = TColor(9002,   0/255., 153/255., 136/255.)
kkOrange  = TColor(9003, 238/255., 119/255.,  51/255.)
kkRed     = TColor(9004, 204/255.,  51/255.,  17/255.)
kkMagenta = TColor(9005, 238/255.,  51/255., 119/255.)
kkGray    = TColor(9006, 187/255., 187/255., 187/255.)

can = TCanvas("can", "can", 600, 1000)
can .cd()

def get_flav_label(flav):
    label = "#nu"
    if "bar" in flav: label = "#bar{"+label+"}"
    if "mu" in flav: label += "_{#mu}"
    if "tau" in flav: label += "_{#tau}"
    if "e" in flav: label += "_{e}"
    return label

## In this case, ignore hydrogen...
def get_targ_label(targ):
    if targ == "Ar40": return "^{40}Ar"
    if targ == "C8H8": return "^{12}C"
    if targ == "H2O": return "^{16}O"
    print("Unknown target", targ)
    return targ

## This is to remove hydrogen from the /nucleon cross sections NUISANCE produces...
def get_targ_norm(inString):
    if "C8H8" in inString: return 13/12.
    if "H2O" in inString: return  18/16.
    return 1.
    
def get_chain(inputFileNames, max_files=999):

    inFile   = ROOT.TFile(glob(inputFileNames)[0], "READ")
    inFlux   = None
    inEvt    = None
    treeName = None
    nFiles   = 0

    for key in inFile.GetListOfKeys():
        if "FLUX" in key.GetName():
            inFlux = inFile.Get(key.GetName())
            inFlux .SetDirectory(0)
        if "VARS" in key.GetName():
            treeName = key.GetName()
    
    inFile .Close()
    
    inTree = ROOT.TChain(treeName)
    for inputFileName in glob(inputFileNames):

        nFiles += 1
        if nFiles > max_files: break
        
        inTree.Add(inputFileName)

        ## Add the histograms up
        inFile   = ROOT.TFile(inputFileName, "READ")
        for key in inFile.GetListOfKeys():
            if "EVT" not in key.GetName(): continue
            tempEvt = inFile.Get(key.GetName())
            if not inEvt:
                inEvt = tempEvt
                inEvt .SetDirectory(0)
            else: inEvt.Add(tempEvt)
        inFile.Close()    

    print("Found", inputFileNames, ":", inTree.GetEntries(), "events in", nFiles, "files")

    return inTree, inFlux, inEvt, nFiles

## The double ratio is (A/B)/(C/D)
def make_double_ratio_comp(outPlotName, inFileListA, inFileListB, inFileListC, inFileListD,
                           nameList, colzList, \
                           plotVar="q0", binning="100,0,5", cut="cc==1", \
                           labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                           isShape=False, minMax=None):

    ## Skip files that already exist
    if os.path.isfile("plots/"+outPlotName):
        print("Skipping plots/"+outPlotName, "which already exists!")
        return

    isLog = False
    histListA = []
    histListB = []
    histListC = []
    histListD = []    

    ## The combinations
    histListAB   = []
    histListCD   = []
    histListABCD = []
    ratListABCD  = []

    nHists     = len(inFileListA)
    
    can     .cd()
    top_pad = TPad("top_pad", "top_pad", 0, 0.4, 1, 1)
    top_pad .Draw()
    bot_pad = TPad("bot_pad", "bot_pad", 0, 0, 1, 0.4)
    bot_pad .Draw()
    top_pad .cd()
    ratio = 0.6/0.4

    titleSize = 0.05
    labelSize = 0.04
    
    ## Loop over the input files and make the histograms
    for inFileName in inFileListA:
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        targNorm = get_targ_norm(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histListA .append(thisHist)
        
    for inFileName in inFileListB:
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        targNorm = get_targ_norm(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histListB .append(thisHist)

    for inFileName in inFileListC:
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        targNorm = get_targ_norm(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histListC .append(thisHist)

    for inFileName in inFileListD:
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        targNorm = get_targ_norm(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histListD .append(thisHist)     

    ## Make the first ratio
    for x in range(nHists):
        histAB = histListA[x].Clone()
        histAB .Divide(histListB[x])
        histListAB .append(histAB)

        histCD = histListC[x].Clone()
        histCD .Divide(histListD[x])
        histListCD .append(histCD)

    ## Make the double ratio
    for x in range(nHists):
        histABCD = histListAB[x].Clone()
        histABCD .Divide(histListCD[x])
        histListABCD.append(histABCD)
        
    ## Now make the second ratio
    nomHist = histListABCD[0].Clone()
    for x in range(nHists):
        rat_hist = histListABCD[x].Clone()
        rat_hist .Divide(nomHist)
        ratListABCD .append(rat_hist)
        
    ## Get the maximum value
    maxVal = 1.5
    minVal = 0.5

    if minMax:
        minVal = minMax[0]
        maxVal = minMax[1]
    
    ## Actually draw the histograms
    histListABCD[0].Draw("HIST")
    histListABCD[0].SetMaximum(maxVal)
    histListABCD[0].SetMinimum(minVal)

    ## Unify title/label sizes
    histListABCD[0] .GetYaxis().SetTitleSize(titleSize)
    histListABCD[0] .GetYaxis().SetLabelSize(labelSize)
    histListABCD[0] .GetYaxis().SetTitleOffset(1.4)
    
    ## Suppress x axis title and labels
    histListABCD[0] .GetXaxis().SetTitle("")
    histListABCD[0] .GetXaxis().SetTitleSize(0.0)
    histListABCD[0] .GetXaxis().SetLabelSize(0.0)
    
    for x in reversed(range(nHists)):
        histListABCD[x].SetLineWidth(3)
        histListABCD[x].SetLineColor(colzList[x])
        histListABCD[x].Draw("HIST SAME")

    midline = TLine(ratListABCD[1].GetXaxis().GetBinLowEdge(1), 1, ratListABCD[1].GetXaxis().GetBinUpEdge(ratListABCD[1].GetNbinsX()), 1)
    midline .SetLineWidth(3)
    midline .SetLineColor(ROOT.kBlack)
    midline .SetLineStyle(11)
    midline .Draw("LSAME")
    
    ## Now make a legend
    dim = [0.2, 0.85, 0.98, 1.00]
    leg = TLegend(dim[0], dim[1], dim[2], dim[3], "", "NDC")
    leg .SetShadowColor(0)
    leg .SetFillColor(0)
    leg .SetLineWidth(0)
    leg .SetTextSize(0.036)
    leg .SetNColumns(3)
    leg .SetLineColor(kWhite)
    for hist in range(len(histListABCD)):
        leg .AddEntry(histListABCD[hist], nameList[hist], "l")
    leg .Draw("SAME")

    gPad.SetLogy(0)
    if isLog: gPad.SetLogy(1)
    gPad.SetRightMargin(0.02)
    gPad.SetTopMargin(0.15)
    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.022)
    gPad.RedrawAxis()
    gPad.Update()

    ## Now ratios on the bottom panel
    bot_pad.cd()

    ## Skip ratListABCD[0] as everything is a ratio w.r.t that
    ratListABCD[1] .Draw("][ HIST")
    ratListABCD[1] .SetMaximum(1.3)
    ratListABCD[1] .SetMinimum(0.7)

    ratListABCD[1] .GetYaxis().SetTitle("Ratio w.r.t. "+nameList[0])
    ratListABCD[1] .GetYaxis().CenterTitle(1)
    ratListABCD[1] .GetXaxis().CenterTitle(0)
    ratListABCD[1] .GetYaxis().SetTitleOffset(0.85)    
    ratListABCD[1] .GetXaxis().SetNdivisions(505)
    ratListABCD[1] .GetXaxis().SetTickLength(histListABCD[0].GetXaxis().GetTickLength()*ratio)
    ratListABCD[1] .GetXaxis().SetTitleSize(titleSize*ratio)
    ratListABCD[1] .GetXaxis().SetLabelSize(labelSize*ratio)
    ratListABCD[1] .GetYaxis().SetTitleSize(titleSize*ratio)
    ratListABCD[1] .GetYaxis().SetLabelSize(labelSize*ratio)

    for x in reversed(range(1, nHists)):
        ratListABCD[x].SetLineWidth(3)
        ratListABCD[x].SetLineColor(colzList[x])
        ratListABCD[x].Draw("][ HIST SAME")

    midline .Draw("LSAME")
    
    ## Save
    gPad  .RedrawAxis()
    gPad  .SetRightMargin(0.02)
    gPad  .SetTopMargin(0.00)
    gPad  .SetBottomMargin(0.25)
    gPad  .SetLeftMargin(0.15)
    can   .Update()
    can .SaveAs("plots/"+outPlotName)

    
def make_flav_double_ratio_plots(inputDir="inputs/", flavA="nuebar", flavB="numubar", \
                                 flavC="nue", flavD="numu", targ="Ar40", sample="ccinc", minMax=None):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]
    
    cut = "cc==1 && tgta != 1 && tgt != 1000010010 && Enu_true > 0.2"
    sample_label = "CCINC"
    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"
        
    det  = "falling_5GeV"

    inFileListA = [inputDir+"/"+det+"_"+flavA+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]

    inFileListB = [inputDir+"/"+det+"_"+flavB+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]

    inFileListC = [inputDir+"/"+det+"_"+flavC+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavC+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]

    inFileListD = [inputDir+"/"+det+"_"+flavD+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavD+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]
    
    make_double_ratio_comp(det+"_double_flav_ratio_"+targ+"_enu_"+sample+"_gencomp.png", \
                           inFileListA, inFileListB, inFileListC, inFileListD, \
                           nameList, colzList, "Enu_true", "20,0,5", cut, \
                           "E_{#nu}^{true} (GeV); ("+get_flav_label(flavA)+"/"+get_flav_label(flavB)+")/("+get_flav_label(flavC)+"/"+get_flav_label(flavD)+") "+ get_targ_label(targ)+" "+sample_label+" ratio", \
                           False, minMax)

def make_targ_double_ratio_plots(inputDir="inputs/", targ1="C8H8", targ2="H2O", flavA="nue", flavB="numu", sample="ccinc", minMax=None):

    nameList = ["GENIE 10a",\
                "GENIE 10b",\
                "GENIE 10c",\
                "CRPA",\
                "SuSAv2",\
                "NEUT",\
                "NuWro"\
                ]
    colzList = [9000, 9001, 9002, 9003, 9004, 9006, 9005]
    
    cut = "cc==1 && tgta != 1 && tgt != 1000010010 && Enu_true > 0.2"
    sample_label = "CCINC"
    if sample == "cc0pi":
        cut += "&& Sum$(abs(pdg) > 100 && abs(pdg) < 2000)==0 && Sum$(abs(pdg) > 2300 && abs(pdg) < 100000)==0"
        sample_label = "CC0#pi"

    det  = "falling_5GeV"

    inFileListA = [inputDir+"/"+det+"_"+flavA+"_"+targ1+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ1+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]
    inFileListB = [inputDir+"/"+det+"_"+flavB+"_"+targ1+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ1+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]
    inFileListC = [inputDir+"/"+det+"_"+flavA+"_"+targ2+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavA+"_"+targ2+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]
    inFileListD = [inputDir+"/"+det+"_"+flavB+"_"+targ2+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_NEUT562_1M_*_NUISFLAT.root",\
                   inputDir+"/"+det+"_"+flavB+"_"+targ2+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                   ]  
    
    make_double_ratio_comp(det+"_double_targ_ratio_"+targ1+"_over_"+targ2+"_"+flavA+"_over_"+flavB+"_enu_"+sample+"_gencomp.png",
                           inFileListA, inFileListB, inFileListC, inFileListD, \
                           nameList, colzList, "Enu_true", "20,0,5", cut, \
                           "E_{#nu}^{true} (GeV);("+get_flav_label(flavA)+"/"+get_flav_label(flavB)+")_{"+get_targ_label(targ1)+"}/("+get_flav_label(flavA)+"/"+get_flav_label(flavB)+")_{"+get_targ_label(targ2)+"} "+sample_label+" ratio", \
                           False, minMax)
    
    
if __name__ == "__main__":

    inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    for targ in ["Ar40", "C8H8", "H2O"]:
        for sample in ["ccinc", "cc0pi"]:
            make_flav_double_ratio_plots(inputDir, "nuebar", "numubar", "nue", "numu", targ, sample, [0.7, 1.3])

    ## flavA = "nue"
    ## flavB = "numu"
    ## for sample in ["ccinc", "cc0pi"]:
    ##     make_targ_double_ratio_plots(inputDir, "Ar40", "C8H8", flavA, flavB, sample)
    ##     make_targ_double_ratio_plots(inputDir, "H2O", "C8H8", flavA, flavB, sample)
    ## 
    ## flavA = "nuebar"
    ## flavB = "numubar"
    ## for sample in ["ccinc", "cc0pi"]:
    ##     make_targ_double_ratio_plots(inputDir, "Ar40", "C8H8", flavA, flavB, sample)
    ##     make_targ_double_ratio_plots(inputDir, "H2O", "C8H8", flavA, flavB, sample)        

