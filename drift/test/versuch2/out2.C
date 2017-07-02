//TH1F* hnseg(nullptr);
void readEvent2(){
   hnseg = new TH1F("hnseg","Number of segments for selected tracks",4096,0,8192);

   TFile fileIn("run_170614_103926.root");

   TTree* theTree = nullptr;
   fileIn.GetObject("T",theTree);

   TClonesArray *tracks = nullptr;
   Event *event = new Event(); //object must be created before
                               //setting the branch address

   auto bntrack = theTree->GetBranch("fNtrack");
   auto branch  = theTree->GetBranch("event");
   branch->SetAddress(&event);
   auto nevent = theTree->GetEntries();
   for (Int_t i=0;i<nevent;i++) {
      bntrack->GetEvent(i);
      if (event->GetNtrack() < 587)continue;
      theTree->GetEvent(i);           //Read complete accepted event
                                      //in memory.
      hnseg->Fill(event->GetNseg());  //Fill histogram with number of
                                      //segments.
      tracks = event->GetTracks();    //Get pointer to the
                                      //TClonesArray object.
      tracks->Clear();                //Clear it.
   }

   hnseg->Draw();
}

