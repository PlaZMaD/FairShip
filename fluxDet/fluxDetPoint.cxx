#include "fluxDetPoint.h"

#include <iostream>
using std::cout;
using std::endl;


fluxDetPoint::fluxDetPoint()
  : FairMCPoint()
{
}

fluxDetPoint::fluxDetPoint(Int_t trackID, Int_t detID,
			   TVector3 pos, TVector3 mom,
			   Double_t tof, Double_t length,
			   Double_t eLoss, Int_t pdgcode)//,TVector3 Lpos, TVector3 Lmom)
  : FairMCPoint(trackID, detID, pos, mom, tof, length, eLoss), fPdgCode(pdgcode)//,fLpos(Lpos),fLmom(Lmom)
{
}
// -------------------------------------------------------------------------

// -----   Destructor   ----------------------------------------------------
fluxDetPoint::~fluxDetPoint() { }
// -------------------------------------------------------------------------

// -----   Public method Print   -------------------------------------------
void fluxDetPoint::Print() const
{
  cout << "-I- fluxDetPoint: veto point for track " << fTrackID
       << " in detector " << fDetectorID << endl;
  cout << "    Position (" << fX << ", " << fY << ", " << fZ
       << ") cm" << endl;
  cout << "    Momentum (" << fPx << ", " << fPy << ", " << fPz
       << ") GeV" << endl;
}
// -------------------------------------------------------------------------

ClassImp(fluxDetPoint)
