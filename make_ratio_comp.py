import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory
from glob import glob

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

def make_generator_ratio_comp(outPlotName, inFileNumList, inFileDenList, nameList, colzList, \
                              plotVar="q0", binning=[100,0,5], cut="cc==1", \
                              labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                              isShape=False, minMax=None):

    ## Skip files that already exist
    if os.path.isfile("plots/"+outPlotName):
        print("Skipping plots/"+outPlotName, "which already exists!")
        return

    isLog = False
    histNumList = []
    histDenList = []
    histList = []
    ratList  = []
    
    can     .cd()
    top_pad = TPad("top_pad", "top_pad", 0, 0.4, 1, 1)
    top_pad .Draw()
    bot_pad = TPad("bot_pad", "bot_pad", 0, 0, 1, 0.4)
    bot_pad .Draw()
    top_pad .cd()
    ratio = 0.6/0.4

    titleSize = 0.05
    labelSize = 0.04
    histNum   = 0
    
    ## Loop over the input files and make the histograms
    for inFileName in inFileNumList:

        ## Modify to use glob
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)

        ## Correct for hydrogen in some of the samples
        targNorm = get_targ_norm(inFileName)

        thisHist = TH1D("hist_"+str(histNum), "hist_"+str(histNum)+";"+labels, binning[0], binning[1], binning[2])
        inTree.Draw(plotVar+">>hist_"+str(histNum), "("+cut+")*fScaleFactor")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        histNumList .append(thisHist)
        histNum += 1
        
    for inFileName in inFileDenList:

        ## Modify to use glob
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)

        targNorm = get_targ_norm(inFileName)

        thisHist = TH1D("hist_"+str(histNum), "hist_"+str(histNum)+";"+labels, binning[0], binning[1], binning[2])
        inTree.Draw(plotVar+">>hist_"+str(histNum), "("+cut+")*fScaleFactor")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(targNorm/float(nFiles))

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        histDenList .append(thisHist)
        histNum += 1
        
    ## Make the first ratio
    for x in range(len(histNumList)):
        rat_hist = histNumList[x].Clone()
        rat_hist .Divide(histDenList[x])
        histList .append(rat_hist)
        
    ## Now make the second ratio
    nomHist = histList[0].Clone()
    for hist in histList:
        rat_hist = hist.Clone()
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)
        
    ## Get the maximum value
    maxVal = 1.5
    minVal = 0.5

    if minMax:
        minVal = minMax[0]
        maxVal = minMax[1]
    
    ## Actually draw the histograms
    histList[0].Draw("HIST")
    histList[0].SetMaximum(maxVal)
    histList[0].SetMinimum(minVal)

    ## Unify title/label sizes
    histList[0] .GetYaxis().SetTitleSize(titleSize)
    histList[0] .GetYaxis().SetLabelSize(labelSize)
    histList[0] .GetYaxis().SetTitleOffset(1.4)
    
    ## Suppress x axis title and labels
    histList[0] .GetXaxis().SetTitle("")
    histList[0] .GetXaxis().SetTitleSize(0.0)
    histList[0] .GetXaxis().SetLabelSize(0.0)
    
    for x in reversed(range(len(histList))):
        histList[x].SetLineWidth(3)
        histList[x].SetLineColor(colzList[x])
        histList[x].Draw("HIST SAME")

    midline = TLine(ratList[1].GetXaxis().GetBinLowEdge(1), 1, ratList[1].GetXaxis().GetBinUpEdge(ratList[1].GetNbinsX()), 1)
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
    for hist in range(len(histList)):
        leg .AddEntry(histList[hist], nameList[hist], "l")
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

    ## Skip ratList[0] as everything is a ratio w.r.t that
    ratList[1] .Draw("][ HIST")
    ratList[1] .SetMaximum(1.5)
    ratList[1] .SetMinimum(0.5)

    ratList[1] .GetYaxis().SetTitle("Ratio w.r.t. "+nameList[0])
    ratList[1] .GetYaxis().CenterTitle(1)
    ratList[1] .GetXaxis().CenterTitle(0)
    ratList[1] .GetYaxis().SetTitleOffset(0.85)    
    ratList[1] .GetXaxis().SetNdivisions(505)
    ratList[1] .GetXaxis().SetTickLength(histList[0].GetXaxis().GetTickLength()*ratio)
    ratList[1] .GetXaxis().SetTitleSize(titleSize*ratio)
    ratList[1] .GetXaxis().SetLabelSize(labelSize*ratio)
    ratList[1] .GetYaxis().SetTitleSize(titleSize*ratio)
    ratList[1] .GetYaxis().SetLabelSize(labelSize*ratio)

    for x in reversed(range(1, len(histList))):
        ratList[x].SetLineWidth(3)
        ratList[x].SetLineColor(colzList[x])
        ratList[x].Draw("][ HIST SAME")

    midline .Draw("LSAME")
    
    ## Save
    gPad  .RedrawAxis()
    gPad  .SetRightMargin(0.02)
    gPad  .SetTopMargin(0.00)
    gPad  .SetBottomMargin(0.25)
    gPad  .SetLeftMargin(0.15)
    can   .Update()
    can .SaveAs("plots/"+outPlotName)

    
def make_flav_ratio_plots(inputDir="inputs/", flav1="nue", flav2="numu", targ="Ar40", sample="ccinc", minMax=None):

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

    inFileNumList = [inputDir+"/"+det+"_"+flav1+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav1+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                     ]

    inFileDenList = [inputDir+"/"+det+"_"+flav2+"_"+targ+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_NEUT562_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav2+"_"+targ+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                     ]    
    
    make_generator_ratio_comp(det+"_"+flav1+"_over_"+flav2+"_"+targ+"_enu_"+sample+"_gencomp.png", inFileNumList, inFileDenList, \
                              nameList, colzList, "Enu_true", [20,0,5], cut, \
                              "E_{#nu}^{true} (GeV); "+get_flav_label(flav1)+"/"+get_flav_label(flav2)+" "+get_targ_label(targ)+" "+sample_label+" ratio", \
                              False, minMax)

def make_targ_ratio_plots(inputDir="inputs/", targ1="C8H8", targ2="H2O", flav="numu", sample="ccinc", minMax=None):

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

    inFileNumList = [inputDir+"/"+det+"_"+flav+"_"+targ1+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_NEUT562_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ1+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                     ]

    inFileDenList = [inputDir+"/"+det+"_"+flav+"_"+targ2+"_GENIEv3_G18_10a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_GENIEv3_G18_10b_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_GENIEv3_G18_10c_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_GENIEv3_CRPA21_04a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_GENIEv3_G21_11a_00_000_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_NEUT562_1M_*_NUISFLAT.root",\
                     inputDir+"/"+det+"_"+flav+"_"+targ2+"_NUWRO_LFGRPA_1M_*_NUISFLAT.root"\
                     ]    
    
    make_generator_ratio_comp(det+"_"+targ1+"_over_"+targ2+"_"+flav+"_enu_"+sample+"_gencomp.png", inFileNumList, inFileDenList, \
                              nameList, colzList, "Enu_true", [20,0,5], cut, \
                              "E_{#nu}^{true} (GeV);"+get_flav_label(flav)+" "+get_targ_label(targ1)+"/"+get_targ_label(targ2)+" "+sample_label+" ratio", \
                              False, minMax)
    
    
if __name__ == "__main__":

    inputDir="/global/cfs/cdirs/dune/users/cwilk/MC_IOP_review/*/"
    for targ in ["Ar40", "C8H8", "H2O"]:
        for sample in ["ccinc", "cc0pi"]:
            make_flav_ratio_plots(inputDir, "nue", "numu", targ, sample, [0.9, 1.5])
            make_flav_ratio_plots(inputDir, "nuebar", "numubar", targ, sample, [0.9, 1.5])
            make_flav_ratio_plots(inputDir, "nuebar", "nue", targ, sample, [0, 0.8])
            make_flav_ratio_plots(inputDir, "numubar", "numu", targ, sample, [0, 0.8])

    for flav in ["numu", "numubar", "nue", "nuebar"]:
        for sample in ["ccinc", "cc0pi"]:
            make_targ_ratio_plots(inputDir, "Ar40", "C8H8", flav, sample)
            make_targ_ratio_plots(inputDir, "H2O", "C8H8", flav, sample)


