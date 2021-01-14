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

 detectorList.append(MuonShield)

 TargetStation = ROOT.MufluxTargetStation("MufluxTargetStation",ship_geo.target.length,ship_geo.hadronAbsorber.length, ship_geo.target.z,ship_geo.hadronAbsorber.z,ship_geo.targetOpt,ship_geo.target.sl)

 TargetStation.SetIronAbsorber(ship_geo.MufluxTargetStation.absorber_x,ship_geo.MufluxTargetStation.absorber_y)
 TargetStation.SetAbsorberCutout(ship_geo.MufluxTargetStation.absorbercutout_x, ship_geo.MufluxTargetStation.absorbercutout_y)
 TargetStation.SetIronShield(ship_geo.MufluxTargetStation.ironshield_x, ship_geo.MufluxTargetStation.ironshield_y, ship_geo.MufluxTargetStation.ironshield_z)
 TargetStation.SetConcreteShield(ship_geo.MufluxTargetStation.concreteshield_x, ship_geo.MufluxTargetStation.concreteshield_y, ship_geo.MufluxTargetStation.concreteshield_z)
 TargetStation.SetAboveTargetShield(ship_geo.MufluxTargetStation.abovetargetshield_x, ship_geo.MufluxTargetStation.abovetargetshield_y,ship_geo.MufluxTargetStation.abovetargetshield_z)
 TargetStation.SetAboveAbsorberShield(ship_geo.MufluxTargetStation.aboveabsorbershield_x, ship_geo.MufluxTargetStation.aboveabsorbershield_y,ship_geo.MufluxTargetStation.aboveabsorbershield_z)
 TargetStation.SetAboveAboveTargetShield(ship_geo.MufluxTargetStation.aboveabovetargetshield_y)
 TargetStation.SetFloor(ship_geo.MufluxTargetStation.floor_x,ship_geo.MufluxTargetStation.floor_y,ship_geo.MufluxTargetStation.floor_z)
 #TargetStation.SetFloorT34(ship_geo.MufluxTargetStation.floorT34_x,ship_geo.MufluxTargetStation.floorT34_y,ship_geo.MufluxTargetStation.floorT34_z)
 #TargetStation.SetFloorRPC(ship_geo.MufluxTargetStation.floorRPC_x, ship_geo.MufluxTargetStation.floorRPC_y,ship_geo.MufluxTargetStation.floorRPC_z)

 if ship_geo.targetOpt>10:
  slices_length=ROOT.std.vector('float')()
  slices_material=ROOT.std.vector('string')()
  for i in range(1,ship_geo.targetOpt+1):
   slices_length.push_back(eval("ship_geo.target.L"+str(i)))
   slices_material.push_back(eval("ship_geo.target.M"+str(i)))

 TargetStation.SetLayerPosMat(ship_geo.target.xy,slices_length,slices_material)
 detectorList.append(TargetStation)

 #detectorList.append(MufluxSpectrometer)

 Veto = ROOT.veto("Veto", ROOT.kTRUE)  # vacuum tank
 Veto.SetSensePlaneZ(ship_geo.SensPlane.z)
 detectorList.append(Veto)

 for x in detectorList:
  run.AddModule(x)
 
# return list of detector elements
 detElements = {}
 for x in run.GetListOfModules(): detElements[x.GetName()]=x 
 
 return detElements
