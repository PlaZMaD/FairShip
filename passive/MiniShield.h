#ifndef MiniShield_H
#define MiniShield_H

#include "FairModule.h"                 // for FairModule
// #include "FairLogger.h"

#include "Rtypes.h"                     // for MiniShield::Class, Bool_t, etc

#include "TGeoUniformMagField.h"
#include "TGeoMedium.h"
#include "TGeoShapeAssembly.h"
#include "TString.h"
#include <vector>
#include <array>

class MiniShield : public FairModule
{
  public:

   MiniShield(const char* name, const Int_t Design=1,  const char* Title="MiniShield",
                               Double_t Z=0, Double_t L0=0, Double_t L1=0, Double_t L2=0, Double_t L3=0, Double_t L4=0, Double_t L5=0, Double_t L6=0, 
                               Double_t L7=0, Double_t L8=0,Double_t gap=0,Double_t LE=0,Double_t y=400, Double_t floor=500, Double_t field=1.7, 
                               const Int_t withCoMagnet=0, const Bool_t StepGeo=false);

   MiniShield(TString geofile);
   MiniShield();
   virtual ~MiniShield();
   void ConstructGeometry();
   ClassDef(MiniShield,4)

  // void SetSupports(Bool_t supports) { 
  //   fSupport = supports;
  //   FairLogger::GetLogger()->Warning(MESSAGE_ORIGIN, "Setting supports to %s. This will not have any effect if called after the geometry has been constructed.", fSupport ? "true" : "false");
  // }
    
 protected:
  
  Int_t  fDesign;       // design of muon shield, 1=passive, active = ...
  TString fGeofile;
  Double_t  fMiniShieldLength,fY,fField;
  Double_t fFloor;
  Bool_t fSupport;
  Double_t  dZ0,dZ1,dZ2,dZ3,dZ4,dZ5,dZ6,dZ7,dZ8,dXgap,zEndOfAbsorb,mag4Gap,midGapOut7,midGapOut8;
  Int_t InitMedium(TString name);

  void CreateArb8(TString arbName, TGeoMedium *medium, Double_t dZ,
		  std::array<Double_t, 16> corners, Int_t color,
		  TGeoUniformMagField *magField, TGeoVolume *top,
		  Double_t x_translation, Double_t y_translation,
		  Double_t z_translation);

    void CreateArb8(TString arbName, TGeoMedium *medium, Double_t dZ,
      std::array<Double_t, 16> corners, Int_t color,
      TGeoUniformMagField *magField, TGeoVolume *top,
      Double_t x_translation, Double_t y_translation,
      Double_t z_translation, 
      Bool_t stepGeo);

  void CreateTube(TString tubeName, TGeoMedium *medium, Double_t dX,
		  Double_t dY, Double_t dZ, Int_t color, TGeoVolume *top,
		  Double_t x_translation, Double_t y_translation,
		  Double_t z_translation);

  Int_t Initialize(std::vector<TString> &magnetName,
		  std::vector<Double_t> &dXIn, std::vector<Double_t> &dYIn,
		  std::vector<Double_t> &dXOut, std::vector<Double_t> &dYOut,
		  std::vector<Double_t> &dZ, std::vector<Double_t> &midGapIn,
		  std::vector<Double_t> &midGapOut,
		  std::vector<Double_t> &HmainSideMagIn,
		  std::vector<Double_t> &HmainSideMagOut,
		  std::vector<Double_t> &gapIn, std::vector<Double_t> &gapOut,
		  std::vector<Double_t> &Z);

  void CreateMagnet(TString magnetName, TGeoMedium *medium, TGeoVolume *tShield,
		    TGeoUniformMagField *field,
		    Double_t dX, Double_t dY,
		    Double_t dZ, Double_t Z);


};

#endif //MuonSield_H
