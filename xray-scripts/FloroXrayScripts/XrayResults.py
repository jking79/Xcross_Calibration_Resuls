##USAGE: This script takes 6 parameters (1-3: the names of the root files [materials Mo,Ag,Sn], 4: the name of the histogram (qplot), 5: the number of rocs in the module, 6: the common name of the outputfiles [MODULEID+DATE]) 
# python XrayResults.py MoXRaysNov14.root AgXRaysNov14.root SnXRaysNov14.root  Xray/q 5 M_IDNov14 
import sys
import glob
import re
import os
import numpy as np
from array import * 
from ROOT import *
#To get rid of the polymarkers of the Spectrum method, use the option ='goff' in the search function

def get_gpeaks(h,lrange=[0,150],sigma=6,opt="goff",thres=5,niter=1000):
    s = TSpectrum(niter,1)
    h.GetXaxis().SetRange(lrange[0],lrange[1])
    s.Search(h,sigma,opt,thres)
    s.SetAverageWindow(2)
    bufX, bufY = s.GetPositionX(), s.GetPositionY()
    pos = []
    for i in range(s.GetNPeaks()):
        pos.append([bufX[i], bufY[i]])
    pos.sort()
    return pos

#call this function as in Fitter.py (needs the arguments) 
#This function will get the peaks and fit them and save the stat info in .txt files per Material and Roc 
def FitPeaks(rootfile,histo,material,nrocs,output):
    arrayMo = false
    arrayAg = false
    arraySn = false
    ArrayG = TObjArray(int(nrocs))
    if material == 'Mo':
        arrayMo = true
        ArrayMo = TObjArray(int(nrocs))
    elif material == 'Ag':
        arrayAg = true
        ArrayAg = TObjArray(int(nrocs))
    elif material == 'Sn':
        arraySn =true
        ArraySn = TObjArray(int(nrocs))
    #arraytgt= TH1F[int(nrocs)] 
    for i in range(0,int(nrocs)-1):
        stats= open(output+material+'C_'+str(i)+'_stats.txt','w')
        hist = histo +str(i)+"_V0"
        tgt = rootfile.Get(hist)
        print "Opening file:" + hist
        #tgt = hist
        tgt.Rebin(2)
        tgt.Draw()
        tgt.GetXaxis().SetRange(0,150)
        peaks = get_gpeaks(tgt)
        #print len(peaks)
        mid1 = peaks[0][1]
        mid2 = peaks[1][1]
        if(len(peaks)>3):
            print "Too many peaks"
            break  
        if (len(peaks)==2):
            for t in range(1, int(peaks[0][0])):
                if (tgt.GetBinContent(t)/mid1>0.68):
                    sigma1l = t 
                    break
            for j in range(int(peaks[0][0])+1,int(peaks[1][0])):
                if (tgt.GetBinContent(j)/mid1<0.68):
                    sigma1r = j
                    break
            for l in range(int(peaks[1][0])+1,300):
                if (tgt.GetBinContent(l)/mid2<0.68):
                    sigma2r = l
                    break
            for k in range(int(peaks[0][0])+(sigma1r)/2,int(peaks [1][0])):
                if (tgt.GetBinContent(k)/mid2>0.68) and abs(k-peaks[1][0])<20:
                    sigma2l = k
                    break
        if(len(peaks)==3):
            if peaks[1][1] > peaks[2][1]:
                mid3 = peaks[1][1]
                right3 = int(peaks[1][0])
                for t in range(1, int(peaks[0][0])):
                    if (tgt.GetBinContent(t)/mid1>0.68):
                        sigma1l = t 
                        break
                for j in range(int(peaks[0][0])+1,right3):
                    if (tgt.GetBinContent(j)/mid1<0.68):
                        sigma1r = j
                        break
                for l in range(right3+1,300):
                    if (tgt.GetBinContent(l)/mid3<0.68):
                        sigma2r = l
                        break
                for k in range(int(peaks[0][0])+(sigma1r)/2,right3):
                    if (tgt.GetBinContent(k)/mid3>0.68):
                        sigma2l = k
                        if abs(k-right3)< 20:
                            break
            else:
                mid3 = peaks[2][1] 
                right3 = int(peaks[2][0])
                for t in range(1, int(peaks[0][0])):
                    if (tgt.GetBinContent(t)/mid1>0.68):
                        sigma1l = t 
                        break
                for j in range(int(peaks[0][0])+1,int(peaks[1][0])):
                    if (tgt.GetBinContent(j)/mid1<0.68):
                        sigma1r = j
                        break
                for l in range(right3+1,300):
                    if (tgt.GetBinContent(l)/mid3<0.68):
                        sigma2r = l
                        break
                for k in range(int(peaks[1][0])+(sigma1r)/2,right3):
                    if (tgt.GetBinContent(k)/mid3>0.68) and abs(k-right3)<20:
                        sigma2l = k
                        break
        gaus1 = TF1("gaus1","gaus",peaks[0][0]-15, peaks[0][0]+15)
        #gaus2 = TF1("gaus2","gaus",sigma2l, sigma2r)
        if len(peaks)==2: gaus2 = TF1("gaus2","gaus",peaks[1][0]-15,peaks[1][0]+15)
        if len(peaks)==3:
            if peaks[1][1]>peaks[2][1]:
                gaus2 = TF1("gaus2","gaus",peaks[1][0]-20,peaks[1][0]+20)
            else:
                gaus2 = TF1("gaus2","gaus",peaks[2][0]-20,peaks[2][0]+20)
        #gaus1 = TF1("gaus1","gaus",sigma1l, sigma1r)
        #gaus2 = TF1("gaus2","gaus",sigma2l, sigma2r)
        tgt.Fit("gaus1","R")
        tgt.Fit("gaus2","+R")
        tgt.Draw()
        c1.Update()
        mu1 = tgt.GetFunction("gaus1").GetParameter(1)
        mu2 = tgt.GetFunction("gaus2").GetParameter(1)
        sigma1 = tgt.GetFunction("gaus1").GetParameter(2)
        sigma2 = tgt.GetFunction("gaus1").GetParameter(2)
        print mu1 , sigma1, mu2, sigma2
        c1.SaveAs(output+'FitC_'+str(i)+material+'.png')
        stats.writelines(["Mean_Cu_C"+str(i)+":\t"+str(mu1)+"\n", "Sigma_Cu_C"+str(i)+":\t"+str(sigma1)+"\n","Mean_"+material+"_C"+str(i)+":\t"+str(mu2)+"\n", "Sigma_"+material+"_C"+str(i)+":\t"+str(sigma2)+"\n"])
        if arrayMo:
            ArrayMo.AddAt(tgt,i)
        elif arrayAg:
            ArrayAg.AddAt(tgt,i)
        elif arraySn:
            ArraySn.AddAt(tgt,i)
    if arrayMo:
        ArrayG = ArrayMo
    elif arrayAg:
        ArrayG = ArrayAg
    elif arraySn:
        ArrayG = ArraySn
    return ArrayG

def PlotSameNStats(arrayfithisto1, arrayfithisto2, arrayfithisto3, nrocs, output): #need to check the arguments (root files) 
    for i in range(0,int(nrocs)-1):
        fithisto1 = arrayfithisto1[i]
        fithisto2 = arrayfithisto2[i]
        fithisto3 = arrayfithisto3[i]
        #material1 = rootfile1.strip('XRays')
        #material2 = rootfile2.strip('XRays')
        #material3 = rootfile3.strip('XRays')
        #hist1 = histname+"_"+material1+"_C"+str(i)+"_V0"
        #hist2 = histname+"_"+material2+"_C"+str(i)+"_V0"
        #hist2 = histname+"_"+material2+"_C"+str(i)+"_V0"
        #tgt1 = rootfile1.Get(hist1)
        #tgt2 = rootfile2.Get(hist2)
        #tgt3 = rootfile3.Get(hist3)
        c1 = TCanvas('c1',"Fluorescence test",1)
        gStyle.SetOptStat(0)
        fithisto1.GetXaxis().SetRange(0,150)
        fithisto2.GetXaxis().SetRange(0,150)
        fithisto3.GetXaxis().SetRange(0,150)
        fithisto1.SetLineColor(kBlue)
        fithisto2.SetLineColor(kMagenta)
        fithisto3.SetLineColor(kGreen)
        c1.cd()
        #c1.SetTitle("Single Roc Fluorescence tests")
        gStyle.SetOptTitle(0)
        #stat1 = fithistos1.FindObject("stats")
        mu1f = fithisto1.GetFunction("gaus2").GetParameter(1)
        sigma1f = fithisto1.GetFunction("gaus2").GetParameter(2)
        mu2f = fithisto2.GetFunction("gaus2").GetParameter(1)
        sigma2f = fithisto2.GetFunction("gaus2").GetParameter(2)
        mu3f = fithisto3.GetFunction("gaus2").GetParameter(1)
        sigma3f = fithisto3.GetFunction("gaus2").GetParameter(2)
        mu1 = float("{0:.2f}".format(mu1f))
        mu2 = float("{0:.2f}".format(mu2f))
        mu3 = float("{0:.2f}".format(mu3f))
        sigma1 = float("{0:.2f}".format(sigma1f))
        sigma2 = float("{0:.2f}".format(sigma2f))
        sigma3 = float("{0:.2f}".format(sigma3f))
        #tgtpeaks1 = tgt1.FitPeaks()
        #tgtpeaks2 = tgt2.FitPeaks()
        #tgtpeaks3 = tgt3.FitPeaks()
        fithisto1.Draw()
        c1.Update()
        textmu1 = TLatex()
        textmu1.SetNDC()
        textmu1.SetTextColor(kBlue)
        textmu1.SetTextSize(0.03)
        textmu1.DrawText(0.7,0.3,"Mo.Mean():"+ str(mu1))
        textsigma1 = TLatex()
        textsigma1.SetNDC()
        textsigma1.SetTextColor(kBlue)
        textsigma1.SetTextSize(0.03)
        textsigma1.DrawText(0.7,0.2,"Mo.Sigma():"+ str(sigma1))
        c1.Update()
        #gStyle.SetOptStat(1101)
        #stat1 = fithisto1.FindObject("stats")
        #stat1.SetX1NDC(0.70)
        #stat1.SetX2NDC(0.90)
        #stat1.SetY1NDC(0.10)
        #stat1.SetY2NDC(0.30)
        #stat1.SetTextColor(kBlue)
        fithisto2.Draw("sames")
        textmu2 = TLatex()
        textmu2.SetNDC()
        textmu2.SetTextColor(kMagenta)
        textmu2.SetTextSize(0.03)
        textmu2.DrawText(0.7,0.5,"Ag.Mean():"+ str(mu2))
        textsigma2 = TLatex()
        textsigma2.SetNDC()
        textsigma2.SetTextColor(kMagenta)
        textsigma2.SetTextSize(0.03)
        textsigma2.DrawText(0.7,0.4,"Ag.Sigma():"+ str(sigma2))
        c1.Update()
        #gStyle.SetOptStat(1101)
        #stat2 = fithisto2.FindObject("stats")
        #stat2.SetX1NDC(0.70)
        #stat2.SetX2NDC(0.90)
        #stat2.SetY1NDC(0.30)
        #stat2.SetY2NDC(0.50)
        #stat2.SetTextColor(kMagenta)
        fithisto3.Draw("sames")
        textmu3 = TLatex()
        textmu3.SetNDC()
        textmu3.SetTextColor(kGreen)
        textmu3.SetTextSize(0.03)
        textmu3.DrawText(0.7,0.7,"Sn.Mean():"+ str(mu3))
        textsigma3 = TLatex()
        textsigma3.SetNDC()
        textsigma3.SetTextColor(kGreen)
        textsigma3.SetTextSize(0.03)
        textsigma3.DrawText(0.7,0.6,"Sn.Sigma():"+ str(sigma3))
        c1.Update()
        #gStyle.SetOptStat(1101)
        #stat3 = fithisto3.FindObject("stats")
        #stat3.SetX1NDC(0.70)
        #stat3.SetX2NDC(0.90)
        #stat3.SetY1NDC(0.50)
        #stat3.SetY2NDC(0.70)
        #stat3.SetTextColor(kGreen)
        text = TLatex()
        text.SetNDC()
        text.DrawText(0.4,0.95,"Fluorescence tests C_"+str(i))
        print 'Saving to:', output
        c1.SaveAs(output+"XRayFluoResultsC_"+str(i)+'.png')
        c1.Close()
    return 

def ConversionPlot(nrocs,output):
    convfactcu = 8048/3.6
    convfactmo = 17479/3.6
    convfactag = 22163/3.6
    convfactsn= 25271/3.6
    #qplotfit = open("SummaryQplots.txt",'w')
    n_oh = TH1F('n_oh','N_o', 100,-2000,-1000)
    slopeh = TH1F('Slope','Slope',100, 0,100)
    for i in range(0,int(nrocs)-1):
        mu_cu =[]
        sig_cu=[]
        mu_mo = []
        sig_mo = []
        mu_ag =[]
        sig_ag =[]
        mu_sn =[]
        sig_sn = []
        mu_in =[]
        sig_in = []
        for file in glob.glob("*"+str(i)+"_stats.txt"):
        #for file in os.getcwd():
            #if file.endswith (str(i)+)
            name = os.path.splitext(file)[0]
            print "Opening:",name
            #material = name.strip('_stats')
            #if(material == 'Mo'):
            if('MoC_' in name):
                material = 'Mo'
                f = open(file,'r')
                line = f.readlines()
                for k in range(0,len(line)):
                    if "_Cu" in line[k]:
                        if "Mean_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            meancu = words[1].strip('\n')
                            mu_cu.append(meancu)
                        elif "Sigma_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            sigmacu = words[1].strip('\n') 
                            sig_cu.append(sigmacu)   
                    else:
                        if "Mean_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            mean = words[1].strip('\n')
                            mu_mo.append(mean)
                        elif "Sigma_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            sigma = words[1].strip('\n')
                            sig_mo.append(sigma)
                f.close()               
            elif('AgC_' in name):
                material = 'Ag'
                f = open(file,'r')
                line = f.readlines()
                for k in range(0,len(line)):
                    if "_Cu" in line[k]:
                        if "Mean_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            meancu = words[1].strip('\n')
                            mu_cu.append(meancu)
                        elif "Sigma_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            sigmacu = words[1].strip('\n') 
                            sig_cu.append(sigmacu)   
                    else:
                        if "Mean_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            mean = words[1].strip('\n')
                            mu_ag.append(mean)
                        elif "Sigma_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            sigma = words[1].strip('\n')
                            sig_ag.append(sigma)
                f.close()
            elif('SnC_' in name):
                material = 'Sn'
                convfact= 25271/3.6
                f = open(file,'r')
                line = f.readlines()
                for k in range(0,len(line)):
                    if "_Cu" in line[k]:
                        if "Mean_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            meancu = words[1].strip('\n')
                            mu_cu.append(meancu)
                        elif "Sigma_Cu" in line[k]:
                            words =  re.split(':\t',line[k])
                            sigmacu = words[1].strip('\n') 
                            sig_cu.append(sigmacu)   
                    else:
                        if "Mean_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            mean = words[1].strip('\n')
                            mu_sn.append(mean)
                        elif "Sigma_"+material in line[k]:
                            words =  re.split(':\t',line[k])
                            sigma = words[1].strip('\n')
                            sig_sn.append(sigma)
                f.close()
        n_cu = len(mu_cu)
        n_mo = len(mu_mo)
        n_ag = len(mu_ag)
        n_sn = len(mu_sn)
        n_all = n_cu + n_mo + n_ag + n_sn
        sigma_y = [0]*n_all
        mus = mu_cu +mu_mo + mu_ag + mu_sn
        sigma_x = sig_cu + sig_mo + sig_ag+ sig_sn
        k_cu = [convfactcu]*n_cu
        k_mo = [convfactmo]*n_mo
        k_ag = [convfactag]*n_ag
        k_sn = [convfactsn]*n_sn
        k = k_cu + k_mo + k_ag+ k_sn
        matrix = np.zeros(((len(mus)),4))
        for j in range(0,len(mus)):
            matrix[j][0] = float(mus[j])
            matrix[j][1] = float(k[j])
            matrix[j][2] = float(sigma_x[j])
        table = open('SummaryTable'+'C_'+str(i)+'.txt','w')
        np.savetxt("SummaryTable"+"C_"+str(i)+".txt",matrix, delimiter="\t", fmt="%s", newline='\n' )
        gStyle.SetOptFit(1)
        c1 = TCanvas('c1',"Fluorescence test",1)
        c1.cd()
        c1.Update()
        gr = TGraphErrors("SummaryTable"+"C_"+str(i)+".txt")
        gr.SetMarkerStyle(41)
        fit = TF1("fit","pol1",0,300)
        gr.Fit("fit","w","l",0,300)
        gr.SetMarkerStyle(20)
        n_o = gr.GetFunction("fit").GetParameter(0)
        print "no:",n_o
        slope = gr.GetFunction("fit").GetParameter(1)
        print "slope:",slope
        gr.Draw("AP")
        gr.GetXaxis().SetRange(0,300)
        gr.GetYaxis().SetRange(0,8000)
        gr.GetXaxis().SetTitle("Vcal")
        gr.GetYaxis().SetTitle("No.Electrons")
        c1.Update()
        gr.Draw("AP")
        ps = c1.FindObject("Graph").FindObject("stats")
        ps.SetX1NDC(0.15)
        ps.SetX2NDC(0.55)
        c1.SetGrid()
        c1.Update()
        c1.SaveAs('QplotC_'+str(i)+'.png')
        c1.Close()
        ##get q value of fit and error and add them to a table then use TGraphError to make a distribution of them 
        n_oh.Fill(n_o)
        slopeh.Fill(slope)
    c2 = TCanvas('c2',"Distribution N_o",1)
    c2.cd()
    gStyle.SetOptStat(1)
    n_oh.Draw()
    n_oh.SetStats(1)
    c2.Update()
    ps2 = n_oh.GetListOfFunctions().FindObject("stats")
    n_oh.Draw()
    c2.Update()
    #ps2.SetX1NDC(0.15)
    #ps2.SetX2NDC(0.55)
    c2.SaveAs(output+'Distribution_NoEle.png')
    c3 = TCanvas('c3',"Distribution N_o",1)
    c3.cd()
    gStyle.SetOptStat(1)
    slopeh.Draw()
    slopeh.SetStats(1)
    c3.Update()
    slopeh.GetXaxis().SetTitle("p1[Vcal/No.Ele]")
    slopeh.GetYaxis().SetTitle("Entries")
    slopeh.Draw()
    c3.Update()
    c3.SaveAs(output+'Distribution_Slope.png')
    return  

##MAIN###
rootfile1 = TFile(sys.argv[1]) 
rootfile2 = TFile(sys.argv[2])
rootfile3 = TFile(sys.argv[3])
histname = sys.argv[4]
nrocs = sys.argv[5]
output = sys.argv[6]
rootfile1name = sys.argv[1]
rootfile2name = sys.argv[2]
rootfile3name = sys.argv[3]
material1 = 'Mo'
material2 = 'Ag'
material3 = 'Sn'
hist1 = histname+"_"+material1+"_C"
hist2 = histname+"_"+material2+"_C"
hist3 = histname+"_"+material3+"_C"
Arraytgt1 = FitPeaks(rootfile1,hist1,material1,nrocs,output)
Arraytgt2 = FitPeaks(rootfile2,hist2,material2,nrocs,output)
Arraytgt3 = FitPeaks(rootfile3,hist3,material3,nrocs,output)
PlotSameNStats(Arraytgt1,Arraytgt2,Arraytgt3,nrocs,output)
ConversionPlot(nrocs, output) 

