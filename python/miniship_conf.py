#!/usr/bin/env python
# -*- coding: latin-1 -*-
from __future__ import print_function
from __future__ import division
import ROOT,os
import shipunit as u
from ShipGeoConfig import AttrDict,ConfigRegistry
detectorList = []

def getParameter(x,ship_geo,latestShipGeo):
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
  a = getattr(latestShipGeo,top)
  return getattr(a,last)
    
def posHcal(z,hfile,HcalOption): 
 HcalZSize = 0
 sz = hfile+"z"+str(z)+".geo"
 floc = os.environ["FAIRSHIP"]+"/geometry"
 f_hcal  = floc+"/"+hfile
 f_hcalz = floc+"/"+sz
 f = open(f_hcal) 
 rewrite = True
 if sz in os.listdir(floc):
  test = os.popen("diff "+ f_hcal+ " "+ f_hcalz).read()
  if str.count(test,'---')==1 and not test.find('Position')<0: rewrite = False # only different is z position
 if rewrite: fn = open(f_hcalz,'w')
 for l in f.readlines():
   if rewrite:
    if not l.find("ZPos")<0:
      l ="ZPos="+str(z)+ "	#Position of Hcal  center	[cm]\n"
    fn.write(l)
   if not l.find("HcalZSize")<0:
     HcalZSize = float(l[len('HcalZSize')+1:].split('#')[0]) 
 f.close()
 if rewrite: fn.close()
 if HcalOption==2: hcal = ROOT.hcal("Hcal", ROOT.kFALSE, sz)
 else:                      hcal = ROOT.hcal("Hcal", ROOT.kTRUE, sz)
 return hcal,HcalZSize
def makeEcalGeoFile(z,efile):
 EcalZSize = 0
 sz = efile+"z"+str(z)+".geo"
 floc = os.environ["FAIRSHIP"]+"/geometry"
 f_ecal  = floc+"/"+efile
 f_ecalz = floc+"/"+sz
 f = open(f_ecal) 
 rewrite = True
 if sz in os.listdir(floc):
  test = os.popen("diff "+ f_ecal+ " "+ f_ecalz).read()
  if str.count(test,'---')==1 and not test.find('Position')<0: rewrite = False # only different is z position
 if rewrite: fn = open(f_ecalz,'w')
 for l in f.readlines():
   if rewrite:
    if not l.find("ZPos")<0:
      l ="ZPos="+str(z)+ "	#Position of Ecal start		[cm]\n"
    fn.write(l)
   if not l.find("EcalZSize")<0:
     EcalZSize = float(l[len('EcalZSize')+1:].split('#')[0]) 
 f.close()
 if rewrite: fn.close()  
 return EcalZSize,sz
def posEcal(z,efile):
 EcalZSize,sz = makeEcalGeoFile(z,efile)
 ecal = ROOT.ecal("Ecal", ROOT.kTRUE, sz)
 return ecal,EcalZSize

def configure(run,ship_geo):
# ---- for backward compatibility ----
 if not hasattr(ship_geo,"tankDesign"): ship_geo.tankDesign = 5
 if not hasattr(ship_geo,"muShieldGeo"): ship_geo.muShieldGeo = None
 if not hasattr(ship_geo.hcal,"File"):  ship_geo.hcal.File = "hcal.geo"
 if not hasattr(ship_geo.Bfield,'x') :  ship_geo.Bfield.x   = 3.*u.m
 if not hasattr(ship_geo,'cave') :       
   ship_geo.cave = AttrDict(z=0*u.cm)
   ship_geo.cave.floorHeightMuonShield = 5*u.m
   ship_geo.cave.floorHeightTankA   = 4.5*u.m
   ship_geo.cave.floorHeightTankB   = 2.*u.m
 if not hasattr(ship_geo,'NuTauTT') : ship_geo.NuTauTT= AttrDict(z=0*u.cm)
 if not hasattr(ship_geo.NuTauTT,'design') : ship_geo.NuTauTT.design = 0
 if not hasattr(ship_geo,'EcalOption'):     ship_geo.EcalOption = 1      
 latestShipGeo = ConfigRegistry.loadpy("$FAIRSHIP/geometry/miniship_config.py")
# -----Create media-------------------------------------------------
 run.SetMaterials("media.geo")  # Materials
# ------------------------------------------------------------------------
  
# -----Create geometry----------------------------------------------
 cave= ROOT.ShipCave("CAVE")
 cave.SetGeometryFileName("cave.geo")
 detectorList.append(cave)
 # MiniShield = ROOT.MiniShield("MiniShield") 

 TargetStation = ROOT.ShipTargetStation("TargetStation",ship_geo.target.length,
                                                        ship_geo.target.z,ship_geo.targetOpt,ship_geo.target.sl);
 if ship_geo.targetOpt>10:
  slices_length   = ROOT.std.vector('float')()
  slices_material = ROOT.std.vector('std::string')()
  for i in range(1,ship_geo.targetOpt+1):
   slices_length.push_back(  eval("ship_geo.target.L"+str(i)))
   slices_material.push_back(eval("ship_geo.target.M"+str(i)))
  TargetStation.SetLayerPosMat(ship_geo.target.xy,slices_length,slices_material)
 detectorList.append(TargetStation)




 MiniShield = ROOT.MiniShield(
            "MiniShield", 0, "MiniMuonShield",
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
 fluxDet = ROOT.fluxDet("fluxDet", ROOT.kTRUE)
 detectorList.append(fluxDet)

#-----   Magnetic field   -------------------------------------------
 # if not hasattr(ship_geo.Bfield,"fieldMap"):
 #  if ship_geo.strawDesign == 4 or ship_geo.strawDesign == 10 : fMagField = ROOT.ShipBellField("wilfried", ship_geo.Bfield.max ,ship_geo.Bfield.z,2,ship_geo.Yheight/2.*u.m )  
 #  else :                                                      fMagField = ROOT.ShipBellField("wilfried", ship_geo.Bfield.max ,ship_geo.Bfield.z,1,ship_geo.Yheight/2.*u.m )  
 #  if ship_geo.muShieldDesign==6: fMagField.IncludeTarget(ship_geo.target.xy, ship_geo.target.z0, ship_geo.target.length)
 #  run.SetField(fMagField)
#
 exclusionList = []
 #exclusionList = ["Muon","Ecal","Hcal","Strawtubes","TargetTrackers","NuTauTarget","HighPrecisionTrackers",\
 #                 "Veto","Magnet","MuonShield","TargetStation","NuTauMudet","EmuMagnet", "TimeDet", "UpstreamTagger"]

 for x in detectorList:
   if x.GetName() in exclusionList: continue
   run.AddModule(x)
# return list of detector elements
 detElements = {}
 for x in run.GetListOfModules(): detElements[x.GetName()]=x
 return detElements
