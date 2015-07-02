##USAGE: This script takes 6 parameters (1-3: the names of the root files [materials Mo,Ag,Sn], 4: the name of the histogram (qplot), 5: the number of rocs in the module, 6: the common name of the outputfiles [MODULEID+DATE]) 
# python XrayResults.py CuXRaysNov14.root AgXRaysNov14.root SnXRaysNov14.root  Xray/q 5 M_IDNov14 

import sys
import glob
import re
import os
import numpy as np
from array import * 
from ROOT import *

module = 'N00601'
filmlist = [ 'Cu', 'Ag', 'Sn', 'In' ] 	# list of films used where TFile name should be "floroCu40.root" as an example
histname = 'Xray/q' 			# with subdirectory for q hist in TFile
nrocs = 16 				# should not change unless a roc is disabled
startroc = 0				# should not change unless a roc disabled
fitwidth = 8
output = "XrayFloroResults" 		# or whatever you would like it to be
prestring = 'floro'  			# of TFile name where TFile name should be "floroCu40.root" as an example
poststring = '35.root' 			# of TFile name where TFile name should be "floroCu40.root" as an example
rootfilename0 = 'FloroXRay.root' ##module + '_XR_FL.root'

# if filmlist is changed these two functions need to be modified appratlly
def mycolor( ele ):
	
	if ele == 'Cu':	
		return kGreen
	elif ele == 'Ag':
		return kBlue
	elif ele == 'Sn':
		return kRed
	elif ele == 'In':
		return kMagenta
	else:
		return kBlack

def mypos( ele ):
	
	if ele == 'Cu':	
		return 0.3
	elif ele == 'Ag':
		return 0.4
	elif ele == 'Sn':
		return 0.5
	elif ele == 'In':
		return 0.6
	else:
		return 0.7


#To get rid of the polymarkers of the Spectrum method, use the option ='goff' in the search function
def get_gpeaks(h,lrange=[0,190],sigma=3,opt="goff",thres=.2,niter=1000):

	print "--Finding Peaks----------------------------"

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
def fitPeaks(rootfile,histo,material,roc,output):

	print "-Fitting Spectrum Peaks----------------------------------------------------------------"

        c0 = TCanvas('c0',"Fluorescence Fits",1)
        stats= open(output+ '_' +material+'_C'+str(roc)+'_stats.txt','w')
        tgt = getHisto( rootfile, histo, material, roc )
        tgt.Draw()
        tgt.GetXaxis().SetRange(0,150)
        tgt.Draw()
        c0.Update()
        mu1 = tgt.GetFunction("gaus1").GetParameter(1)
        mu2 = tgt.GetFunction("gaus2").GetParameter(1)
        sigma1 = tgt.GetFunction("gaus1").GetParameter(2)
        sigma2 = tgt.GetFunction("gaus2").GetParameter(2)
        print mu1 , sigma1, mu2, sigma2
        c0.SaveAs(output+'xFit_' + material + '_C'+str(roc) +'_plot.png')
        c0.Close()
        stats.writelines(["Mean_Mo_C"+str(roc)+":\t"+str(mu1)+"\n",
				"Sigma_Mo_C"+str(roc)+":\t"+str(sigma1)+"\n",
					"Mean_"+material+"_C"+str(roc)+":\t"+str(mu2)+"\n", 
						"Sigma_"+material+"_C"+str(roc)+":\t"+str(sigma2)+"\n"])
        stats.close()
	
    	return tgt

#call this function as in Fitter.py (needs the arguments) 
#This function will get the peaks and fit them and save the stat info in .txt files per Material and Roc 
def getHisto(rootfile,histo,material,roc):

	print "-Finding Fitted Histogram-----------------------------------------------------"

	hist = histo +str(roc)+"_V0"
	tgt = rootfile.Get(hist)
	print "Opening file:" + hist
	tgt.Rebin(2)
	peaks = get_gpeaks(tgt)
	print 'Found ' + str(len(peaks)) + " peaks for Roc " + str(roc) + " with  " + material
	if material == "Cu":
		if len(peaks) == 2 :
			gaus2 = TF1("gaus2","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
			gaus1 = TF1("gaus1","gaus",peaks[1][0]-fitwidth,peaks[1][0]+fitwidth)
		elif len(peaks) == 3 :
			gaus2 = TF1("gaus2","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
			gaus1 = TF1("gaus1","gaus",peaks[2][0]-fitwidth,peaks[2][0]+fitwidth)
		elif len(peaks) == 1 :
                        gaus2 = TF1("gaus2","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
                        gaus1 = TF1("gaus1","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
	elif len(peaks) == 4:
		gaus1 = TF1("gaus1","gaus",peaks[2][0]-fitwidth,peaks[2][0]+fitwidth)
		gaus2 = TF1("gaus2","gaus",peaks[3][0]-fitwidth,peaks[3][0]+fitwidth)
	elif len(peaks) == 3:
		gaus1 = TF1("gaus1","gaus",peaks[1][0]-fitwidth,peaks[1][0]+fitwidth)
		gaus2 = TF1("gaus2","gaus",peaks[2][0]-fitwidth,peaks[2][0]+fitwidth)
	elif len(peaks) == 2:
		gaus1 = TF1("gaus1","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
		gaus2 = TF1("gaus2","gaus",peaks[1][0]-fitwidth,peaks[1][0]+fitwidth)
    	elif len(peaks) == 1:
        	gaus1 = TF1("gaus1","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
        	gaus2 = TF1("gaus2","gaus",peaks[0][0]-fitwidth,peaks[0][0]+fitwidth)
        

	tgt.Fit("gaus1","R")
	tgt.Fit("gaus2","+R")

	return tgt

def findStatsByEle( material , myfile):
	
	print "--Entering Find By Element Conversion Plots ----------------------------------------" 
	infile = open(myfile,'r')
	line = infile.readlines()
	for k in range(0,len(line)):
		if "Mo" in line[k]:
			if "Mean_Mo" in line[k]:
				words =  re.split(':\t',line[k])
				meanmo = words[1].strip('\n')
			elif "Sigma_Mo" in line[k]:
				words =  re.split(':\t',line[k])
				sigmamo = words[1].strip('\n')   
		else:
			if "Mean_"+material in line[k]:
				words =  re.split(':\t',line[k])
				mean = words[1].strip('\n')
			elif "Sigma_"+material in line[k]:
				words =  re.split(':\t',line[k])
				sigma = words[1].strip('\n')
	infile.close()
	print "Find by Ele Results Mo: mean:" + str( meanmo )+ " sigma:" + str( sigmamo ) + " " + material + ": mean:" + str( mean ) + " sigma:" + str (  sigma ) 
	return [ meanmo, sigmamo, mean, sigma ]


def drawConvPlotByRoc( nrocs, output ):

	print "-Entering Conversion plots by ROC ---------------------------------------------------------------"

	cfcu = 8048/3.6
	cfmo = 17479/3.6
	cfag = 22163/3.6
	cfin = 24209/3.6
	cfsn= 25272/3.6
					
	n_oh = TH1F('n_oh','No_Electrons', 10,0,1000)
	slopeh = TH1F('Slope','Slope',50, 20,70)
	moh = TH1F('moh','Mo_Peak',200, 0,200)


	for i in range(0,int(nrocs)):
		
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
		sigma_y = []
		mus = []
		sigma_x = []
		k = []
		vmatrix = []

		for myfile in glob.glob("*_C"+str(i)+"_stats.txt"):	

			name = os.path.splitext(myfile)[0]
			print "Opening:",name

			if('Cu' in name):
				result = findStatsByEle( 'Cu', myfile )
				#print result
				mu_mo.append(result[0])
				sig_mo.append(result[1])
				mu_cu.append(result[2])
				sig_cu.append(result[3])

			elif('Ag' in name):
				result = findStatsByEle( 'Ag', myfile )
				#print result
				mu_mo.append(result[0])
				sig_mo.append(result[1])
				mu_ag.append(result[2])
				sig_ag.append(result[3])

			elif('Sn' in name):
				result = findStatsByEle( 'Sn', myfile )
				#print result
				mu_mo.append(result[0])
				sig_mo.append(result[1])
				mu_sn.append(result[2])
				sig_sn.append(result[3])

			elif('In' in name):
				result = findStatsByEle( 'In', myfile )
				#print result
				mu_mo.append(result[0])
				sig_mo.append(result[1])
				mu_in.append(result[2])
				sig_in.append(result[3])

		print "Printing Summury Table for Roc " + str(i) 
		
		sigma_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		mus = mu_cu + mu_mo + mu_ag + mu_in + mu_sn
		sigma_x = sig_cu +  sig_mo + sig_ag+ sig_in + sig_sn
		k = [ cfcu, cfmo, cfmo, cfmo, cfmo, cfag, cfin, cfsn ]
		
		vmatrix = [ k, mus, sigma_y, sigma_x ]
		table = open('SummaryTable_C'+str(i)+'.txt','w')
		np.savetxt("SummaryTable_C"+str(i)+".txt",zip(*vmatrix), delimiter="\t", fmt="%s") 
		table.close()

		gStyle.SetOptFit(1)
		c1 = TCanvas('c1',"Fluorescence Summury",1)
		c1.cd()
		c1.Update()
		gr = TGraphErrors("SummaryTable_C"+str(i)+".txt")
		gr.SetMarkerStyle(41)
		fit = TF1("fit"+str(i),"pol1",1000,10000)
		gr.Fit("fit"+str(i),"w","l",1000,10000)
		gr.SetMarkerStyle(20)
		gr.Draw("AP")
		gr.GetYaxis().SetRange(0,300)
		gr.GetXaxis().SetRange(0,8000)
		gr.GetYaxis().SetTitle("Vcal")
		gr.GetXaxis().SetTitle("No.Electrons")
	
		slope = gr.GetFunction("fit"+str(i)).GetParameter(1)
		slope_err = gr.GetFunction("fit"+str(i)).GetParError(1)
		slopeh.Fill(1.0/slope) 
		print "slope:",(1.0/slope)		
		n_o = gr.GetFunction("fit"+str(i)).GetParameter(0)
		n_oh.Fill(-n_o/slope)
		print "no:",(-n_o/slope)
		

		c1.Update()
		gr.Draw("AP")
		ps = c1.FindObject("Graph").FindObject("stats")
		ps.SetX1NDC(0.15)
		ps.SetX2NDC(0.55)
		c1.SetGrid()
		textslope = TLatex()
		textslope.SetNDC()
		textslope.SetTextColor(kBlue)
		textslope.SetTextSize(0.03)
		textslope.DrawLatex(0.3,0.7,"C" + str(i)+" : e^{-}/Vcal:"+ '{0:.4}'.format(1./slope) + " +/- " + '{0:.4}'.format((slope_err)/pow(slope,2)))
		c1.Update()
		c1.SaveAs('QplotC'+str(i)+'_2.png')
		c1.Close()
		##get q value of fit and error and add them to a table then use TGraphError to make a distribution of them 
			
		for val in mu_mo:	
			moh.Fill( float(val)  )

	print "Conversion plots by Roc returning with values: "	
	print n_oh
	print slopeh 	
	return [ n_oh, slopeh, moh ]


def DrawConvPlotSum(nrocs,output):

	print "Entering DrawConvPlotSum****************************************************************************"	
	
	cfmo = (17479/3.6)/50
	results = drawConvPlotByRoc( nrocs, output )
	print "Printing summury Conversion Plots--------------------------------------------------------------------"
	#print results
	n_oh = results[0]
	slopeh = results[1]
	moh = results[2]
	print "Have histograms : "
	print n_oh
	print slopeh

	c2 = TCanvas('c2',"Distribution N_o",1)
	c2.cd()
	gStyle.SetOptStat(1)
	n_oh.Draw()
	n_oh.SetStats(1)
	c2.Update()
	ps2 = n_oh.GetListOfFunctions().FindObject("stats")
	n_oh.Draw()
	c2.Update()
	c2.SaveAs(output+'Distribution_NoEle.png')
	c2.Close()

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
	c3.Close()

	c5 = TCanvas('c5',"Distribution Mo Peak",1)
	c5.cd()
	gStyle.SetOptStat(1)
	moh.Draw()
	moh.SetStats(1)
	c5.Update()
	moh.GetXaxis().SetTitle("Mo: Vcal")
	moh.GetYaxis().SetTitle("Entries")
	moh.Draw()
	c5.Update()
	textmu5 = TLatex()
	textmu5.SetNDC()
	textmu5.SetTextColor( mycolor(filmlist[2]))
	textmu5.SetTextSize(0.03)
	textmu5.DrawText(0.5,0.6, "Mo Expected Mean: "+ str(float("{0:.2f}".format(cfmo))))
	c5.Update()
	c5.SaveAs(output+'MO_Peak.png')
	c5.Close()

	return  


def FitDrawIndyRocSpectrums( filmlist, histname, nrocs, output, prestring, poststring ):

	print "Entering Fit Spectrums By ROC*******************************************************"
	
	for roc in range(startroc,int(nrocs)):

		print 'Getting fits for Roc: ' + str(roc)
		objects = []
		ele = filmlist[0]
		rootfilename =  rootfilename0 ##prestring + ele + poststring
		rootfile = TFile( rootfilename )
		hist = histname+"_"+ele+"_C"
		print "opening: " + rootfilename + "/" + hist
		fitPeaks(rootfile,hist,ele,roc,output)

		ele = filmlist[1]
		rootfilename =  rootfilename0 ##prestring + ele + poststring
		rootfile = TFile( rootfilename )
		hist = histname+"_"+ele+"_C"
		print "opening: " + rootfilename + "/" + hist
		fitPeaks(rootfile,hist,ele,roc,output)

		ele = filmlist[2]
		rootfilename =  rootfilename0 ##prestring + ele + poststring
		rootfile = TFile( rootfilename )
		hist = histname+"_"+ele+"_C"
		print "opening: " + rootfilename + "/" + hist
		fitPeaks(rootfile,hist,ele,roc,output)

		ele = filmlist[3]
		rootfilename =  rootfilename0 ##prestring + ele + poststring
		rootfile = TFile( rootfilename )
		hist = histname+"_"+ele+"_C"
		print "opening: " + rootfilename + "/" + hist
		fitPeaks(rootfile,hist,ele,roc,output)
	return


def FitDrawSumRocSpectrums(  filmlist, histname, nrocs, output, prestring, poststring ):

	print "Drawing Histograms********************************************************"

	for roc in range(startroc,int(nrocs)):

		print "Opening Histograms for Roc: " + str(roc) + "---------------------------------------------------------------"

		rootfilename1 = rootfilename0 ##prestring + filmlist[0] + poststring
		rootfile1 = TFile( rootfilename1 )
		hist1 = histname+"_"+filmlist[0]+"_C"
		print "opening: " + rootfilename1 + "/" + hist1
		fithisto1 = getHisto(rootfile1,hist1,filmlist[0], roc)

		rootfilename2 = rootfilename0 ##prestring + filmlist[1] + poststring
		rootfile2 = TFile( rootfilename2 )
		hist2 = histname+"_"+filmlist[1]+"_C"
		print "opening: " + rootfilename2 + "/" + hist2
		fithisto2 = getHisto(rootfile2,hist2,filmlist[1], roc)

		rootfilename3 = rootfilename0 ##prestring + filmlist[2] + poststring
		rootfile3 = TFile( rootfilename3 )
		hist3 = histname+"_"+filmlist[2]+"_C"
		print "opening: " + rootfilename3 + "/" + hist3
		fithisto3 = getHisto(rootfile3,hist3,filmlist[2], roc)

		rootfilename4 = rootfilename0 ##prestring + filmlist[3] + poststring
		rootfile4 = TFile( rootfilename4 )
		hist4 = histname+"_"+filmlist[3]+"_C"
		print "opening: " + rootfilename4 + "/" + hist4
		fithisto4 = getHisto(rootfile4,hist4,filmlist[3], roc)

		print 'Plotting Summury for Roc: ' + str(roc) + "------------------------------------------------------------------------"

		c4 = TCanvas('c4',"Fluorescence test",1)
		gStyle.SetOptStat(0)
		fithisto1.GetXaxis().SetRange(0,150)
		fithisto2.GetXaxis().SetRange(0,150)
		fithisto3.GetXaxis().SetRange(0,150)
		fithisto4.GetXaxis().SetRange(0,150)		
		fithisto1.SetLineColor( mycolor(filmlist[0]))
		fithisto2.SetLineColor( mycolor(filmlist[1]))
		fithisto3.SetLineColor( mycolor(filmlist[2]))
		fithisto4.SetLineColor( mycolor(filmlist[3]))
		c4.cd()
		gStyle.SetOptTitle(0)

		muf = fithisto1.GetFunction("gaus2").GetParameter(1)
		sigmaf = fithisto1.GetFunction("gaus2").GetParameter(2)
		mu1 = float("{0:.2f}".format(muf))
		sigma1 = float("{0:.2f}".format(sigmaf))
		muf = fithisto2.GetFunction("gaus2").GetParameter(1)
		sigmaf = fithisto2.GetFunction("gaus2").GetParameter(2)
		mu2 = float("{0:.2f}".format(muf))
		sigma2 = float("{0:.2f}".format(sigmaf))
		muf = fithisto3.GetFunction("gaus2").GetParameter(1)
		sigmaf = fithisto3.GetFunction("gaus2").GetParameter(2)
		mu3 = float("{0:.2f}".format(muf))
		sigma3 = float("{0:.2f}".format(sigmaf))
		muf = fithisto4.GetFunction("gaus2").GetParameter(1)
		sigmaf = fithisto4.GetFunction("gaus2").GetParameter(2)
		mu4 = float("{0:.2f}".format(muf))
		sigma4 = float("{0:.2f}".format(sigmaf))

		fithisto1.Draw()
		textmu1 = TLatex()
		textmu1.SetNDC()
		textmu1.SetTextColor( mycolor(filmlist[0]))
		textmu1.SetTextSize(0.03)
		textmu1.DrawText(0.7,mypos(filmlist[0]), filmlist[0] + ".Mean():"+ str(mu1))
		textsigma1 = TLatex()
		textsigma1.SetNDC()
		textsigma1.SetTextColor( mycolor(filmlist[0]))
		textsigma1.SetTextSize(0.03)
		textsigma1.DrawText(0.7,mypos(filmlist[0])-0.05, filmlist[0] + ".Sigma():"+ str(sigma1))
		c4.Update()

		fithisto2.Draw( "sames" )
		textmu2 = TLatex()
		textmu2.SetNDC()
		textmu2.SetTextColor( mycolor(filmlist[1]))
		textmu2.SetTextSize(0.03)
		textmu2.DrawText(0.7,mypos(filmlist[1]), filmlist[1] + ".Mean():"+ str(mu2))
		textsigma2 = TLatex()
		textsigma2.SetNDC()
		textsigma2.SetTextColor( mycolor(filmlist[1]))
		textsigma2.SetTextSize(0.03)
		textsigma2.DrawText(0.7,mypos(filmlist[1])-0.05, filmlist[1] + ".Sigma():"+ str(sigma2))
		c4.Update()

		fithisto3.Draw( "sames" )
		textmu3 = TLatex()
		textmu3.SetNDC()
		textmu3.SetTextColor( mycolor(filmlist[2]))
		textmu3.SetTextSize(0.03)
		textmu3.DrawText(0.7,mypos(filmlist[2]), filmlist[2] + ".Mean():"+ str(mu3))
		textsigma3 = TLatex()
		textsigma3.SetNDC()
		textsigma3.SetTextColor( mycolor(filmlist[2]))
		textsigma3.SetTextSize(0.03)
		textsigma3.DrawText(0.7,mypos(filmlist[2])-0.05, filmlist[2] + ".Sigma():"+ str(sigma3))
		c4.Update()
	
		fithisto4.Draw( "sames" )
		textmu4 = TLatex()
		textmu4.SetNDC()
		textmu4.SetTextColor( mycolor(filmlist[3]))
		textmu4.SetTextSize(0.03)
		textmu4.DrawText(0.7,mypos(filmlist[3]), filmlist[3] + ".Mean():"+ str(mu4))
		textsigma4 = TLatex()
		textsigma4.SetNDC()
		textsigma4.SetTextColor( mycolor(filmlist[3]))
		textsigma4.SetTextSize(0.03)
		textsigma4.DrawText(0.7,mypos(filmlist[3])-0.05, filmlist[3] + ".Sigma():"+ str(sigma4))
		c4.Update()

		text = TLatex()
		text.SetNDC()
		text.DrawText(0.3,0.95,"Fluorescence tests C"+str(roc))
		print 'Saving to:', output+"_C"+str(roc)+'.png ------------------------------------------------------------------------------'
		c4.SaveAs(output+"_C"+str(roc)+'.png')
		c4.Close()
	return



##MAIN###
#filmlist = [ 'Cu', 'Ag', 'Sn', 'In' ]
#histname = 'Xray/q' 
#nrocs = 16
#output = "XrayFloroResults"
#prestring = 'floro'
#poststring = '40.root'
print "Analyzing Florescent Spectrum Results<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
FitDrawIndyRocSpectrums( filmlist, histname, nrocs, output, prestring, poststring )
FitDrawSumRocSpectrums( filmlist, histname, nrocs, output, prestring, poststring )
DrawConvPlotSum(nrocs, output) 
print "Th th thats all folks<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"












