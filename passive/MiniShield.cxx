#include "MiniShield.h"

#include "TGeoManager.h"
#include "TObjArray.h"                  // for TObjArray
#include "TString.h"                    // for TString
#include "TGeoBBox.h"
#include "TGeoTrd1.h"
#include "TGeoCompositeShape.h"
#include "TGeoBoolNode.h"
#include "TGeoTube.h"
#include "TGeoMaterial.h"
#include "FairGeoInterface.h"
#include "FairGeoMedia.h"
#include "FairGeoBuilder.h"
#include "FairRuntimeDb.h"              // for FairRuntimeDb
#include "TVectorT.h"
#include "TFile.h"
#include <iostream>                     // for operator<<, basic_ostream, etc

Double_t cm = 1;
Double_t m = 100 * cm;
Double_t mm = 0.1 * cm;
Double_t kilogauss = 1.;
Double_t tesla = 10 * kilogauss;

MiniShield::~MiniShield() {}
MiniShield::MiniShield() : FairModule("MiniShield", "") {}

MiniShield::MiniShield(TString geofile)
  : FairModule("MuonShield", "MiniShield")
{
  fGeofile = geofile;
  auto f = TFile::Open(geofile, "read");
  TVectorT<Double_t> params;
  params.Read("params");
  Double_t LE = 10. * m, floor = 5. * m;
  fDesign = 8;
  fField = 1.7;
  dZ0 = 1 * m;
  dZ1 = 0.4 * m;
  dZ2 = 2.31 * m;
  dZ3 = params[2];
  dZ4 = params[3];
  dZ5 = params[4];
  dZ6 = params[5];
  dZ7 = params[6];
  dZ8 = params[7];
  fMiniShieldLength = 2 * (dZ1 + dZ2 + dZ3 + dZ4 + dZ5 + dZ6 + dZ7 + dZ8) + LE;

  fFloor = floor;
  fSupport = true;

  Double_t Z = -25 * m - fMiniShieldLength / 2.;

  zEndOfAbsorb = Z + dZ0 - fMiniShieldLength / 2.;
  zEndOfAbsorb -= dZ0;
}

MiniShield::MiniShield(const char* name, const Int_t Design, const char* Title,
                               Double_t Z, Double_t L0, Double_t L1, Double_t L2, Double_t L3, Double_t L4, Double_t L5, Double_t L6,
                               Double_t L7, Double_t L8, Double_t gap, Double_t LE, Double_t, Double_t floor, Double_t field, const Int_t withCoMagnet, const Bool_t StepGeo)
  : FairModule(name ,Title)
{
 fDesign = Design;
 fField  = field;
 fGeofile = "";
 fStepGeo = StepGeo;
 fWithCoMagnet = withCoMagnet;
 if (fDesign==1){
     fMiniShieldLength = L1;   
    }
 if (fDesign==2 || fDesign==3 || fDesign==4 ){
     Fatal("MiniShield","Design %i not anymore supported",fDesign);
    }
 if (fDesign==5 || fDesign==6){
     dZ0 = L0;
     dZ1 = L1;
     dZ2 = L2;
     dZ3 = L3;
     dZ4 = L4;
     dZ5 = L5;
     dZ6 = L6;
     dZ7 = L7;
     dZ8 = L8;
     dXgap= gap;
     fMiniShieldLength = 2*(dZ1+dZ2+dZ3+dZ4+dZ5+dZ6+dZ7+dZ8) + LE ; //leave some space for nu-tau detector   
    }
    
 if (fDesign>=7){
     dZ1 = L1;
     dZ2 = L2;
     dZ3 = L3;
     dZ4 = L4;
     dZ5 = L5;
     dZ6 = L6;
     dZ7 = L7;
     dZ8 = L8;
     fMiniShieldLength =
	 2 * (dZ1 + dZ2 + dZ3 + dZ4 + dZ5 + dZ6 + dZ7 + dZ8) + LE;
   }
    
 fFloor = (fDesign >= 7) ? floor : 0;

 zEndOfAbsorb = Z + dZ0 - fMiniShieldLength/2.;   
 if(fDesign>=6){zEndOfAbsorb = Z - fMiniShieldLength/2.;}
 fSupport = true;
}

// -----   Private method InitMedium 
Int_t MiniShield::InitMedium(TString name) 
{
   static FairGeoLoader *geoLoad=FairGeoLoader::Instance();
   static FairGeoInterface *geoFace=geoLoad->getGeoInterface();
   static FairGeoMedia *media=geoFace->getMedia();
   static FairGeoBuilder *geoBuild=geoLoad->getGeoBuilder();

   FairGeoMedium *ShipMedium=media->getMedium(name);

   if (!ShipMedium)
     Fatal("InitMedium","Material %s not defined in media file.", name.Data());
   TGeoMedium* medium=gGeoManager->GetMedium(name);
   if (medium)
     return ShipMedium->getMediumIndex();
   return geoBuild->createMedium(ShipMedium);
}

void MiniShield::CreateTube(TString tubeName, TGeoMedium *medium,
				Double_t dX, Double_t dY, Double_t dZ,
				Int_t color, TGeoVolume *tShield,
				Double_t x_translation, Double_t y_translation,
				Double_t z_translation) {
  TGeoVolume *absorber = gGeoManager->MakeTube(tubeName, medium, dX, dY, dZ);
  absorber->SetLineColor(color);
  tShield->AddNode(
      absorber, 1,
      new TGeoTranslation(x_translation, y_translation, z_translation));
}

void MiniShield::CreateArb8(TString arbName, TGeoMedium *medium,
				Double_t dZ, std::array<Double_t, 16> corners,
				Int_t color, TGeoUniformMagField *magField,
				TGeoVolume *tShield, Double_t x_translation,
				Double_t y_translation,
				Double_t z_translation) {
  TGeoVolume *magF =
      gGeoManager->MakeArb8(arbName, medium, dZ, corners.data());
  magF->SetLineColor(color);
  if (fDesign != 11 || arbName.Contains("Absorb")){magF->SetField(magField);}
  tShield->AddNode(magF, 1, new TGeoTranslation(x_translation, y_translation,
						z_translation));
}

void MiniShield::CreateArb8(TString arbName, TGeoMedium *medium,
          Double_t dZ, std::array<Double_t, 16> corners,
          Int_t color, TGeoUniformMagField *magField,
          TGeoVolume *tShield, Double_t x_translation,
          Double_t y_translation,
          Double_t z_translation, 
          Bool_t stepGeo) {
  if (!stepGeo)
  {
    CreateArb8 (arbName, medium, dZ, corners, color, magField, tShield, x_translation, y_translation, z_translation);
    return;
  }
  Double_t partLength = 0.5;
  Int_t zParts = std::ceil(2.0*dZ/m/partLength);
  Double_t finalCorners[zParts][16];
  Double_t dxdy[4][2];
  Double_t dZp = dZ/Double_t(zParts);

  for (int i = 0; i < 4; ++i)
  {
    dxdy[i][0] = (corners[8+2*i] - corners[0+2*i])/Double_t(zParts);
    dxdy[i][1] = (corners[9+2*i] - corners[1+2*i])/Double_t(zParts);
  }

  std::copy(corners.data() + 0,  corners.data() + 8, finalCorners[0]);

  for (int i = 0; i < zParts; ++i)
  {
    for (int k = 0; k < 4; ++k)
    {
      finalCorners[i][8+2*k] = finalCorners[i][0+2*k] + dxdy[k][0];
      finalCorners[i][9+2*k] = finalCorners[i][1+2*k] + dxdy[k][1];
    }
    if (i != zParts-1)
    {
      std::copy(finalCorners[i] + 8, finalCorners[i] + 16, finalCorners[i+1]);
    }
  }
  
  for (int i = 0; i < zParts; ++i)
  {
    for (int k = 0; k < 4; ++k)
    {
      finalCorners[i][8+2*k] = finalCorners[i][0+2*k]  = (finalCorners[i][0+2*k] + finalCorners[i][8+2*k]) / 2.0;
      finalCorners[i][9+2*k] = finalCorners[i][1+2*k]  = (finalCorners[i][9+2*k] + finalCorners[i][1+2*k]) / 2.0;
    }
  }

  std::vector<TGeoVolume*> magF;
  
  for (int i = 0; i < zParts; ++i)
  {
    magF.push_back(gGeoManager->MakeArb8(arbName + '_' + std::to_string(i), medium, dZp - 0.00001*m, finalCorners[i]));
    magF[i]->SetLineColor(color);
    magF[i]->SetField(magField);
  }

  for (int i = 0; i < zParts; ++i)
  {
    Double_t true_z_translation = z_translation + 2.0 * Double_t(i) * dZp - dZ + dZp;
    tShield->AddNode(magF[i], 1, new TGeoTranslation(x_translation, y_translation, true_z_translation));
  }
}

void MiniShield::CreateMagnet(TString magnetName,TGeoMedium* medium,TGeoVolume *tShield,TGeoUniformMagField *field,
				  Double_t dX, Double_t dY, Double_t dZ,
          Double_t Z
          )
  {
    TGeoBBox* mainMagnet = new TGeoBBox("miniShield", dX, dY, dZ);
    mainMagnet->SetField(field)
    tShield->AddNode(mainMagnet, 1, new TGeoTranslation(0,0,Z));
    
  }

Int_t MiniShield::Initialize(std::vector<TString> &magnetName,
				std::vector<Double_t> &dXIn, std::vector<Double_t> &dYIn,
				std::vector<Double_t> &dXOut, std::vector<Double_t> &dYOut,
				std::vector<Double_t> &dZ, std::vector<Double_t> &midGapIn,
				std::vector<Double_t> &midGapOut,
				std::vector<Double_t> &HmainSideMagIn,
				std::vector<Double_t> &HmainSideMagOut,
				std::vector<Double_t> &gapIn, std::vector<Double_t> &gapOut,
				std::vector<Double_t> &Z) {

    auto f = TFile::Open(fGeofile, "read");
    TVectorT<Double_t> params;
    params.Read("params");

  return nMagnets;
}
void MiniShield::ConstructGeometry()
{
    TGeoVolume *top=gGeoManager->GetTopVolume();
    TGeoVolume *tShield = new TGeoVolumeAssembly("MiniShieldArea");
    InitMedium("steel");
    TGeoMedium *steel =gGeoManager->GetMedium("steel");
    InitMedium("iron");
    TGeoMedium *iron  =gGeoManager->GetMedium("iron");
    InitMedium("Concrete");
    TGeoMedium *concrete  =gGeoManager->GetMedium("Concrete");

    Double_t ironField = fField*tesla;
    TGeoUniformMagField *mainField = new TGeoUniformMagField(0.,ironField,0.);
   
	  CreateMagnet("MiniShield",iron,tShield,mainField, 100., 100., 100., 0.);

    top->AddNode(tShield, 1);
}
ClassImp(MiniShield)
