import sys
from ROOT import *

def rotatehist(hist):
 hnew = hist.Clone()
 nbinsx = hist.GetNbinsX()
 nbinsy = hist.GetNbinsY()
 for x in range(1,nbinsx+1):
  for y in range(1,nbinsy+1):
   hist.SetBinContent(x,y, hnew.GetBinContent( nbinsx - x + 1, nbinsy - y + 1 ))

rootfile = TFile(sys.argv[1])
histname = sys.argv[2]
output = sys.argv[3]

print 'Opening ROOT File:',sys.argv[1]
print 'Grabbing hists:', histname


c1 = TCanvas('c1','',416*2,160*2)
c1.Divide(8,2,0.0,0.0)

gStyle.SetOptStat(0)

hists = {}

for num in range(0,5):
 hist = histname.split('#')[0]+str(num)+histname.split('#')[1]
 if num < 8:
  padnum = num + 9
  c1.cd(padnum)
  #rootfile.Get(hist).Draw('Acol')
  rootfile.Get(hist).Draw()
 else:
  padnum = 16 - num
  hists[padnum] = rootfile.Get(hist).Clone()
  rotatehist(hists[padnum])
  c1.cd(padnum)
  #hists[padnum].Draw('Acol')
  hist[padnum].Draw()


print 'Saving to:', output

c1.SaveAs(output)
