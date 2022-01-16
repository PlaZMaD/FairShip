#ifndef PNDUnmuGENERATOR_H
#define PNDUnmuGENERATOR_H 1

#include "TROOT.h"
#include "FairGenerator.h"
#include "TTree.h"                      // for TTree
#include "TClonesArray.h"               
#include "FairLogger.h"                 // for FairLogger, MESSAGE_ORIGIN
#include <string>
#include <vector>
#include <array>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <sstream>
#include <boost/foreach.hpp>

class FairPrimaryGenerator;

class UnrolledMuonBackGenerator : public FairGenerator
{
 public:
  
  /** default constructor **/
  UnrolledMuonBackGenerator();
  
  /** destructor **/
  virtual ~UnrolledMuonBackGenerator();
  
  /** public method ReadEvent **/
  Bool_t ReadEvent(FairPrimaryGenerator*);  
  virtual Bool_t Init(const char*, int, std::string json_input, const Bool_t fl); //!
  virtual Bool_t Init(const char*, std::string json_input); //!
  Int_t GetNevents();//!
  void CloseFile();//!
  void SetPhiRandom(Bool_t fl) { fPhiRandomize = fl; };
  void FollowAllParticles() { followMuons = false; };
  void SetSmearBeam(Double_t sb) { fsmearBeam = sb; };
  void SetSameSeed(Int_t s) {
    LOGF(info, "Seed: %d", s);
    fSameSeed = s;
  };
  Bool_t checkDiMuon(Int_t muIndex);
  void SetDownScaleDiMuon(){ fdownScaleDiMuon = kTRUE; };

private:
protected:
  Float_t id,parentid,pythiaid,w,px,py,pz,vx,vy,vz,ecut;
  TClonesArray* MCTrack; //!
  TClonesArray* vetoPoints; //!
  TFile* fInputFile;    //! 
  TTree* fTree;         //! 
  int fNevents;
  float f_zOffset;      //!
  int fn;
  Bool_t fPhiRandomize;
  Bool_t fdownScaleDiMuon;
  Bool_t followMuons;
  Int_t fSameSeed;
  Double_t fsmearBeam ;
  boost::property_tree::ptree input_config;
  std::vector<int>eventList;
  std::vector<double>weightsList;

  ClassDef(UnrolledMuonBackGenerator,6);
};

#endif /* !PNDmuGENERATOR_H */
