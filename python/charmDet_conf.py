#!/usr/bin/env python
# -*- coding: latin-1 -*-
import ROOT,os
import shipunit as u
from ShipGeoConfig import ConfigRegistry
detectorList = []

def getParameter(x,ship_geo,latestCharmGeo):
  lv = x.split('.')
  last = lv[len(lv)-1]
  top = ''
  for l in range(len(lv)-1): 
    top += lv[l]
    if l<len(lv)-2: top +='.' 
  a = getattr(ship_geo,top)
  if hasattr(a,last): return getattr(a,last)
# not in the list of recorded parameteres. probably added after
# creation of file. Check newest geometry_config:
  a = getattr(latestCharmGeo,top)
  return getattr(a,last)

def configure(run,ship_geo,Gfield=''):
 latestCharmGeo = ConfigRegistry.loadpy("$FAIRSHIP/geometry/charm-geometry_config.py")
# -----Create media-------------------------------------------------
 run.SetMaterials("media.geo")  # Materials
 
# -----Create geometry----------------------------------------------
 cave= ROOT.ShipCave("CAVE")
 cave.SetGeometryFileName("caveWithAir.geo")
 detectorList.append(cave)

 if ship_geo.optParams and ship_geo.muShieldDesign !=8:
    MiniShield = ROOT.ShipMuonShield(
        ship_geo.optParams, "MuonShield", ship_geo.muShieldDesign, "ShipMuonShield",
        ship_geo.muShield.z, ship_geo.muShield.dZ0, ship_geo.muShield.dZ1,
        ship_geo.muShield.dZ2, ship_geo.muShield.dZ3,
        ship_geo.muShield.dZ4, ship_geo.muShield.dZ5,
        ship_geo.muShield.dZ6, ship_geo.muShield.dZ7,
        ship_geo.muShield.dZ8, ship_geo.muShield.dXgap,
        ship_geo.muShield.LE, ship_geo.Yheight * 4. / 10.,
        ship_geo.cave.floorHeightMuonShield,ship_geo.muShield.Field,
        ship_geo.muShieldWithCobaltMagnet, ship_geo.muShieldStepGeo,
        ship_geo.hadronAbsorber.WithConstField, ship_geo.muShield.WithConstField)
    detectorList.append(MiniShield)
 else:
   if ship_geo.muShieldDesign in [3, 4, 5, 6, 7, 9]:
    MuonShield = ROOT.ShipMuonShield(
       "MuonShield", ship_geo.muShieldDesign, "ShipMuonShield",
       ship_geo.muShield.z, ship_geo.muShield.dZ0, ship_geo.muShield.dZ1,
       ship_geo.muShield.dZ2, ship_geo.muShield.dZ3,
       ship_geo.muShield.dZ4, ship_geo.muShield.dZ5,
       ship_geo.muShield.dZ6, ship_geo.muShield.dZ7,
       ship_geo.muShield.dZ8, ship_geo.muShield.dXgap,
       ship_geo.muShield.LE, ship_geo.Yheight * 4. / 10.,
       ship_geo.cave.floorHeightMuonShield, ship_geo.muShield.Field,
       ship_geo.muShieldWithCobaltMagnet, ship_geo.muShieldStepGeo,
       ship_geo.hadronAbsorber.WithConstField, ship_geo.muShield.WithConstField)

   elif ship_geo.muShieldDesign == 8:
    MuonShield = ROOT.ShipMuonShield(ship_geo.muShield.z, ship_geo.muShieldGeo,
                                   ship_geo.muShieldWithCobaltMagnet,
                                   ship_geo.muShieldStepGeo,
                                   ship_geo.hadronAbsorber.WithConstField,
                                   ship_geo.muShield.WithConstField)
   elif ship_geo.muShieldDesign == 20:
    MuonShield = ROOT.ShipMuonShield("MuonShield", 1.1, ship_geo.muShieldDesign, "ShipMuonShield", ship_geo.muShield.Start_Z, ship_geo.muShield.Z, ship_geo.muShield.H1, ship_geo.muShield.Field, ship_geo.muShield.Gap)

   detectorList.append(MuonShield)

 Veto = ROOT.veto("Veto", ROOT.kTRUE)  # vacuum tank
 if ship_geo.muShieldDesign == 20:
  Veto.SetSensePlaneZ(
    ship_geo.SensPlane.z_1,
    ship_geo.SensPlane.z_2,
    ship_geo.muShield.Start_Z - 10*u.cm,
    ship_geo.muShield.Start_Z + 2.*ship_geo.muShield.Z + ship_geo.muShield.Gap,
    ship_geo.muShield.Start_Z + 2.*2.*ship_geo.muShield.Z + 3.*ship_geo.muShield.Gap ,
    ship_geo.muShield.Start_Z + 2.*3.*ship_geo.muShield.Z + 5.*ship_geo.muShield.Gap, 
    ship_geo.muShield.Start_Z + 2.*4.*ship_geo.muShield.Z + 7.*ship_geo.muShield.Gap,
    ship_geo.muShield.Start_Z + 2.*4.*ship_geo.muShield.Z + 9.*ship_geo.muShield.Gap + 100*u.cm)
 else:
  Veto.SetSensePlaneZ(ship_geo.SensPlane.z_1, ship_geo.SensPlane.z_2, ship_geo.SensPlane.z_3)
 detectorList.append(Veto)

 Goliath = ROOT.GoliathMagnet("Goliath")
 #Goliath.SetTransverseSizes(ship_geo.Goliath.D1Short, ship_geo.Goliath.D1Long)
 Goliath.SetGoliathSizes(ship_geo.Goliath.H, ship_geo.Goliath.TS, ship_geo.Goliath.LS,
                              ship_geo.Goliath.BasisH);
 Goliath.SetCoilParameters(ship_geo.Goliath.CoilR, ship_geo.Goliath.UpCoilH,
                                ship_geo.Goliath.LowCoilH, ship_geo.Goliath.CoilD);
 Goliath.SetGoliathCentre(ship_geo.Goliath.goliathcentre_to_beam)
 Goliath.SetGoliathCentreZ(ship_geo.Goliath.goliathcentre)

 if ship_geo.muShieldDesign!=8:
  detectorList.append(Goliath)

 for x in detectorList:
  run.AddModule(x)
 
# return list of detector elements
 detElements = {}
 for x in run.GetListOfModules(): detElements[x.GetName()]=x 
 
 return detElements
