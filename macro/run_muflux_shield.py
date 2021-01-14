from __future__ import print_function
from __future__ import division
import os
import sys
import getopt
import ROOT as r
import makeALPACAEvents

# Fix https://root-forum.cern.ch/t/pyroot-hijacks-help/15207 :
r.PyConfig.IgnoreCommandLineOptions = True

import shipunit as u
import shipRoot_conf
import rootUtils as ut
from ShipGeoConfig import ConfigRegistry
from argparse import ArgumentParser

import charmDet_conf as shipDet_conf
import geomGeant4
import saveBasicParameters

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()

parser.add_argument("--FollowMuon", dest="followMuon", help="Make muonshield active to follow muons", required=False,
                    action="store_true")
parser.add_argument("--FastMuon", dest="fastMuon", help="Only transport muons for a fast muon only background estimate",
                    required=False, action="store_true")
parser.add_argument("-n", "--nEvents", dest="nEvents", help="Number of events to generate", required=False, default=100,
                    type=int)
parser.add_argument("-i", "--firstEvent", dest="firstEvent", help="First event of input file to use", required=False,
                    default=0, type=int)
parser.add_argument("-s", "--seed", dest="theSeed",
                    help="Seed for random number. Only for experts, see TRrandom::SetSeed documentation",
                    required=False, default=0, type=int)
parser.add_argument("-S", "--sameSeed", dest="sameSeed",
                    help="can be set to an integer for the muonBackground simulation with specific seed for each muon, only for experts!" \
                    , required=False, default=False, type=int)
parser.add_argument("--phiRandom", dest="phiRandom",  help="only relevant for muon background generator, random phi", required=False, action="store_true")
group.add_argument("-f", dest="inputFile", help="Input file if not default file", required=False, default=False)
parser.add_argument("-g", dest="geofile", help="geofile for muon shield geometry, for experts only", required=False,
                    default=None)
parser.add_argument("-o", "--output", dest="outputDir", help="Output directory", required=False, default=".")
parser.add_argument("--stepMuonShield", dest="muShieldStepGeo", help="activate steps geometry for the muon shield",
                    required=False, action="store_true", default=False)
parser.add_argument("--coMuonShield", dest="muShieldWithCobaltMagnet",
                    help="replace one of the magnets in the shield with 2.2T cobalt one, downscales other fields, works only for muShieldDesign >2",
                    required=False, type=int, default=0)
parser.add_argument("--muShieldDesign", dest="ds", help="5=TP muon shield, 6=magnetized hadron, 7=short magnet design, 9=optimised with T4 as constraint, 8=requires config file\
                                            ,10=with field map for hadron absorber", required=False,
                    default=9, type=int)

options = parser.parse_args()

if options.muShieldWithCobaltMagnet and options.ds < 3:
    print("--coMuonShield works only for muShieldDesign >2")
    sys.exit()

print('FairShip setup to produce', options.nEvents, 'events')
print("STPEGEO:{}".format(options.muShieldStepGeo))

r.gRandom.SetSeed(options.theSeed)
shipRoot_conf.configure(0)

ship_geo = ConfigRegistry.loadpy("$FAIRSHIP/geometry/charm-geometry_config.py",
                                 muShieldDesign=options.ds,
                                 muShieldGeo=options.geofile,
                                 muShieldStepGeo=options.muShieldStepGeo,
                                 muShieldWithCobaltMagnet=options.muShieldWithCobaltMagnet)

if not os.path.exists(options.outputDir):
    os.makedirs(options.outputDir)
tag = "MiniShield.MuonBack"
outFile = "%s/ship.%s.root" % (options.outputDir, tag)
mcEngine = "TGeant4"

run = r.FairRunSim()
run.SetName(mcEngine)  # Transport engine
run.SetOutputFile(outFile)  # Output file
# user configuration file default g4Config.C
run.SetUserConfig('g4Config.C')
modules = shipDet_conf.configure(run, ship_geo)
primGen = r.FairPrimaryGenerator()

fileType = ut.checkFileExists(options.inputFile)
if fileType == 'tree':
    # 2018 background production
    primGen.SetTarget(ship_geo.target.z0 + 70.845 * u.m, 0.)
else:
    primGen.SetTarget(ship_geo.target.z0 + 50 * u.m, 0.)

MuonBackgen = r.MuonBackGenerator()
MuonBackgen.Init(options.inputFile, options.firstEvent,options.phiRandom)
if options.sameSeed:
    MuonBackgen.SetSameSeed(options.sameSeed)
primGen.AddGenerator(MuonBackgen)
if not options.nEvents:
    n_events = MuonBackgen.GetNevents()
else:
    n_events = min(options.nEvents, MuonBackgen.GetNevents())
print('Process ', options.nEvents, ' from input file, with Phi random=', options.phiRandom)
if options.followMuon:
    options.fastMuon = True
    modules['Veto'].SetFollowMuon()
if options.fastMuon:
    modules['Veto'].SetFastMuon()
run.SetGenerator(primGen)
run.SetStoreTraj(r.kFALSE)
run.Init()

gMC = r.TVirtualMC.GetMC()
fStack = gMC.GetStack()
fStack.SetMinPoints(1)
fStack.SetEnergyCut(-100.*u.MeV)

print('Initialised run.')

fieldMaker = geomGeant4.addVMCFields(ship_geo, '', True)

fieldMaker.plotField(1, r.TVector3(-300.0, 600.0, 10.0), r.TVector3(-300.0, 300.0, 6.0),
                     os.path.join(options.outputDir, 'Bzx.png'))
fieldMaker.plotField(2, r.TVector3(-300.0, 600.0, 10.0), r.TVector3(-400.0, 400.0, 6.0),
                     os.path.join(options.outputDir, 'Bzy.png'))
print('Start run of {} events.'.format(n_events))
run.Run(n_events)
print('Finished simulation of {} events.'.format(n_events))

run.CreateGeometryFile("%s/geofile_full.%s.root" % (options.outputDir, tag))
# save ShipGeo dictionary in geofile
saveBasicParameters.execute("%s/geofile_full.%s.root" % (options.outputDir, tag),ship_geo)

# tmpFile = outFile+"tmp"
# xxx = outFile.split('/')
# check = xxx[len(xxx)-1]
# print(check)
# fin = False
# for ff in r.gROOT.GetListOfFiles():
#     nm = ff.GetName().split('/')
#     print(ff)
#     if nm[len(nm)-1] == check: fin = ff
# if not fin: fin   = r.TFile.Open(outFile)
# t     = fin.cbmsim
# fout  = r.TFile(tmpFile,'recreate')
# sTree = t.CloneTree(0)
# nEvents = 0
# pointContainers = []
# for x in sTree.GetListOfBranches():
#     name = x.GetName()
#     if not name.find('Point')<0: pointContainers.append('sTree.'+name+'.GetEntries()') # makes use of convention that all sensitive detectors fill XXXPoint containers
# for n in range(t.GetEntries()):
#  rc = t.GetEvent(n)
#  empty = True
#  for x in pointContainers:
#     if eval(x)>0: empty = False
#  if not empty:
#     rc = sTree.Fill()
#     nEvents+=1
# sTree.AutoSave()
# fout.Close()
# print("removed empty events, left with:", nEvents)
# rc1 = os.system("rm  "+outFile)
# rc2 = os.system("mv "+tmpFile+" "+outFile)
# fin.SetWritable(False) # bpyass flush error