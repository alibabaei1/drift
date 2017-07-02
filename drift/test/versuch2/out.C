//#include "Riostream.h"
Double_t chi2Function(Double_t *x, Double_t *par)
{
	Double_t retval = 0;
	if ( TMath::Power(2, 0.5*par[1]) * TMath::Gamma(0.5*par[1]) ) {
		retval = (par[0]*(TMath::Power(x[0], 0.5*par[1] - 1)
		* TMath::Exp(-0.5*x[0]) /
		(TMath::Power(2, 0.5*par[1]) * TMath::Gamma(0.5*par[1]))));
	}
	return retval;
}
void macro3 () {
	chi2func = new TF1("chi2func", chi2Function, 0., 30, 2 );
	chi2func->SetParNames("norm", "ndf");
	chi2func->SetParameter(0, 100. );
	chi2func->SetParameter(1, 10.);
	chi2func->Draw();
}

void macro5 () {
	ifstream in;
	in.open("something.dat");
	TH1D* fitHist = new TH1D("fitHist","",120,-6.,6.);
	int nlines=0;
	while (!in.eof()) {
		nlines++;
		double massDiff = 0;
		int nEvents = 0;
		in >> massDiff >> nEvents;
		// if (in.eof()) break;
		cout << nlines << " " << fitHist->FindBin(massDiff)
		<< " " << massDiff << " " << nEvents << " " << sqrt(nEvents) << endl;
		fitHist->SetBinContent(fitHist->FindBin(massDiff),nEvents);
		fitHist->SetBinError(fitHist->FindBin(massDiff),sqrt(nEvents));
	}
	fitHist->DrawCopy();
	in.close();
}
void macro()
{
	ifstream in;
	in.open("myout.dat");

	double x,y;
	Int_t nlines = 0;
	TFile* file = new TFile("run_170614_103926.root","RECREATE");
	TNtuple *ntuple = new TNtuple("ntuple","data from ascii file","x:y:erry");

	while (1) {
		in >> x >> y;
		if (!in.good()) break;
		cout << x << " " << endl;
		ntuple->Fill(x,y,sqrt(y));
		nlines++; 
	}
	printf(" found %d pointsn",nlines);
	in.close();
	file->Write();

	return;
}
