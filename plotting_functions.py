import ROOT
import os
from ROOT import gStyle, TGaxis, TPad, TLine, gROOT, TH1, TColor, TCanvas, TFile, TH1D, gPad, TLegend, kWhite, gDirectory, gEnv
from glob import glob
from array import array

## Use double precision for TTree draw
gEnv.SetValue("Hist.Precision.1D", "double")

## No need to see the plots appear here
gROOT.SetBatch(1)
gStyle.SetLineWidth(3)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(0)
TGaxis.SetMaxDigits(4)

gStyle.SetTextSize(0.06)
gStyle.SetLabelSize(0.06,"xyzt")
gStyle.SetTitleSize(0.07,"xyzt")

gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetNdivisions(505, "XY")
gStyle.SetLineStyleString(11,"40 20 40 20")
gStyle.SetLineStyleString(12,"20 10 20 10")

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

kkMuted0  = TColor(8000,  51/255.,  34/255., 136/255.)
kkMuted1  = TColor(8001, 136/255., 204/255., 238/255.)
kkMuted2  = TColor(8002,  68/255., 170/255., 153/255.)
kkMuted3  = TColor(8003,  17/255., 119/255.,  51/255.)
kkMuted4  = TColor(8004, 153/255., 153/255.,  51/255.)
kkMuted5  = TColor(8005, 221/255., 204/255., 119/255.)
kkMuted6  = TColor(8006, 204/255., 102/255., 119/255.)
kkMuted7  = TColor(8007, 136/255.,  34/255.,  85/255.)
kkMuted8  = TColor(8008, 170/255.,  68/255., 153/255.)
kkMuted9  = TColor(8009, 221/255., 221/255., 221/255.)

def get_chain(inputFileNamesWithNorm, max_files=999):

    ## Do something funky to get a normalisation in here...
    inputFileNamesWithNormSplit = inputFileNamesWithNorm.split(";")
    inputFileNames = inputFileNamesWithNormSplit[0]
    print("Found", inputFileNames)

    norm = "1"
    if len(inputFileNamesWithNormSplit) > 1:
        norm = inputFileNamesWithNormSplit[1]
        print("Found norm:", norm)
    
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
            ## if not inEvt:
            ##     inEvt = tempEvt
            ##     inEvt .SetDirectory(0)
            ## else: inEvt.Add(tempEvt)
        inFile.Close()    

    ## Scale the event rate histogram
    ## inEvt .Scale(1./nFiles)
    print("Found", inTree.GetEntries(), "events in chain")

    return inTree, inFlux, inEvt, nFiles, norm

def make_one_panel_plot(outPlotName, histList, nameList, legDim=[0.65, 0.5, 0.85, 0.93], \
                        yLimits=[0, None], topMidLine=False, isLog=False, lineStyle="C", legHeader=None):
    
    can_small = TCanvas("can_small", "can_small", 600, 600)
    can_small.cd()

    titleSize = 0.07
    labelSize = 0.06
    
    ## Sort out the yLimits
    minVal = yLimits[0]
    maxVal = yLimits[1]
    
    if not maxVal:
        maxVal   = 0
        for hist in histList:
            if hist.GetMaximum() > maxVal:
                maxVal = hist.GetMaximum()        
        maxVal = maxVal*1.1
        if isLog: maxVal *= 2

    ## Print integrals
    for h in range(len(histList)):
        print(nameList[h], "integral =", histList[h].Integral(0, -1, "width"))
        
    ## Actually draw the histograms
    histList[0].Draw(lineStyle+"HIST")
    histList[0].SetMaximum(maxVal)
    if not isLog: histList[0].SetMinimum(minVal)

    ## Unify title/label sizes
    histList[0] .GetYaxis().SetTitleSize(titleSize)
    histList[0] .GetYaxis().SetLabelSize(labelSize)
    histList[0] .GetYaxis().SetTitleOffset(1.1)
    histList[0] .GetXaxis().SetTitleSize(titleSize)
    histList[0] .GetXaxis().SetLabelSize(labelSize)
    
    for x in reversed(range(len(histList))):
        histList[x].SetLineWidth(3)
        histList[x].Draw(lineStyle+"HIST SAME")

    midline = TLine(histList[0].GetXaxis().GetBinLowEdge(1), 1, histList[0].GetXaxis().GetBinUpEdge(histList[0].GetNbinsX()), 1)
    midline .SetLineWidth(2)
    midline .SetLineColor(ROOT.kBlack)
    midline .SetLineStyle(2)
    if topMidLine: midline.Draw("LSAME")
        
    ## Now make a legend
    leg = TLegend(legDim[0], legDim[1], legDim[2], legDim[3], "", "NDC")
    leg .SetShadowColor(0)
    leg .SetFillColor(0)
    leg .SetLineWidth(0)
    leg .SetTextSize(0.06)
    leg .SetLineColor(kWhite)
    if legHeader: 
        leg .SetHeader(legHeader)
    for hist in range(len(histList)):
        leg .AddEntry(histList[hist], nameList[hist], "l")
    leg .Draw("SAME")

    gPad.SetLogy(0)
    if isLog: gPad.SetLogy(1)
    gPad.SetRightMargin(0.03)
    gPad.SetTopMargin(0.03)
    gPad.SetLeftMargin(0.17)
    gPad.SetBottomMargin(0.15)
    gPad.RedrawAxis()
    gPad.Update()
    can_small .SaveAs(outPlotName)


def make_two_panel_plot(outPlotName, histList, ratList, nameList, legDim=[0.65, 0.5, 0.85, 0.93], \
                        yLimits=[0, None], yRatLimits=[0.4, 1.6], topMidLine=False, isLog=False, \
                        rat_title_num="Model", lineStyle="C", legHeader=None):

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

    midline = TLine(ratList[1].GetXaxis().GetBinLowEdge(1), 1, ratList[1].GetXaxis().GetBinUpEdge(ratList[1].GetNbinsX()), 1)
    midline .SetLineWidth(2)
    midline .SetLineColor(ROOT.kBlack)
    midline .SetLineStyle(2)
    
    ## Set the y limits
    minVal = yLimits[0]
    maxVal = yLimits[1]
    if not maxVal:
        maxVal   = 0
        for hist in histList:
            if hist.GetMaximum() > maxVal:
                maxVal = hist.GetMaximum()        
        maxVal = maxVal*1.1

    ## Print integrals
    for h in range(len(histList)):
        print(nameList[h], "integral =", histList[h].Integral(0, -1, "width"))
        
    ## Actually draw the histograms
    histList[0].Draw(lineStyle+"HIST")
    histList[0].SetMaximum(maxVal)
    if not isLog: histList[0].SetMinimum(minVal)
    
    ## Unify title/label sizes
    histList[0] .GetYaxis().SetTitleSize(titleSize)
    histList[0] .GetYaxis().SetLabelSize(labelSize)
    histList[0] .GetYaxis().SetTitleOffset(0.8)
    
    ## Suppress x axis title and labels
    histList[0] .GetXaxis().SetTitle("")
    histList[0] .GetXaxis().SetTitleSize(0.0)
    histList[0] .GetXaxis().SetLabelSize(0.0)
    
    for x in reversed(range(len(histList))):
        histList[x].SetLineWidth(3)
        histList[x].Draw(lineStyle+"HIST SAME")
        
    ## Now make a legend
    leg = TLegend(legDim[0], legDim[1], legDim[2], legDim[3], "", "NDC")
    leg .SetShadowColor(0)
    leg .SetFillColor(0)
    leg .SetLineWidth(0)
    leg .SetTextSize(0.07)
    leg .SetLineColor(kWhite)
    if legHeader:
        leg .SetHeader(legHeader)
    for hist in range(len(histList)):
        leg .AddEntry(histList[hist], nameList[hist], "l")
    leg .Draw("SAME")

    ## For ratio plots
    if topMidLine: midline.Draw("LSAME")
    
    gPad.SetLogy(0)
    if isLog: gPad.SetLogy(1)
    gPad.SetRightMargin(0.03)
    gPad.SetTopMargin(0.01)

    ### TESTING
    # gPad.SetTopMargin(0.1)

    gPad.SetLeftMargin(0.15)
    gPad.SetBottomMargin(0.028)
    gPad.RedrawAxis()
    gPad.Update()

    ## Now ratios on the bottom panel
    bot_pad.cd()

    ## Skip ratList[0] as everything is a ratio w.r.t that
    ratList[1] .Draw(lineStyle+"HIST")
    ratList[1] .SetMaximum(yRatLimits[1])
    ratList[1] .SetMinimum(yRatLimits[0])

    ratList[1] .GetYaxis().SetTitle("#frac{"+rat_title_num+"}{"+nameList[0]+"}")
    ratList[1] .GetYaxis().CenterTitle(1)
    ratList[1] .GetXaxis().CenterTitle(0)
    ratList[1] .GetYaxis().SetTitleOffset(0.65)    
    ratList[1] .GetXaxis().SetNdivisions(505)
    ratList[1] .GetXaxis().SetTickLength(histList[0].GetXaxis().GetTickLength()*ratio)
    ratList[1] .GetXaxis().SetTitleSize(titleSize*ratio)
    ratList[1] .GetXaxis().SetLabelSize(labelSize*ratio)
    ratList[1] .GetYaxis().SetTitleSize(titleSize*ratio*0.9)
    ratList[1] .GetYaxis().SetLabelSize(labelSize*ratio)

    for x in range(1, len(histList)):
        ratList[x].SetLineWidth(3)
        ratList[x].Draw(lineStyle+"HIST SAME")

    midline .Draw("LSAME")
    
    ## Save
    gPad  .RedrawAxis()
    gPad  .SetRightMargin(0.03)
    gPad  .SetTopMargin(0.00)
    gPad  .SetBottomMargin(0.24)
    gPad  .SetLeftMargin(0.15)
    can   .Update()
    can .SaveAs(outPlotName)


## This is slightly mad, all because of the silly way I used an ensemble of monoenergetic flux files to make flat distributions as a function of true Enu
## It just takes the first entry in each file, and fills the histogram, then returns that
## GiBUU made it harder than it needed to be...
def mad_enu_norm_hist(inputFileNames, hist):

    inFile   = ROOT.TFile(glob(inputFileNames)[0], "READ")
    treeName = None
    for key in inFile.GetListOfKeys():
        if "VARS" not in key.GetName(): continue
        treeName = key.GetName()
    inFile .Close()

    ## Loop over files and add a single entry
    for inputFileName in glob(inputFileNames):
        inputFile = ROOT.TFile(inputFileName, "READ")
        inTree = inputFile.Get(treeName)
        inTree .GetEntry(0)
        hist .Fill(inTree .Enu_true)
        inputFile .Close()

    return hist
    

## Return a list of histograms
def get_hist_list(inFileList, plotVar, binning, cut, labels, colzList, lineList, normType=None):
    
    histList = []
    nFile = len(inFileList)

    ## Loop over the input files and make the histograms
    for x in range(nFile):

        if isinstance(cut, list): thisCut = cut[x]
        else: thisCut = cut
        
        inFileName = inFileList[x]

        ## Modify to use glob
        inTree, inFlux, inEvt, nFiles, norm = get_chain(inFileName)

        ## Optional funky binning
        if isinstance(binning, str):
            inTree.Draw(plotVar+">>this_hist("+binning+")", norm+"*fScaleFactor*InputWeight*1E38*("+thisCut+")")
            thisHist = gDirectory.Get("this_hist")
            thisHist .SetDirectory(0)
        else:
            edges = array("d", binning)
            nbins = len(edges) - 1
            thisHist = TH1D("this_hist", "", nbins, edges)
            inTree.Draw(plotVar+">>this_hist", norm+"*fScaleFactor*InputWeight*1E38*("+thisCut+")")
            thisHist = gDirectory.Get("this_hist")
            thisHist .SetDirectory(0)
            
        ## Deal with different numbers of files
        if normType == "enu_ensemble":

            ## Normalize based on the input files
            print("Applying funky normalization... if you aren't using an ensemble of monoenergetic files... you messed up")
            thisNormHist = thisHist .Clone()
            thisNormHist .Reset()
            thisNormHist = mad_enu_norm_hist(inFileName, thisNormHist)
            thisHist .Divide(thisNormHist)

        elif normType == "nofluxaverage":
            thisHist.Scale(inFlux.Integral("width")/nFiles, "width")
        elif normType=="shape":
            thisHist .Scale(1/thisHist.Integral(0, -1))
        elif normType=="theta":
            thisHist .Scale(1/thisHist.GetBinContent(1), "width")            
        else:
            thisHist.Scale(1./nFiles, "width")
        
	## Retain for use
        thisHist .SetNameTitle("thisHist", "thisHist;"+labels)
        histList .append(thisHist)

    ## Sort out the plot colours
    for x in range(len(histList)):
        histList[x].SetLineColor(colzList[x])
        histList[x].SetLineStyle(lineList[x])

    return histList

def make_generator_comp(outPlotName, inFileList, nameList, colzList, lineList, \
                        plotVar="q0", binning="100,0,5", cut="cc==1", \
                        labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", \
                        legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], \
                        norm=None, withRebin=False, isLog=False, include_ratio=True, rat_title_num="Model", \
                        lineStyle="C"):

    ## Skip files that already exist
    if os.path.isfile(outPlotName):
        print("Skipping "+outPlotName, "which already exists!")
        return

    histList =  get_hist_list(inFileList, plotVar, binning, cut, labels, colzList, lineList, norm)
    ratList  = []

    ## Sort out the ratio hists
    nomHist = histList[0].Clone()
    if withRebin: nomHist .Rebin(2)
    for hist in histList:
        rat_hist = hist.Clone()
        if withRebin: rat_hist .Rebin(2)
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)
    
    ## This makes the plots in a standard form
    if include_ratio: make_two_panel_plot(outPlotName, histList, ratList, nameList, legDim, yLimits, yRatLimits, rat_title_num=rat_title_num, isLog=isLog, lineStyle=lineStyle)
    else: make_one_panel_plot(outPlotName, histList, nameList, legDim, yLimits, isLog=isLog, lineStyle=lineStyle)


## This subdivides the prediction of a single generator as required
def make_breakdown_comp(outPlotName, inFileList, legHeader, nameList, colzList, lineList, \
                        plotVar, binning, cutList, \
			labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)", \
			legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0, 1.05], \
			norm=None, withRebin=True, isLog=False, include_ratio=True, rat_title_num="Channel", \
                        lineStyle="C"):

    ## Skip files that already exist
    if os.path.isfile(outPlotName):
        print("Skipping "+outPlotName, "which already exists!")
        return

    histList = []
    ratList  = []
    nFile = len(inFileList)

    histList =  get_hist_list(inFileList, plotVar, binning, cutList, labels, colzList, lineList, norm)

    ## Sort out the ratio hists
    nomHist = histList[0].Clone()
    if withRebin: nomHist .Rebin(2)
    for hist in histList:
        rat_hist = hist.Clone()
        if withRebin: rat_hist .Rebin(2)
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)

    ## This makes the plots in a standard form
    if include_ratio: make_two_panel_plot(outPlotName, histList, ratList, nameList, legDim, yLimits, yRatLimits, rat_title_num=rat_title_num, legHeader=legHeader, lineStyle=lineStyle)
    else: make_one_panel_plot(outPlotName, histList, nameList, legDim, yLimits, legHeader=legHeader, lineStyle=lineStyle)
    

def make_generator_ratio_comp(outPlotName, inFileNumList, inFileDenList, nameList, colzList, lineList, \
                              plotVar="q0", binning="100,0,5", cut="cc==1", \
                              labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                              legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], include_ratio=True, withRebin=False):

    ## Skip files that already exist
    if os.path.isfile(outPlotName):
        print("Skipping "+outPlotName, "which already exists!")
        return
    
    histList    = []
    ratList     = []
    histNumList = get_hist_list(inFileNumList, plotVar, binning, cut, labels, colzList, lineList, isEnu=True)
    histDenList = get_hist_list(inFileDenList, plotVar, binning, cut, labels, colzList, lineList, isEnu=True)
    
    ## Make the first ratio
    for x in range(len(histNumList)):
        rat_hist = histNumList[x].Clone()
        rat_hist .Divide(histDenList[x])
        histList .append(rat_hist)        
    
    ## Sort out the ratio hists
    nomHist = histList[0].Clone()
    if withRebin: nomHist .Rebin(2)
    for hist in histList:
        rat_hist = hist.Clone()
        if withRebin: rat_hist .Rebin(2)
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)
    
    ## This makes the plots in a standard form
    if include_ratio: make_two_panel_plot(outPlotName, histList, ratList, nameList, legDim, yLimits, yRatLimits, topMidLine=True)
    else: make_one_panel_plot(outPlotName, histList, nameList, legDim, yLimits, topMidLine=True)

    
def make_A_over_BC_comp(outPlotName, inFileListA, inFileListB, inFileListC, nameList, colzList, lineList, \
                        plotVar="q0", binning="100,0,5", cut="cc==1", \
                        labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                        legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6], include_ratio=True, withRebin=False):

    ## Skip files that already exist
    if os.path.isfile(outPlotName):
        print("Skipping "+outPlotName, "which already exists!")
        return

    histList  = []
    ratList   = []
    histListA = get_hist_list(inFileListA, plotVar, binning, cut, labels, colzList, lineList, False, False)
    histListB = get_hist_list(inFileListB, plotVar, binning, cut, labels, colzList, lineList, False, False)
    histListC = get_hist_list(inFileListC, plotVar, binning, cut, labels, colzList, lineList, False, False)
    
    ## Make the first ratio
    for x in range(len(histListA)):
        rat_hist = histListA[x].Clone()
        den_hist = histListB[x].Clone()
        den_hist .Add(histListC[x])
        rat_hist .Divide(den_hist)
        histList .append(rat_hist)

    ## Sort out the ratio hists
    nomHist = histList[0].Clone()
    if withRebin: nomHist .Rebin(2)
    for hist in histList:
        rat_hist = hist.Clone()
        if withRebin: rat_hist .Rebin(2)
        rat_hist .Divide(nomHist)
        ratList  .append(rat_hist)

    ## This makes the plots in a standard form
    if include_ratio: make_two_panel_plot(outPlotName, histList, ratList, nameList, legDim, yLimits, yRatLimits, topMidLine=False, lineStyle="")
    else: make_one_panel_plot(outPlotName, histList, nameList, legDim, yLimits, topMidLine=False, lineStyle="")

    
    
## The double ratio is (A/B)/(C/D)
def make_generator_double_ratio_comp(outPlotName, inFileListA, inFileListB, inFileListC, inFileListD, \
                                     nameList, colzList, plotVar, binning, cut="cc==1", \
                                     labels="q_{0} (GeV); d#sigma/dq_{0} (#times 10^{-38} cm^{2}/nucleon)",
                                     legDim=[0.65, 0.5, 0.85, 0.93], yLimits=[0, None], yRatLimits=[0.4, 1.6]):
    
    ## Skip files that already exist
    if os.path.isfile(outPlotName):
        print("Skipping "+outPlotName, "which already exists!")
        return

    isLog = False
    histListA = get_hist_list(inFileListA, plotVar, binning, cut, labels, colzList, lineList)
    histListB = get_hist_list(inFileListB, plotVar, binning, cut, labels, colzList, lineList)
    histListC = get_hist_list(inFileListC, plotVar, binning, cut, labels, colzList, lineList)
    histListD = get_hist_list(inFileListD, plotVar, binning, cut, labels, colzList, lineList)

    ## The combinations
    histListAB   = []
    histListCD   = []
    histListABCD = []
    ratListABCD  = []

    nHists     = len(inFileListA)
    
    ## Binning info
    fine_binning="200,0,2"
    bin_arr = array('d', binning)
    nbins = len(binning)-1
    
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

    ## Sort out the plot colours
    for x in range(nHists): histListABCD[x].SetLineColor(colzList[x])

    ## Sort out the ratio hists
    nomHist = histListABCD[0].Clone()
    for hist in histListABCD:
        rat_hist = hist.Clone()
        rat_hist .Divide(nomHist)
        ratListABCD  .append(rat_hist)
    
    ## This makes the plots in a standard form
    make_two_panel_plot(outPlotName, histListABCD, ratListABCD, nameList, legDim, yLimits, yRatLimits, topMidLine=True)
