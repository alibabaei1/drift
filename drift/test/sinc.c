#include “TMath.h”
#include “TF1.h”

int SincMacro()
{

TF1 *f1 = new TF1("f1","sin(x)/x",0.,10.);
f1->Draw();
    return 0;
}

