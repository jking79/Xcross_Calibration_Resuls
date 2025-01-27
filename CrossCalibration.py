print "Loading Root..."

#import pdb; pdb.set_trace()
import os
import re
from optparse import OptionParser
from ROOT import *
gROOT.Macro("$HOME/.rootlogon.C")
gROOT.SetBatch()
gStyle.SetOptStat("n")
gStyle.SetCanvasColor(kWhite)

parser = OptionParser()
parser.add_option("-f", "--files", dest="files", default="crosscalibrate_KU.root,crosscalibrate_UNL.root", help="List of input files (file1.root,file2.root)")
##"mtt922datafnal/CrossCalibration.root,mtt922data/CrossCalibration.root,./mtt922dataUNL/crosscalibrate.root,./mtt922datapurdue/crosscalibrate_2.root"
parser.add_option("-l", "--legend", dest="legend", default="KU,UNL", help="Legend label for each file (file1,file2)")
##default="FNAL,KU,UNL,Purdue"
parser.add_option("-c", "--colors", dest="colors", default="1,2,4,7,3,6,5,9,8", help="Set the histogram colors for each input file (1,2,4)")
parser.add_option("-o", "--outputdir", dest="outputdir", default="CrossCalibration", help="Output directory for all the PNG files")
parser.add_option("-s", "--select", dest="select", default="", help="Compare only plots that match the regular expression (Pretest*)")
parser.add_option("-v", "--veto", dest="veto", default="", help="Veto plots that match the regular expression (Pretest*)")
parser.add_option("--log", action="store_true", dest="log", default="False", help="Change to log scale")
(options, args) = parser.parse_args()

options.outputdir += "/"
if not os.path.isdir(options.outputdir): os.mkdir(options.outputdir)

can = TCanvas("Plots","Plots",850,650)
if options.log is True: can.SetLogy(1)

if options.legend!="":
    doleg = True
    leg = TLegend(0.65, 0.8, 0.9, 0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(1)
else: doleg = False

Legends = options.legend.split(",")
colors = options.colors.split(",")
for i in range(len(colors)): colors[i] = int(colors[i])

filelist=[]
for filename in options.files.split(","): filelist.append(TFile(filename))

def GetRanges(histname, filelist):
    maximum=0
    xmin=1000
    xmax=0
    for file in filelist:
        hist = file.Get(histname)
        maximum = max(maximum,hist.GetMaximum())
        for bin in range(1,hist.GetNbinsX()+1):
            if hist.GetBinContent(bin)>0:
                xmin=min(xmin,hist.GetBinLowEdge(bin))
                break
        for bin in range(hist.GetNbinsX()+1,0,-1):
            if hist.GetBinContent(bin)>0:
                xmax=max(xmax,hist.GetBinLowEdge(bin))
                break
    return maximum,xmin,xmax
    
def CompareTH1(histname, filelist):
    can.Clear()
    (maximum, xmin, xmax) = GetRanges(histname, filelist)
    for i in range(len(filelist)):
        hist = filelist[i].Get(histname)
        if histname.find("BumpBonding")!=-1 and filelist[i].GetName().find("mtt922dataUNL")!=-1: hist = filelist[i].Get(histname.replace("V0","V1"))
        hist.SetStats(0)
        hist.SetLineColor(colors[i])
        if options.log is True:
            hist.SetMinimum(0.1)
            scale=2
        else:
            scale=1.2
        if i==0:
            hist.SetMaximum(maximum*scale)
            hist.GetXaxis().SetRangeUser(xmin-2,xmax+2)
            hist.Draw("hist")
        else:
            hist.Draw("same hist")
        if doleg is True: leg.AddEntry(hist,Legends[i])
    
    if doleg is True: leg.Draw()
    outputfile = histname.replace("/","_")+".png"
    if options.log is True: outputfile = outputfile.replace(".png","_log.png")
    can.SaveAs(options.outputdir+outputfile)
    leg.Clear()

def CompareTH2(histname, filelist):
    can.Clear()
    basehist = filelist[0].Get(histname)
    outputhistlist=[]
    minvalue = 1000
    maxvalue = -1000
    maximum = 0
    for i in range(1,len(filelist)):
        outputhist = TH1D("CompareHist"+str(i),basehist.GetTitle()+";"+"#DeltaValue"+";",2001,-1000,1000)
        outputhistlist.append(outputhist)
        histnum = i-1
        testhist = filelist[i].Get(histname)
        if histname.find("BumpBonding")!=-1 and filelist[i].GetName().find("mtt922dataUNL")!=-1: testhist = filelist[i].Get(histname.replace("V0","V1"))
        outputhistlist[histnum].SetLineColor(colors[histnum])
        for ixbin in range(basehist.GetNbinsX()):
            for iybin in range(basehist.GetNbinsY()):
                basevalue = basehist.GetBinContent(ixbin,iybin)
                testvalue = testhist.GetBinContent(ixbin,iybin)
                if basevalue==0 and testvalue==0: continue
                value = testvalue-basevalue
                minvalue = min(minvalue,value)
                maxvalue = max(maxvalue,value)
                outputhistlist[histnum].Fill(value)
        if options.log is True: outputhistlist[histnum].SetMinimum(0.1)
        if doleg is True: leg.AddEntry(outputhistlist[histnum],Legends[i]+"-"+Legends[0])
        outputhistlist[histnum].SetStats(0)
        maximum = max(maximum,outputhistlist[histnum].GetMaximum())
    for i in range(len(outputhistlist)):
        outputhistlist[i].GetXaxis().SetRangeUser(minvalue-2,maxvalue+2)
        if options.log is True: outputhistlist[i].SetMaximum(2*maximum)
        else: outputhistlist[i].SetMaximum(1.2*maximum)
        if i==0: outputhistlist[i].Draw()
        else: outputhistlist[i].Draw("same")
    if doleg is True: leg.Draw()
    outputfile = histname.replace("/","_")+".png"
    if options.log is True: outputfile = outputfile.replace(".png","_log.png")
    can.SaveAs(options.outputdir+outputfile)
    leg.Clear()

def CompareTH2dumb(histname, filelist):
    basehist = filelist[0].Get(histname)
    for i in range(1,len(filelist)):
        testhist = filelist[i].Get(histname)
        testhist.Add(basehist,-1)
        testhist.Draw("colz")
        if doleg: outputfile = histname.replace("/","_")+"_"+Legends[i]+".png"
        else: outputfile = histname.replace("/","_")+"_"+filelist[i].GetName()[:filelist[i].GetName().find(".root")]+".png"
        if options.log is True: outputfile = outputfile.replace(".png","_log.png")
        can.SaveAs(options.outputdir+outputfile)
        
for dir in filelist[0].GetListOfKeys():
    if dir.GetClassName().find("TDirectory")!=-1:
        for histkey in filelist[0].Get(dir.GetName()).GetListOfKeys():
            hist = dir.GetName()+"/"+histkey.GetName()
            CompareHist = True
            for file in filelist:
                if file.Get(hist) == None: CompareHist=False
            if not CompareHist: continue
            select = re.search(options.select,hist)
            veto = re.search(options.veto,hist)
            if options.select!="" and SXselect is None: continue
            if options.veto!="" and veto is not None: continue
            histtype = histkey.GetClassName()
            if histtype.find("TH1")!=-1: CompareTH1(hist, filelist)
            if histtype.find("TH2")!=-1: CompareTH2(hist, filelist)
                #if options.log is not True: CompareTH2dumb(hist, filelist)

print "Done!"
