
#include <math.h>
#include <time.h>
#include <fstream>
#include <iostream>
#include <iomanip>



void DecodeRaw( unsigned int raw, bool invert)
{
    unsigned int input = raw;
    int value = (raw & 0x0f) + ((raw >> 1) & 0xf0);
    if( (raw & 0x10) >0) {
      //LOG(logDEBUGAPI) << "invalid pulse-height fill bit from raw value of "<< std::hex << raw << std::dec << ": " << *this;
      //throw DataDecoderError("Error decoding pixel raw value");
    cout << "invalid pulse-height fill bit from raw value of "<< std::hex << raw << std::dec << ": " << *this;
    return;	
    }
    int c =    (raw >> 21) & 7;
    c = c*6 + ((raw >> 18) & 7);

    int r2 =    (raw >> 15) & 7;
    if(invert) { r2 ^= 0x7; }
    int r1 = (raw >> 12) & 7;
    if(invert) { r1 ^= 0x7; }
    int r0 = (raw >>  9) & 7;
    if(invert) { r0 ^= 0x7; }
    int r = r2*36 + r1*6 + r0;

    int row = 80 - r/2;
    int column = 2*c + (r&1);
	
    cout << std::dec << "Row: " << row << " Column: " << column << " ph: " << value << " c: " << c << " r: " << r ;
    cout << " input : " << std::hex << input << endl;
    return;    
    //if (row >= ROC_NUMROWS || column >= ROC_NUMCOLS){
    //  LOG(logDEBUGAPI) << "invalid pixel from raw value of "<< std::hex << raw << std::dec << ": " << *this;
    //  throw DataDecoderError("Error decoding pixel raw value");
    //}
}// DecodeRaw



void DecodePixel(unsigned int raw, int & x, int & y, int & ph)
{
        ph = (raw & 0x0f) + ((raw >> 1) & 0xf0);
	int input  = raw;
        raw >>= 9;
        int c =    (raw >> 12) & 7;
        c = c*6 + ((raw >>  9) & 7);
        int r =    (raw >>  6) & 7;
        r = r*6 + ((raw >>  3) & 7);
        r = r*6 + ( raw        & 7);
        y = 80 - r/2;
        x = 2*c + (r&1);
	cout << dec << "y: " << y << " x: " << x << " ph: " << ph << " c: " << c << " r: " << r << " input : " << hex << input << endl;
	//printf("   Pixel [%05o] %2i/%2i: %3u\n", raw, x, y, ph);
	return;
}

void DecodePixel( unsigned int raw )
{

        int x,y,ph;
        DecodePixel(raw,x,y,ph);
        //printf("   Pixel [%05o] %2i/%2i: %3u\n", raw, x, y, ph);
	return;
}
