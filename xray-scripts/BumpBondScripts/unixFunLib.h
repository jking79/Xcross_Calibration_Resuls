//=================================================================================================  
//  Jack W King III   private code file
//  unix system intergration helper functions
//  all rights resevered 
//---------unix functions libary h--------------------------------------------------------------------
//===================  libaries ===================================================================
#ifndef CSTD
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <cstring>
#include <string>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <ctime>
#define CSTD
#endif

#ifndef UNIX
#define UNIX
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#endif

#ifndef UNIXHELPERS
#define UNIXHELPERS
using namespace std;



//===========================================================================================================
//======================= #define section for compile controlls=============================================

//#define TESTUNIXLIB	//  turns on class testing functions
//#define SCREEN  //  sends status info to the screen

//================================================================================================================
//==============================const string defs=================================================================
//====================================================================================================================

#define MAX_BUF 4096

//================================================================================================
// these are helper functions for manipulating strings and doing class conversions 
// from and to strings with intergers and to convert from intergers to and from binary strings
//====================================================================================================
//
//=================  helper function binary as string converter ====================================
//


//==================================================================================================================================
//======================================= check to see if path exist as a file or a pipe respect ========================================================================================


int 	isFile( string path );
int 	isPipe( string path );

//==================================================== using fifos ===========================================================================
//===============================================================================================================================

void 	sendToPipe( string pipe, string input );//uses unix commands
int 	openOutPipe( string pipe  );
void 	sendToPipe( int fd, string input );
void 	sendToPipe( ofstream& pipe, string input );
void 	flushToPipe( string pipe );
void 	sendToFPipe( string pipe, string input );//uses file streams

//===================================================== using fifos =============================================================================
//===============================================================================================================================

string 	getFromPipe( string pipe );//uses unix commands
int 	openInPipe( string pipe );
string 	getFromPipe( int fd );
string 	getFromPipe( ifstream& pipe );
int 	scanFromPipe( string pipe, string& result );//nonblocking
void 	flushFromPipe( string pipe );
string 	getFromFPipe( string pipe );//uses file streams

//======================================================= create fifos ( named pipes )===============================================================================
//=====================================================================================================================================
int 	makePipe( string path );
int 	makeFPipe( string path );//uses file streams
//================================================= open ifstream and ofstream with strings=================================================================================
//===============================================================================================================================

int 	openInStream( string fileName, ifstream& in );
int 	openOutStream( string fileName, ofstream& out );

//=============================================misc system commands=====================================================================================
//===============================================================================================================================


int 	sysCmd( string cmd );
void 	rmFile( string pipe );// remove file of type pipe
string 	getGMTimeDate();
string 	getAppWorkingDir();
string 	getAppHostName();

//=============================================================================================================================
//========================================  possion random distribution functions ===========================================

int 	pRand( int mean );
int 	pRand( int m, int t );
int 	gRand( int mean, int thres );


#endif

