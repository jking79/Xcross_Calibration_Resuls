#define events_cxx

#include "events.h"
#include "strFunLib.cpp"


events* setevent( string name )
{
      	TFile* f = new TFile( strToChar( name ) );
	cout << f << endl;
      	TTree* thetree;
      	f->GetObject("DAQ/events",thetree);
	cout << thetree << endl;
	return ( new events( thetree ) );
}


void events::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L events.C
//      Root > events t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//
//
//    This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//    Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//    To read only selected branches, Insert statements like:
//    METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
//    METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//    by  b_branchname->GetEntry(ientry); //read only this branch
      if (fChain == 0) return;

         Long64_t nentries = fChain->GetEntriesFast();

         Long64_t nbytes = 0, nb = 0;
              for (Long64_t jentry=0; jentry<nentries;jentry++) {
                   Long64_t ientry = LoadTree(jentry);
                   if (ientry < 0) break;
                   nb = fChain->GetEntry(jentry);   nbytes += nb;
                 // if (Cut(ientry) < 0) continue;
         }
	return;
}//end of loop

const int MAX = 16;

void events::makeHitsVsEvents(){

        string dirfile("HitsVsEvents.root");
        string histfile("HitsVsEvents_C");
        string histname("Hits per Event for ROC ");
        string histfilesuffix(".hist");

        TFile* dir = new TFile( strToChar( dirfile ), "UPDATE" );
        TH1D* hist[ MAX ];
        int* nhpr[ MAX ];

        Long64_t nentries = fChain->GetEntriesFast();
        Long64_t nbytes = 0, nb = 0;
        int nhpe = 0, index = 0;


        for( int i = 0; i < MAX; i++ ){
        nhpr[i] = 0;
        hist[i] = new TH1D( strToChar( histfile + intToStr( i ) + histfilesuffix ), strToChar( histname + intToStr( i ) ), nentries, 0, nentries );
        };//end of histgram creation loop

        if (fChain == 0) return;

        for (Long64_t jentry=0; jentry<nentries;jentry++) {
                Long64_t ientry = LoadTree(jentry);
                if (ientry < 0) break;
                nb = fChain->GetEntry(jentry);   nbytes += nb;
                while( ( (int) pval[index] )  > 0 ){
                        nhpe++;
                        //cout << (int) pval[index] << " ";
                        index++;
                };// end of loop to count number of hits per event
                //cout << (int) nhpe << " " << endl;
                index = 0;
                while( index <= nhpe ){
                        nhpr[ ( (int) proc[ index ] ) ] =  (int) nhpr[ ( (int) proc[ index ] ) ] + (int) 1;
                        //cout << (int) nhpr[ ( proc[ index ] ) ] << " " << (int) proc[ index ] << " " << index << endl;
                        index++;
                };// end of loop to cont number of hits per roc
                index = 0;
                nhpe = 0;
                while( index < MAX ){
			for( int i = 0; i < ( int ) nhpr[ index ]; i++){
                        	hist[ index ]->Fill( (Double_t)( jentry ) );
				//cout << (Double_t) jentry << endl;
			}
                        nhpr[ index ] = 0;
                        index++;
                };//end of loop to fill histograms
                index = 0;
        };//end of entry read loop
        for( index = 0; index < MAX; index++ ){
                hist[ index ]->Write();
        };//end of loop to write histograms to disk
        dir->Close();
        return;
} //end of makeHitsVsEvents

void events::makeEventVsHits(){

	string dirfile("EventVsHits.root");
	string histfile("EventVsHits_C");
	string histname("Events per Hit for ROC ");
	string histfilesuffix(".hist");

	TFile* dir = new TFile( strToChar( dirfile ), "UPDATE" ); 
	TH1D* hist[ MAX ];  
	int* nhpr[ MAX ];
	
	for( int i = 0; i < MAX; i++ ){
	nhpr[i] = 0;
	hist[i] = new TH1D( strToChar( histfile + intToStr( i ) + histfilesuffix ), strToChar( histname + intToStr( i ) ), 40, 0, 40 );
	};//end of histgram creation loop

  	if (fChain == 0) return;

   	Long64_t nentries = fChain->GetEntriesFast();
   	Long64_t nbytes = 0, nb = 0;
	int nhpe = 0, index = 0;
   	for (Long64_t jentry=0; jentry<nentries;jentry++) {
      		Long64_t ientry = LoadTree(jentry);
      		if (ientry < 0) break;
      		nb = fChain->GetEntry(jentry);   nbytes += nb;
		while( ( (int) pval[index] )  > 0 ){ 
			nhpe++;
			//cout << (int) pval[index] << " ";
			index++;
		};// end of loop to count number of hits per event
		//cout << (int) nhpe << " " << endl;
		index = 0;
		while( index <= nhpe ){
			nhpr[ ( (int) proc[ index ] ) ] =  (int) nhpr[ ( (int) proc[ index ] ) ] + (int) 1;
			//cout << (int) nhpr[ ( proc[ index ] ) ] << " " << (int) proc[ index ] << " " << index << endl;
			index++;
		};// end of loop to cont number of hits per roc
		index = 0;
		nhpe = 0;
		while( index < MAX ){
			hist[ index ]->Fill( ((Double_t)( nhpr[ index ])) );
			nhpr[ index ] = 0;
			index++;
		};//end of loop to fill histograms
		index = 0;
   	};//end of entry read loop
	for( index = 0; index < MAX; index++ ){
		hist[ index ]->Write();
	};//end of loop to write histograms to disk
	dir->Close();
	return;
} //end of makeEventvsHits


#endif//event_cpp
