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
  fField = 2.0;
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
    TGeoVolume* mainMagnet = gGeoManager->MakeBox(magnetName, medium, dX, dY, dZ);
    mainMagnet->SetField(field);
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

  return 0;
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
    TGeoUniformMagField *mainField = new TGeoUniformMagField(0., 2.0*tesla, 0.);
   
	  CreateMagnet("MiniShield",iron,tShield,mainField, 500./2., 500./2., 500./2.0, -6250.);

    top->AddNode(tShield, 1);


    float mField = 1.6 * tesla;
    TGeoUniformMagField *fieldsAbsorber[4] = {
      new TGeoUniformMagField(0., mField, 0.),
      new TGeoUniformMagField(0., -mField, 0.),
      new TGeoUniformMagField(-mField, 0., 0.),
      new TGeoUniformMagField(mField, 0., 0.)
    };
    magnetName = {"MagnAbsorb1", "MagnAbsorb2", "Magn1", "Magn2", "Magn3",
       "Magn4", "Magn5", "Magn6", "Magn7"
     };
    fieldDirection = {
        FieldDirection::up, FieldDirection::up, FieldDirection::up,
        FieldDirection::up, FieldDirection::up, FieldDirection::down,
        FieldDirection::down, FieldDirection::down, FieldDirection::down,
     };
     dZgap = 0.1 * m;
     zGap = 0.5 * dZgap;
     dZ1 =  0.35 * m + zGap;
     
     dXIn[0] = 0.4 * m;
     dXOut[0] = 0.40 * m;
     dYIn[0] = 1.5 * m;
     dYOut[0] = 1.5 * m;
     gapIn[0] = 0.1 * mm;
     gapOut[0] = 0.1 * mm;
     dZ[0] = dZ1 - zgap / 2;
     Z[0] = zEndOfAbsorb + dZ[0] + zgap;

     dXIn[1] = 0.5 * m;
     dXOut[1] = 0.5 * m;
     dYIn[1] = 1.3 * m;
     dYOut[1] = 1.3 * m;
     gapIn[1] = 0.02 * m;
     gapOut[1] = 0.02 * m;
     dZ[1] = dZ2 - zgap / 2;
     Z[1] = Z[0] + dZ[0] + dZ[1] + zgap;

     dXIn[2] = 0.72 * m;
     dXOut[2] = 0.51 * m;
     dYIn[2] = 0.29 * m;
     dYOut[2] = 0.46 * m;
     gapIn[2] = 0.10 * m;
     gapOut[2] = 0.07 * m;
     dZ[2] = dZ3 - zgap / 2;
     Z[2] = Z[1] + dZ[1] + dZ[2] + 2 * zgap;

     dXIn[3] = 0.54 * m;
     dXOut[3] = 0.38 * m;
     dYIn[3] = 0.46 * m;
     dYOut[3] = 1.92 * m;
     gapIn[3] = 0.14 * m;
     gapOut[3] = 0.09 * m;
     dZ[3] = dZ4 - zgap / 2;
     Z[3] = Z[2] + dZ[2] + dZ[3] + zgap;

     dXIn[4] = 0.10 * m;
     dXOut[4] = 0.31 * m;
     dYIn[4] = 0.35 * m;
     dYOut[4] = 0.31 * m;
     gapIn[4] = 0.51 * m;
     gapOut[4] = 0.11 * m;
     dZ[4] = dZ5 - zgap / 2;
     Z[4] = Z[3] + dZ[3] + dZ[4] + zgap;

     dXIn[5] = 0.03 * m;
     dXOut[5] = 0.32 * m;
     dYIn[5] = 0.54 * m;
     dYOut[5] = 0.24 * m;
     gapIn[5] = 0.08 * m;
     gapOut[5] = 0.08 * m;
     dZ[5] = dZ6 - zgap / 2;
     Z[5] = Z[4] + dZ[4] + dZ[5] + zgap;

     dXIn[6] = 0.22 * m;
     dXOut[6] = 0.32 * m;
     dYIn[6] = 2.09 * m;
     dYOut[6] = 0.35 * m;
     gapIn[6] = 0.08 * m;
     gapOut[6] = 0.13 * m;
     dZ[6] = dZ7 - zgap / 2;
     Z[6] = Z[5] + dZ[5] + dZ[6] + zgap;

     dXIn[7] = 0.33 * m;
     dXOut[7] = 0.77 * m;
     dYIn[7] = 0.85 * m;
     dYOut[7] = 2.41 * m;
     gapIn[7] = 0.09 * m;
     gapOut[7] = 0.26 * m;
     dZ[7] = dZ8 - zgap / 2;
     Z[7] = Z[6] + dZ[6] + dZ[7] + zgap;

     dXIn[8] = dXOut[7];
     dYIn[8] = dYOut[7];
     dXOut[8] = dXIn[8];
     dYOut[8] = dYIn[8];
     gapIn[8] = gapOut[7];
     gapOut[8] = gapIn[8];
     dZ[8] = 0.1 * m;
     Z[8] = Z[7] + dZ[7] + dZ[8];

     for (int i = 0; i < 8; ++i) {
        midGapIn[i] = 0.;
        midGapOut[i] = 0.;
        HmainSideMagIn[i] = dYIn[i] / 2;
        HmainSideMagOut[i] = dYOut[i] / 2;
     }
    for (Int_t nM = 0; nM < 2; nM++) {
    CreateMagnet(magnetName[nM], iron, tShield, fieldsAbsorber,
           fieldDirection[nM], dXIn[nM], dYIn[nM], dXOut[nM],
           dYOut[nM], dZf[nM], midGapIn[nM], midGapOut[nM],
           HmainSideMagIn[nM], HmainSideMagOut[nM], gapIn[nM],
           gapOut[nM], Z[nM], true, false);
  }

      std::vector<TGeoTranslation*> mag_trans;

      auto mag2 = new TGeoTranslation("mag2", 0, 0, +dZ1);
      mag2->RegisterYourself();
      mag_trans.push_back(mag2);

      Double_t zgap = 10;
      Double_t absorber_offset = zgap;
      Double_t absorber_half_length = (dZf[0] + dZf[1]) + zgap / 2.;
      auto abs = new TGeoBBox("absorber", 3.95 * m, 3.4 * m, absorber_half_length);
      const std::vector<TString> absorber_magnets =
         (fDesign == 7) ? std::vector<TString>{"MagnAbsorb1", "MagnAbsorb2"} : std::vector<TString>{"MagnAbsorb2"};
      const std::vector<TString> magnet_components = fDesign == 7 ? std::vector<TString>{
    "_MiddleMagL", "_MiddleMagR",  "_MagRetL",    "_MagRetR",
    "_MagCLB",     "_MagCLT",      "_MagCRT",     "_MagCRB",
    "_MagTopLeft", "_MagTopRight", "_MagBotLeft", "_MagBotRight",
      }: std::vector<TString>{
    "_MiddleMagL", "_MiddleMagR",  "_MagRetL",    "_MagRetR",
    "_MagTopLeft", "_MagTopRight", "_MagBotLeft", "_MagBotRight",
      };
      TString absorber_magnet_components;
      for (auto &&magnet_component : magnet_components) {
  // format: "-<magnetName>_<magnet_component>:<translation>"
  absorber_magnet_components +=
      ("-" + absorber_magnets[0] + magnet_component + ":" +
       mag_trans[0]->GetName());
  if (fDesign == 7) {
  absorber_magnet_components +=
      ("-" + absorber_magnets[1] + magnet_component + ":" +
       mag_trans[1]->GetName());
  }
      }
      TGeoCompositeShape *absorberShape = new TGeoCompositeShape(
    "Absorber", "absorber" + absorber_magnet_components); // cutting out
                // magnet parts
                // from absorber
      TGeoVolume *absorber = new TGeoVolume("AbsorberVol", absorberShape, iron);
      absorber->SetLineColor(42); // brown / light red
      tShield->AddNode(absorber, 1, new TGeoTranslation(0, 0, zEndOfAbsorb + absorber_half_length + absorber_offset));

      
     auto coatBox = new TGeoBBox("coat", 10 * m - 1 * mm, 10 * m - 1 * mm, absorber_half_length);
     auto coatShape = new TGeoCompositeShape("CoatShape", "coat-absorber");
     auto coat = new TGeoVolume("CoatVol", coatShape, concrete);
     tShield->AddNode(coat, 1, new TGeoTranslation(0, 0, zEndOfAbsorb + absorber_half_length + absorber_offset ));
     TGeoVolume *coatWall = gGeoManager->MakeBox("CoatWall",concrete,10 * m - 1 * mm, 10 * m - 1 * mm, 7 * cm - 1 * mm);
     coatWall->SetLineColor(kRed);
     tShield->AddNode(coatWall, 1, new TGeoTranslation(0, 0, zEndOfAbsorb + 2*absorber_half_length + absorber_offset+7 * cm));

      
}
ClassImp(MiniShield)
