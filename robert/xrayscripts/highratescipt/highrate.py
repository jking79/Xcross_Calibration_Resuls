#/usr/bin/python

import string
import matplotlib.pyplot as plt
import math


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


findfiduc = 'INFO: Vcal hit fiducial efficiency (%):'
findoverall = 'INFO: Vcal hit overall efficiency (%):'
findhitrate = 'INFO: X-ray hit rate [MHz/cm2]:'

lfiduc = []
loverall = []
lhitrate = []
lcnt = []

head = 'HRate40direct-' ##'hr'
tail = 'ma-stacked_0505.log'
mid = [ '.2', '.4', '.6', '.8', '1' ]
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
				lfiduc[cnt].append( float( x ) )
		if string.find( splitline[0], findoverall ) > -1 :
			del splitline[0]
			for x in splitline:
				loverall[cnt].append( float( x ) )
		if string.find( splitline[0], findhitrate ) > -1 :
			del splitline[0]
			for x in splitline:
				lhitrate[cnt].append( float( x ) )
	lcnt.append(cnt)
	cnt = cnt + 1




plt.figure(1)
for ele in lcnt:
	pc1 = color[ele] +'o'
	pc2 = color[ele] + '<'
	olabel = "Overall: " + mid[ele] + "mA"
##	plt.plot( lhitrate[ele], eff_to_ineff_conversion(lfiduc[ele]), pc1, label = "Fiducial" )
	plt.plot( lhitrate[ele], eff_to_ineff_conversion(loverall[ele]), pc2, label = olabel )
plt.legend(loc='upper left')
plt.ylabel("% InEfficency " )
plt.xlabel("MHz/cm^2") 
plt.title("InEfficency vs Hit Rate")
plt.savefig( "Highrate.png", format = "png")
plt.show()








