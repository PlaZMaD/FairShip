#ifndef MuonShield_H
#define MuonShield_H

#include "FairModule.h"                 // for FairModule
#include "FairLogger.h"

#include "Rtypes.h"                     // for ShipMuonShield::Class, Bool_t, etc

#include "TGeoUniformMagField.h"
#include "TGeoMedium.h"
#include "TGeoShapeAssembly.h"
#include "TString.h"
#include <vector>
#include <array>
#include <math.h>

enum class FieldDirection : bool { up, down };

class ShipMuonShield : public FairModule
{
  public:

   ShipMuonShield(const char* name, const Int_t Design=1,  const char* Title="ShipMuonShield",
                               Double_t Z=0, Double_t L0=0, Double_t L1=0, Double_t L2=0, Double_t L3=0, Double_t L4=0, Double_t L5=0, Double_t L6=0, 
                               Double_t L7=0, Double_t L8=0,Double_t gap=0,Double_t LE=0,Double_t y=400, Double_t floor=500, Double_t field=1.7, 
                               const Int_t withCoMagnet=0, const Bool_t StepGeo=false,
                               const Bool_t WithConstAbsorberField=true, const Bool_t WithConstShieldField=true);

   ShipMuonShield(const char* name, const double to_be_done,const Int_t Design=20,  const char* Title="ShipMuonShield",
                               Double_t Start_Z=0, Double_t Z=0, Double_t H1=0, Double_t field=1.7, Double_t mgap=0);

   ShipMuonShield(TString params, const char* name, const Int_t Design=1,  const char* Title="ShipMiniShield",
                               Double_t Z=0, Double_t L0=0, Double_t L1=0, Double_t L2=0, Double_t L3=0, Double_t L4=0, Double_t L5=0, Double_t L6=0, 
                               Double_t L7=0, Double_t L8=0,Double_t gap=0,Double_t LE=0,Double_t y=400, Double_t floor=500, Double_t field=1.7, 
                               const Int_t withCoMagnet=0, const Bool_t StepGeo=false,
                               const Bool_t WithConstAbsorberField=true, const Bool_t WithConstShieldField=true);

   ShipMuonShield(Double_t Z, TString geofile, const Int_t withCoMagnet=0, const Bool_t StepGeo=false,
   const Bool_t WithConstAbsorberField=true, const Bool_t WithConstShieldField=true);
   ShipMuonShield();
   virtual ~ShipMuonShield();
   void ConstructGeometry();
   ClassDef(ShipMuonShield,4)

  void SetSupports(Bool_t supports) { 
    fSupport = supports;
    FairLogger::GetLogger()->Warning(MESSAGE_ORIGIN, "Setting supports to %s. This will not have any effect if called after the geometry has been constructed.", fSupport ? "true" : "false");
  }

  // H_zone is h_l(r) from PG Memo and W_zone is 2 * f_l(r)
  // Inputs and outputs are in [cm]
  Double_t CalculateGapWidth(Double_t _H_zone, Double_t _W_zone) {
    Double_t H_zone = _H_zone / 100;
    Double_t W_zone = _W_zone / 100;
    return (H_steel * H_zone + H_steel * W_zone + 625000. / M_PI * B_avg * _delta) * 1.5 /
           (0.25 * J * H_zone - H_steel) * 100;
  }

 protected:
  
  TString optParams = "";
  Int_t  fDesign;       // design of muon shield, 1=passive, active = ...
  TString fGeofile;
  Double_t  fMuonShieldLength,fY,fField;
  Double_t fFloor;
  Bool_t fSupport;
  Double_t  dZ0,dZ1,dZ2,dZ3,dZ4,dZ5,dZ6,dZ7,dZ8,dXgap,zEndOfAbsorb,mag4Gap,midGapOut7,midGapOut8;
  Int_t InitMedium(TString name);

  Int_t fWithCoMagnet;
  Bool_t fStepGeo;
  Bool_t fWithConstAbsorberField;
  Bool_t fWithConstShieldField;


  const Double_t J = pow(10., 6.); //[A/m^2]
  const Double_t H_steel = 3000.0; //[A/m]
  const Double_t B_avg = 1.8; //[T]
  const Double_t _delta = 8 * 0.5 * pow(10., -3.); //[m]

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
		  std::vector<FieldDirection> &fieldDirection,
		  std::vector<Double_t> &dXIn, std::vector<Double_t> &dYIn,
		  std::vector<Double_t> &dXOut, std::vector<Double_t> &dYOut,
		  std::vector<Double_t> &dZ, std::vector<Double_t> &midGapIn,
		  std::vector<Double_t> &midGapOut,
		  std::vector<Double_t> &HmainSideMagIn,
		  std::vector<Double_t> &HmainSideMagOut,
		  std::vector<Double_t> &gapIn, std::vector<Double_t> &gapOut,
		  std::vector<Double_t> &Z);

  Int_t mini_Initialize(std::vector<TString> &magnetName,
      std::vector<FieldDirection> &fieldDirection,
      std::vector<Double_t> &dXIn, std::vector<Double_t> &dYIn,
      std::vector<Double_t> &dXOut, std::vector<Double_t> &dYOut,
      std::vector<Double_t> &dZ, std::vector<Double_t> &midGapIn,
      std::vector<Double_t> &midGapOut,
      std::vector<Double_t> &HmainSideMagIn,
      std::vector<Double_t> &HmainSideMagOut,
      std::vector<Double_t> &gapIn, std::vector<Double_t> &gapOut,
      std::vector<Double_t> &Z);

  void CreateMagnet(TString magnetName, TGeoMedium *medium, TGeoVolume *tShield,
		    TGeoUniformMagField *fields[4],
		    FieldDirection fieldDirection, Double_t dX, Double_t dY,
		    Double_t dX2, Double_t dY2, Double_t dZ, Double_t middleGap,
		    Double_t middleGap2, Double_t HmainSideMag,
		    Double_t HmainSideMag2, Double_t gap, Double_t gap2,
		    Double_t Z, Bool_t NotMagnet, Bool_t stepGeo);

};

#endif //MuonSield_H
