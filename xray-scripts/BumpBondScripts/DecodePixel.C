
#include <math.h>
#include <time.h>
#include <fstream>
#include <iostream>
#include <iomanip>


void DecodeRaw(uint32_t raw, bool invert) {
    value = (raw & 0x0f) + ((raw >> 1) & 0xf0);
    if( (raw & 0x10) >0) {
      LOG(logDEBUGAPI) << "invalid pulse-height fill bit from raw value of "<< std::hex << raw << std::dec << ": " << *this;
      throw DataDecoderError("Error decoding pixel raw value");
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

    row = 80 - r/2;
    column = 2*c + (r&1);

    if (row >= ROC_NUMROWS || column >= ROC_NUMCOLS){
      LOG(logDEBUGAPI) << "invalid pixel from raw value of "<< std::hex << raw << std::dec << ": " << *this;
      throw DataDecoderError("Error decoding pixel raw value");
    }
  }

} // namespace pxar



void DecodePixel(unsigned int raw, int & x, int & y, int & ph)
{
        ph = (raw & 0x0f) + ((raw >> 1) & 0xf0);
        raw >>= 9;
        int c =    (raw >> 12) & 7;
        c = c*6 + ((raw >>  9) & 7);
        int r =    (raw >>  6) & 7;
        r = r*6 + ((raw >>  3) & 7);
        r = r*6 + ( raw        & 7);
        y = 80 - r/2;
        x = 2*c + (r&1);
        printf("   Pixel [%05o] %2i/%2i: %3u", raw, x, y, ph);
	return;
}

void DecodePixel(unsigned int raw)
{

        int x,y,ph;
        DecodePixel(raw,x,y,ph);
        printf("   Pixel [%05o] %2i/%2i: %3u", raw, x, y, ph);
	return;
}
