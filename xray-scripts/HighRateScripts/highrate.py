#/usr/bin/python

import string
import matplotlib.pyplot as plt
import numpy
import math
from numpy import *
from matplotlib.pyplot import *

#line0 = 'this is a test string that list a lot of nonsense so that i can test this parsers'
#line1 = "[16:55:24.178]     INFO: Vcal hit fiducial efficiency (%):  99.9 97.7 96.9 96.6 94.5 95.1 96.6 96.8 93.6 95.4 91.9 93.4 92.6 96.5 99.0 100.0\n"
#line2 = '[16:55:24.178]     INFO: Vcal hit overall efficiency (%):  99.8 97.7 96.7 96.3 94.1 94.6 96.2 96.6 93.4 95.0 88.1 92.8 92.0 96.2 99.0 100.0'
#line3 = '[16:55:24.178]     INFO: X-ray hit rate [MHz/cm2]:  3.7 60.2 103.9 165.8 172.1 185.3 173.2 152.6 146.3 179.7 167.6 172.4 176.3 113.0 37.5 2.0'
#line4 = 'short stiring'


def eff_to_ineff_conversion( list ):
	temp = []
	for ele in list:
		temp.append( 100.0 - ele )
	return temp


psc = 100 # precentiale scale

findfiduc = 'INFO: Vcal hit fiducial efficiency (%):'
findoverall = 'INFO: Vcal hit overall efficiency (%):'
findhitrate = 'INFO: X-ray hit rate [MHz/cm2]:'

lfiduc = []
loverall = []
lhitrate = []
lcnt = []
xs = []
ys = []

head = 'hr'
#head = 'HRate40direct-' 
tail = 'ma35.log'
#tail = 'ma-stacked_0505.log'
mid = [ '02', '04', '06', '08', '10' ]
#mid = [ '.2', '.4', '.6', '.8', '1' ]

color = [ 'r', 'b', 'g', 'y', 'm' ]

for ele in mid:
	lfiduc.append([])
	loverall.append([])
	lhitrate.append([])
cnt = 0
for ele in mid:
	rootLogFile = head + ele + tail

	for inline in open( rootLogFile, 'r').readlines():

		splitline  = string.rsplit( inline.strip(), ' ', 16 )
		if string.find( splitline[0], findfiduc ) > -1 :
			del splitline[0]
			for x in splitline:
				lfiduc[cnt].append( float( x )/psc )
		if string.find( splitline[0], findoverall ) > -1 :
			del splitline[0]
			for x in splitline:
				loverall[cnt].append( float( x )/psc )
		if string.find( splitline[0], findhitrate ) > -1 :
			del splitline[0]
			for x in splitline:
				lhitrate[cnt].append( float( x ) )
	lcnt.append(cnt)
	cnt = cnt + 1

rateErr = 0.293
effErr = 0.480/psc


plt.figure(1)
for ele in lcnt:
	pc1 = color[ele] +'.'
##	pc2 = color[ele] + '<'
	olabel = "Overall: " + str(float(mid[ele])/10.0) + "mA"
##	plt.plot( lhitrate[ele], eff_to_ineff_conversion(lfiduc[ele]), pc1, label = "Fiducial" )
#	plt.plot( lhitrate[ele], eff_to_ineff_conversion(loverall[ele]),pc1, label = olabel )
#	plt.errorbar( lhitrate[ele], eff_to_ineff_conversion(loverall[ele]), rateErr , effErr, None, color[ele] )
	plt.plot( lhitrate[ele], loverall[ele],pc1, label = olabel )
	plt.errorbar( lhitrate[ele], loverall[ele], [effErr*math.sqrt(i) for i in loverall[ele]], [rateErr*math.sqrt(i) for i in lhitrate[ele]], None, color[ele] )
	xs = xs + lhitrate[ele]
	ys = ys + loverall[ele]
plt.legend(loc='lower left') # upper left')
plt.ylabel("% InEfficency " )
plt.xlabel("MHz/cm^2") 
#plt.title("InEfficency vs Hit Rate")

coefficients = polyfit(xs, ys, 3)
eqt = poly1d(coefficients)
x2 = arange(0,250, 1)
y2 = eqt(x2)
plot(x2, y2)
text( 100, 1, eqt, fontsize = 12 )
print eqt(140)
plt.title("Efficency vs Hit Rate")
plt.savefig( "Highrate2.png", format = "png")
plt.show()







# error calcs----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#    int numTrigs = N = fParNtrig * 4160;
# double sensorArea = A = 0.015 * 0.010 * 54 * 81
#    numTrigsString += Form(" %4d", numTrigs );
#    fidCalEfficiencyString += Form(" %.1f", fidHits[i]/static_cast<double>(fidPixels[i]*fParNtrig)*100);
#    allCalEfficiencyString += Form(" %.1f", allHits[i]/static_cast<double>(numTrigs)*100);
#    xRayRateString += Form(" %.1f", xHits[i]/static_cast<double>(numTrigs)/25./sensorArea*1000.);

#sigma rate = C/N w/ C = 40./A = 40/(0.015*0.010*54*81) = 60.96631611 => 0.0029310728899038
#sigma eff  = C/N w/ C = 100 =>  0.0048076923076923
#
#Ntrig               5
#Vcal                200
#runDaq              button
#trgfrequency(khz)   20
#runseconds          2
#triggerdelay        20

#N = 20800 = (1/2) = 0.006933752



