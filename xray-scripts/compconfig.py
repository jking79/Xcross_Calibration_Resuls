import os
import re

dirone = "KUConfig/"
dirtwo = "UNLConfig/"

setfilenames = [ 'configParameters', 'defaultMaskFile', 'tbmParameters_C0a', 'tbmParameters_C0b', 'tbParameters', 'testParameters', 'testPatterns' ]
cfilenames = [ 'dacParameters35_C', 'phCalibration_C', 'phCalibrationFitErr35_C', 'readbackCal_C', 'SCurveData_C', 'trimParameters_C' ]

suffix = ".dat"
precom = "diff "
postcom = " >> diff"

for file in setfilenames :
	os.system( precom + dirone + file + suffix + " " + dirtwo + file + suffix + postcom + file + suffix )

for file in cfilenames :
	for roc in range(0,15) :
		os.system( precom + dirone + file + str(roc) + suffix + " " + dirtwo + file + str(roc) + suffix + postcom + file + str(roc) + suffix )
		

