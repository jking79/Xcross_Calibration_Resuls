#include <iostream>
#include <cstdlib>



using namespace std;

float GetPt100Temerature(float r);

int main(int argc, char *argv[]){
        cout <<endl;
        cout <<"Resistance: "<<(argv[1])<< " Ohms" <<endl;
  cout <<"Degrees: "<<GetPt100Temerature(atof(argv[1]))<<" Celcius"<<endl<<endl;
  return 0;
}

float GetPt100Temerature(float r)
{
  float const Pt100[] = { 80.31,   82.29,  84.27,  86.25,  88.22,  90.19,  92.16,  94.12,  96.09,  98.04,
                          100.0,  101.95, 103.9,  105.85, 107.79, 109.73, 111.67, 113.61, 115.54, 117.47,
                          119.4,  121.32, 123.24, 125.16, 127.07, 128.98, 130.89, 132.8,  134.7,  136.6,
                          138.5,  140.39, 142.29, 157.31, 175.84, 195.84 };
  int t = -50, i = 0, dt = 0;
  if (r > Pt100[0])
    while (250 > t) {
      dt = (t < 110) ? 5 : (t > 110) ? 50 : 40;
      if (r < Pt100[++i])
        return t + (r - Pt100[i-1]) * dt / (Pt100[i] - Pt100[i-1]);
      t += dt;
    };

  return t;
}


int main(){

	for( int t = 0; t <







