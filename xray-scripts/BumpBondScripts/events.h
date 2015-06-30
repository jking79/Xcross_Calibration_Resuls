//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jun 26 15:45:45 2014 by ROOT version 5.34/18
// from TTree events/events
// found on file: ../../Module_Comparison_Tests/ForJack_M_CL_901_ROC5_XRay.root
//////////////////////////////////////////////////////////

#ifndef events_h
#define events_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "TCanvas.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TLegend.h"
#include "TArrow.h"
#include "TLatex.h"
#include "TDirectory.h"


// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class events {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   UShort_t        header;
   UShort_t        trailer;
   UShort_t        npix;
   UChar_t         proc[3074];   //[npix]
   UChar_t         pcol[3074];   //[npix]
   UChar_t         prow[3074];   //[npix]
   UChar_t         pval[3074];   //[npix]

   // List of branches
   TBranch        *b_header;   //!
   TBranch        *b_trailer;   //!
   TBranch        *b_npix;   //!
   TBranch        *b_proc;   //!
   TBranch        *b_pcol;   //!
   TBranch        *b_prow;   //!
   TBranch        *b_pval;   //!

   events(TTree *tree=0);
   events( string name );
   virtual ~events();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
  
};

#endif

#ifdef events_cxx
events::events(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("ForJack_M_CL_901_ROC5_XRay.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("ForJack_M_CL_901_ROC5_XRay.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("ForJack_M_CL_901_ROC5_XRay.root:/DAQ");
      dir->GetObject("events",tree);

   }
   Init(tree);
}

events::~events()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t events::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t events::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void events::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("header", &header, &b_header);
   fChain->SetBranchAddress("trailer", &trailer, &b_trailer);
   fChain->SetBranchAddress("npix", &npix, &b_npix);
   fChain->SetBranchAddress("proc", proc, &b_proc);
   fChain->SetBranchAddress("pcol", pcol, &b_pcol);
   fChain->SetBranchAddress("prow", prow, &b_prow);
   fChain->SetBranchAddress("pval", pval, &b_pval);
   Notify();
}

Bool_t events::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void events::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t events::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef events_cxx
