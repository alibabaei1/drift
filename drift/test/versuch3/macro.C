void macro1()
{
	TH1F h1("h1","Beispiel",40,0,10);
	TF1 f1("func1","exp(-x)*x",0,10);
	h1.FillRandom("func1",1000);
	h1.DrawCopy();
}
