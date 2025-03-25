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

gStyle.SetTextSize(0.06)
gStyle.SetLabelSize(0.06,"xyzt")
gStyle.SetTitleSize(0.07,"xyzt")

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


def get_chain(inputFileNames, max_files=999):

    print("Found", inputFileNames)
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

    print("Found", inTree.GetEntries(), "events in chain")

    return inTree, inFlux, inEvt, nFiles


def make_generator_comp_noratio(outPlotName, inFileList, nameList, colzList, \
                                plotVar="q0", binning="100,0,5", cut="cc==1", \
                                labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
			        legDim=[0.65, 0.5, 0.85, 0.93], maxVal=None, isShape=False, isLog=False):
    
    ## Skip files that already exist
    if os.path.isfile("plots/"+outPlotName):
        print("Skipping plots/"+outPlotName, "which already exists!")
        return

    can_small = TCanvas("can_small", "can_small", 600, 600)
    can_small.cd()

    histList = []

    titleSize = 0.07
    labelSize = 0.06
    
    ## Loop over the input files and make the histograms
    for inFileName in inFileList:

        ## Modify to use glob
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor*1E38")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(1./nFiles, "width")

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histList .append(thisHist)

    ## Get the maximum value
    if not maxVal:
        maxVal   = 0
        for hist in histList:
            if hist.GetMaximum() > maxVal:
                maxVal = hist.GetMaximum()        
        maxVal = maxVal*1.1
    if isLog: maxVal *= 2
        
    ## Actually draw the histograms
    histList[0].Draw("HIST")
    histList[0].SetMaximum(maxVal)

    ## Unify title/label sizes
    histList[0] .GetYaxis().SetTitleSize(titleSize)
    histList[0] .GetYaxis().SetLabelSize(labelSize)
    histList[0] .GetYaxis().SetTitleOffset(1.3)
    
    ## Suppress x axis title and labels
    # histList[0] .GetXaxis().SetTitle("")
    histList[0] .GetXaxis().SetTitleSize(titleSize)
    histList[0] .GetXaxis().SetLabelSize(labelSize)
    
    if not isLog: histList[0].SetMinimum(0)
    for x in reversed(range(len(histList))):
        histList[x].SetLineWidth(3)
        histList[x].SetLineColor(colzList[x])
        histList[x].Draw("HIST SAME")

    
    ## Now make a legend
    leg = TLegend(legDim[0], legDim[1], legDim[2], legDim[3], "", "NDC")
    leg .SetShadowColor(0)
    leg .SetFillColor(0)
    leg .SetLineWidth(0)
    leg .SetTextSize(0.07)
    # leg .SetNColumns(3)
    leg .SetLineColor(kWhite)
    for hist in range(len(histList)):
        leg .AddEntry(histList[hist], nameList[hist], "l")
    leg .Draw("SAME")

    gPad.SetLogy(0)
    if isLog: gPad.SetLogy(1)
    gPad.SetRightMargin(0.03)
    gPad.SetTopMargin(0.02)
    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.15)
    gPad.RedrawAxis()
    gPad.Update()
    can_small .SaveAs("plots/"+outPlotName)


def make_generator_comp(outPlotName, inFileList, nameList, colzList, \
                        plotVar="q0", binning="100,0,5", cut="cc==1", \
                        labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                        legDim=[0.65, 0.5, 0.85, 0.93], ratLimits=[0.4, 1.6], maxVal=None, isShape=False):

    ## Skip files that already exist
    if os.path.isfile("plots/"+outPlotName):
        print("Skipping plots/"+outPlotName, "which already exists!")
        return
    
    isLog = False
    histList = []
    ratList  = []

    can = TCanvas("can", "can", 800, 800)

    can     .cd()
    bottom_fract = 0.4
    top_pad = TPad("top_pad", "top_pad", 0, bottom_fract, 1, 1)
    top_pad .Draw()
    bot_pad = TPad("bot_pad", "bot_pad", 0, 0, 1, bottom_fract)
    bot_pad .Draw()
    top_pad .cd()
    ratio = (1-bottom_fract)/bottom_fract

    titleSize = 0.07
    labelSize = 0.06
    
    ## Loop over the input files and make the histograms
    for inFileName in inFileList:

        ## Modify to use glob
        inTree, inFlux, inEvt, nFiles = get_chain(inFileName)
        
        inTree.Draw(plotVar+">>this_hist("+binning+")", "("+cut+")*fScaleFactor*1E38")
        thisHist = gDirectory.Get("this_hist")
        thisHist .SetDirectory(0)

        ## Deal with different numbers of files
        thisHist.Scale(1./nFiles, "width")

        ## Allow for shape option
        if isShape: thisHist .Scale(1/thisHist.Integral())

        ## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histList .append(thisHist)

    ## Sort out the ratio hists
    nomHist = histList[0].Clone()
    nomHist .Rebin(2)
    for hist in histList:
        rat_hist = hist.Clone()
        rat_hist .Rebin(2)
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)
        
    ## Get the maximum value
    if not maxVal:
        maxVal   = 0
        for hist in histList:
            if hist.GetMaximum() > maxVal:
                maxVal = hist.GetMaximum()        
        maxVal = maxVal*1.1
        
    ## Actually draw the histograms
    histList[0].Draw("HIST")
    histList[0].SetMaximum(maxVal)

    ## Unify title/label sizes
    histList[0] .GetYaxis().SetTitleSize(titleSize)
    histList[0] .GetYaxis().SetLabelSize(labelSize)
    histList[0] .GetYaxis().SetTitleOffset(0.8)
    
    ## Suppress x axis title and labels
    histList[0] .GetXaxis().SetTitle("")
    histList[0] .GetXaxis().SetTitleSize(0.0)
    histList[0] .GetXaxis().SetLabelSize(0.0)
    
    if not isLog: histList[0].SetMinimum(0)
    for x in reversed(range(len(histList))):
        histList[x].SetLineWidth(3)
        histList[x].SetLineColor(colzList[x])
        histList[x].Draw("HIST SAME")
    
    ## Now make a legend
    leg = TLegend(legDim[0], legDim[1], legDim[2], legDim[3], "", "NDC")
    leg .SetShadowColor(0)
    leg .SetFillColor(0)
    leg .SetLineWidth(0)
    leg .SetTextSize(0.07)
    leg .SetLineColor(kWhite)
    for hist in range(len(histList)):
        leg .AddEntry(histList[hist], nameList[hist], "l")
    leg .Draw("SAME")

    gPad.SetLogy(0)
    if isLog: gPad.SetLogy(1)
    gPad.SetRightMargin(0.03)
    gPad.SetTopMargin(0.01)
    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.022)
    gPad.RedrawAxis()
    gPad.Update()

    ## Now ratios on the bottom panel
    bot_pad.cd()

    ## Skip ratList[0] as everything is a ratio w.r.t that
    ratList[1] .Draw("][ HIST")
    ratList[1] .SetMaximum(ratLimits[1])
    ratList[1] .SetMinimum(ratLimits[0])

    ratList[1] .GetYaxis().SetTitle("#frac{Model}{"+nameList[0]+"}")
    ratList[1] .GetYaxis().CenterTitle(1)
    ratList[1] .GetXaxis().CenterTitle(0)
    ratList[1] .GetYaxis().SetTitleOffset(0.65)    
    ratList[1] .GetXaxis().SetNdivisions(505)
    ratList[1] .GetXaxis().SetTickLength(histList[0].GetXaxis().GetTickLength()*ratio)
    ratList[1] .GetXaxis().SetTitleSize(titleSize*ratio)
    ratList[1] .GetXaxis().SetLabelSize(labelSize*ratio)
    ratList[1] .GetYaxis().SetTitleSize(titleSize*ratio*0.9)
    ratList[1] .GetYaxis().SetLabelSize(labelSize*ratio)

    for x in reversed(range(1, len(histList))):
        ratList[x].SetLineWidth(3)
        ratList[x].SetLineColor(colzList[x])
        ratList[x].Draw("][ HIST SAME")

    midline = TLine(ratList[1].GetXaxis().GetBinLowEdge(1), 1, ratList[1].GetXaxis().GetBinUpEdge(ratList[1].GetNbinsX()), 1)
    midline .SetLineWidth(3)
    midline .SetLineColor(ROOT.kBlack)
    midline .SetLineStyle(11)
    midline .Draw("LSAME")
    
    ## Save
    gPad  .RedrawAxis()
    gPad  .SetRightMargin(0.03)
    gPad  .SetTopMargin(0.00)
    gPad  .SetBottomMargin(0.24)
    gPad  .SetLeftMargin(0.15)
    can   .Update()
    can .SaveAs("plots/"+outPlotName)



