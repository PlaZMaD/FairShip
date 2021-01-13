#!/usr/bin/env python
import os
import sys
import getopt
import ROOT
import makeALPACAEvents
# Fix https://root-forum.cern.ch/t/pyroot-hijacks-help/15207 :
ROOT.PyConfig.IgnoreCommandLineOptions = True

import shipunit as u
import shipRoot_conf
import rootUtils as ut
from ShipGeoConfig import ConfigRegistry
from argparse import ArgumentParser

debug = 0  # 1 print weights and field
           # 2 make overlap check
dryrun = False # True: just setup Pythia and exit

DownScaleDiMuon = False

# Default HNL parameters
theHNLMass   = 1.0*u.GeV
theProductionCouplings = theDecayCouplings = None

# Default dark photon parameters
theDPmass    = 0.2*u.GeV

# Alpaca
motherMode = True

mcEngine     = "TGeant4"
simEngine    = "MuonBack"  # "Genie" # Ntuple

inclusive    = "c"    # True = all processes if "c" only ccbar -> HNL, if "b" only bbar -> HNL, if "bc" only Bc+/Bc- -> HNL, and for darkphotons: if meson = production through meson decays, pbrem = proton bremstrahlung, qcd = ffbar -> DP.

MCTracksWithHitsOnly   = False  # copy particles which produced a hit and their history
MCTracksWithEnergyCutOnly = True # copy particles above a certain kin energy cut
MCTracksWithHitsOrEnergyCut = False # or of above, factor 2 file size increase compared to MCTracksWithEnergyCutOnly

charmonly    = False  # option to be set with -A to enable only charm decays, charm x-sec measurement  
HNL          = True

inputFile    = "/eos/experiment/ship/data/Charm/Cascade-parp16-MSTP82-1-MSEL4-978Bpot.root"
defaultInputFile = True

globalDesigns = {'2016':{'dy':10.,'dv':5,'ds':7,'nud':1,'caloDesign':0,'strawDesign':4},\
                 '2018':{'dy':10.,'dv':6,'ds':9,'nud':3,'caloDesign':3,'strawDesign':10}}
default = '2018'

inactivateMuonProcesses = False   # provisionally for making studies of various muon background sources
checking4overlaps = False
if debug>1 : checking4overlaps = True

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("--Ntuple",  dest="ntuple",  help="Use ntuple as input", required=False, action="store_true")
parser.add_argument("--MuonBack",dest="muonback",  help="Generate events from muon background file, --Cosmics=0 for cosmic generator data", required=False, action="store_true")
parser.add_argument("--FollowMuon",dest="followMuon", help="Make muonshield active to follow muons", required=False, action="store_true")
parser.add_argument("--FastMuon",  dest="fastMuon",  help="Only transport muons for a fast muon only background estimate", required=False, action="store_true")
parser.add_argument("--phiRandom", dest="phiRandom",  help="only relevant for muon background generator, random phi", required=False, action="store_true")
parser.add_argument("-n", "--nEvents",dest="nEvents",  help="Number of events to generate", required=False,  default=100, type=int)
parser.add_argument("-i", "--firstEvent",dest="firstEvent",  help="First event of input file to use", required=False,  default=0, type=int)
parser.add_argument("-s", "--seed",dest="theSeed",  help="Seed for random number. Only for experts, see TRrandom::SetSeed documentation", required=False,  default=0, type=int)
parser.add_argument("-S", "--sameSeed",dest="sameSeed",  help="can be set to an integer for the muonBackground simulation with specific seed for each muon, only for experts!"\
                                            ,required=False,  default=False, type=int)
parser.add_argument("--muShieldDesign", dest="ds",  help="5=TP muon shield, 6=magnetized hadron, 7=short magnet design, 9=optimised with T4 as constraint, 8=requires config file\
                                            ,10=with field map for hadron absorber", required=False, default=globalDesigns[default]['ds'], type=int)
group.add_argument("-f",        dest="inputFile",       help="Input file if not default file", required=False, default=False)
parser.add_argument("-g",        dest="geofile",       help="geofile for muon shield geometry, for experts only", required=False, default=None)
parser.add_argument("-o", "--output",dest="outputDir",  help="Output directory", required=False,  default=".")
parser.add_argument("--charm", dest="charm",  help="!=0 create charm detector instead of SHiP", required=False, default=0)
parser.add_argument("--PG",      dest="pg",      help="Use Particle Gun", required=False, action="store_true")
parser.add_argument("--pID",     dest="pID",     help="id of particle used by the gun (default=22)", required=False, default=22, type=int)
parser.add_argument("--factor",     dest="factor", required=False, default=1.0, type=float)
parser.add_argument("--Estart",  dest="Estart",  help="start of energy range of particle gun for muflux detector (default=10 GeV)", required=False, default=10, type=float)
parser.add_argument("--Eend",    dest="Eend",    help="end of energy range of particle gun for muflux detector (default=10 GeV)", required=False, default=10, type=float)
parser.add_argument("--optParams", dest='optParams', required=False, default=False)

options = parser.parse_args()

if options.ntuple:   simEngine = "Ntuple"
if options.muonback: simEngine = "MuonBack"
if options.pg:       simEngine = "PG"
if options.inputFile:
  if options.inputFile == "none": options.inputFile = None
  inputFile = options.inputFile
  defaultInputFile = False





if (simEngine == "Ntuple" or simEngine == "MuonBack") and defaultInputFile :
  print('input file required if simEngine = Ntuple or MuonBack')
  print(" for example -f /eos/experiment/ship/data/Mbias/pythia8_Geant4-withCharm_onlyMuons_4magTarget.root")
  sys.exit()
ROOT.gRandom.SetSeed(options.theSeed)  # this should be propagated via ROOT to Pythia8 and Geant4VMC
shipRoot_conf.configure(0)     # load basic libraries, prepare atexit for python
ship_geo = ConfigRegistry.loadpy("$FAIRSHIP/geometry/geometry_config.py",
                                                muShieldDesign = 9, 
                                                muShieldGeo=options.geofile,
                                                muShieldStepGeo=False, muShieldWithCobaltMagnet=False, optParams=options.optParams)

# Output file name, add dy to be able to setup geometry with ambiguities.
ship_geo.optParams = options.optParams
tag = simEngine+"-"+mcEngine
if not os.path.exists(options.outputDir):
  os.makedirs(options.outputDir)
outFile = "%s/ship.%s.root" % (options.outputDir, tag)

# rm older files !!! 
for x in os.listdir(options.outputDir):
  if not x.find(tag)<0: os.system("rm %s/%s" % (options.outputDir, x) )
# Parameter file name
parFile="%s/ship.params.%s.root" % (options.outputDir, tag)

# In general, the following parts need not be touched
# ========================================================================

# -----Timer--------------------------------------------------------
timer = ROOT.TStopwatch()
timer.Start()
# ------------------------------------------------------------------------
# -----Create simulation run----------------------------------------
run = ROOT.FairRunSim()
run.SetName(mcEngine)  # Transport engine
run.SetOutputFile(outFile)  # Output file
run.SetUserConfig("g4Config.C") # user configuration file default g4Config.C 
rtdb = run.GetRuntimeDb() 
# -----Create geometry----------------------------------------------
# import shipMuShield_only as shipDet_conf # special use case for an attempt to convert active shielding geometry for use with FLUKA
# import shipTarget_only as shipDet_conf

import miniship_conf
modules = miniship_conf.configure(run,ship_geo)
# -----Create PrimaryGenerator--------------------------------------
primGen = ROOT.FairPrimaryGenerator()


if simEngine == "Ntuple":
# reading previously processed muon events, [-50m - 50m]
 ut.checkFileExists(inputFile)
 primGen.SetTarget(ship_geo.target.z0+50*u.m,0.)
 Ntuplegen = ROOT.NtupleGenerator()
 Ntuplegen.Init(inputFile,options.firstEvent)
 primGen.AddGenerator(Ntuplegen)
 options.nEvents = min(options.nEvents,Ntuplegen.GetNevents())
 print('Process ',options.nEvents,' from input file')
#
if simEngine == "PG": 
  myPgun = ROOT.FairBoxGenerator(options.pID, 1)
  myPgun.SetPRange(options.Estart,options.Eend)
  myPgun.SetPhiRange(0, 360) # // Azimuth angle range [degree]
  myPgun.SetXYZ(0.*u.cm, 0.*u.cm, -7200.*u.cm) 
  if options.charm!=0:
     myPgun.SetThetaRange(0,6) # // Pdefault for muon flux
     primGen.SetTarget(ship_geo.target.z0,0.)
  else:  
     myPgun.SetThetaRange(0,0) # // Polar angle in lab system range [degree]
  primGen.AddGenerator(myPgun)

if simEngine == "MuonBack":
# reading muon tracks from previous Pythia8/Geant4 simulation with charm replaced by cascade production 
 fileType = ut.checkFileExists(inputFile)
 if fileType == 'tree':
 # 2018 background production 
  primGen.SetTarget(ship_geo.target.z0+70.845*u.m,0.)
 else:
  primGen.SetTarget(ship_geo.target.z0+50*u.m,0.)
 #
 MuonBackgen = ROOT.MuonBackGenerator()
 # MuonBackgen.FollowAllParticles() # will follow all particles after hadron absorber, not only muons
 MuonBackgen.Init(inputFile,options.firstEvent, options.factor, options.phiRandom)
 if options.charm == 0: MuonBackgen.SetSmearBeam(5 * u.cm) # radius of ring, thickness 8mm
 elif DownScaleDiMuon: 
    if inputFile[0:4] == "/eos": test = os.environ["EOSSHIP"]+inputFile
    else: test = inputFile
    testf = ROOT.TFile.Open(test)
    if not testf.FileHeader.GetTitle().find('diMu100.0')<0:
        MuonBackgen.SetDownScaleDiMuon()   # avoid interference with boosted channels
        print("MuonBackgenerator: set downscale for dimuon on")
    testf.Close()
 if options.sameSeed: MuonBackgen.SetSameSeed(options.sameSeed)
 primGen.AddGenerator(MuonBackgen)
 options.nEvents = min(options.nEvents,MuonBackgen.GetNevents())
 MCTracksWithHitsOnly = True # otherwise, output file becomes too big
 print('Process ',options.nEvents,' from input file, with Phi random=',options.phiRandom, ' with MCTracksWithHitsOnly',MCTracksWithHitsOnly)
 if options.followMuon :  
    options.fastMuon = True
    modules['Veto'].SetFollowMuon()
 if options.fastMuon :    modules['Veto'].SetFastMuon()

run.SetGenerator(primGen)
# ------------------------------------------------------------------------
run.SetStoreTraj(ROOT.kFALSE)
# -----Initialize simulation run------------------------------------
run.Init()
gMC = ROOT.TVirtualMC.GetMC()
fStack = gMC.GetStack()
if MCTracksWithHitsOnly:
 fStack.SetMinPoints(1)
 fStack.SetEnergyCut(-100.*u.MeV)
elif MCTracksWithEnergyCutOnly:
 fStack.SetMinPoints(-1)
 fStack.SetEnergyCut(100.*u.MeV)
elif MCTracksWithHitsOrEnergyCut: 
 fStack.SetMinPoints(1)
 fStack.SetEnergyCut(100.*u.MeV)
elif options.deepCopy: 
 fStack.SetMinPoints(0)
 fStack.SetEnergyCut(0.*u.MeV)

# if options.eventDisplay:
#  # Set cuts for storing the trajectories, can only be done after initialization of run (?!)
#   trajFilter = ROOT.FairTrajFilter.Instance()
#   trajFilter.SetStepSizeCut(1*u.mm);  
#   trajFilter.SetVertexCut(-20*u.m, -20*u.m,ship_geo.target.z0-1*u.m, 20*u.m, 20*u.m, 200.*u.m)
#   trajFilter.SetMomentumCutP(0.1*u.GeV)
#   trajFilter.SetEnergyCut(0., 400.*u.GeV)
#   trajFilter.SetStorePrimaries(ROOT.kTRUE)
#   trajFilter.SetStoreSecondaries(ROOT.kTRUE)

# The VMC sets the fields using the "/mcDet/setIsLocalMagField true" option in "gconfig/g4config.in"
import geomGeant4
# geomGeant4.setMagnetField() # replaced by VMC, only has effect if /mcDet/setIsLocalMagField  false

# Define extra VMC B fields not already set by the geometry definitions, e.g. a global field,
# any field maps, or defining if any volumes feel only the local or local+global field.
# For now, just keep the fields already defined by the C++ code, i.e comment out the fieldMaker
if options.charm == 0:   # charm and muflux testbeam not yet updated for using the new bfield interface
 if hasattr(ship_geo.Bfield,"fieldMap"):
  fieldMaker = geomGeant4.addVMCFields(ship_geo, '', True)

# Print VMC fields and associated geometry objects
if debug > 0:
 geomGeant4.printVMCFields()
 geomGeant4.printWeightsandFields(onlyWithField = True,\
             exclude=['DecayVolume','Tr1','Tr2','Tr3','Tr4','Veto','Ecal','Hcal','MuonDetector','SplitCal'])
# Plot the field example
fieldMaker.plotField(1, ROOT.TVector3(-9000.0, -3000.0, 10.0), ROOT.TVector3(-300.0, 300.0, 6.0), 'Bzx.png')
fieldMaker.plotField(2, ROOT.TVector3(-9000.0, -3000.0, 10.0), ROOT.TVector3(-400.0, 400.0, 6.0), 'Bzy.png')

if inactivateMuonProcesses :
 ROOT.gROOT.ProcessLine('#include "Geant4/G4ProcessTable.hh"')
 mygMC = ROOT.TGeant4.GetMC()
 mygMC.ProcessGeantCommand("/process/inactivate muPairProd")
 mygMC.ProcessGeantCommand("/process/inactivate muBrems")
 mygMC.ProcessGeantCommand("/process/inactivate muIoni")
 mygMC.ProcessGeantCommand("/process/inactivate muonNuclear")
 mygMC.ProcessGeantCommand("/particle/select mu+")
 mygMC.ProcessGeantCommand("/particle/process/dump")
 gProcessTable = ROOT.G4ProcessTable.GetProcessTable()
 procmu = gProcessTable.FindProcess(ROOT.G4String('muIoni'),ROOT.G4String('mu+'))
 procmu.SetVerboseLevel(2)
# -----Start run----------------------------------------------------
run.Run(options.nEvents)
# -----Runtime database---------------------------------------------
kParameterMerged = ROOT.kTRUE
# parOut = ROOT.FairParRootFileIo(kParameterMerged)
# parOut.open(parFile)
# rtdb.setOutput(parOut)
# rtdb.saveOutput()
# rtdb.printParamContexts()
# getattr(rtdb,"print")()
# ------------------------------------------------------------------------
run.CreateGeometryFile("%s/geofile_full.%s.root" % (options.outputDir, tag))
# save ShipGeo dictionary in geofile
import saveBasicParameters
saveBasicParameters.execute("%s/geofile_full.%s.root" % (options.outputDir, tag),ship_geo)

# checking for overlaps
lGeo = ROOT.gGeoManager
miniShield = sGeo.GetVolume('MiniShieldArea')
nodes = miniShield.GetNodes()
m = 0.
for node in nodes:
  volume = node.GetVolume()
  if 'mini' in volume.GetName():
    m += volume.Weight(0.01, 'a')

if checking4overlaps:
 fGeo = ROOT.gGeoManager
 fGeo.SetNmeshPoints(10000)
 fGeo.CheckOverlaps(0.1)  # 1 micron takes 5minutes
 fGeo.PrintOverlaps()
 # check subsystems in more detail
 for x in fGeo.GetTopNode().GetNodes(): 
   x.CheckOverlaps(0.0001)
   fGeo.PrintOverlaps()
# -----Finish-------------------------------------------------------
timer.Stop()
rtime = timer.RealTime()
ctime = timer.CpuTime()
print(' ') 
print("Macro finished succesfully.") 
if "P8gen" in globals() : 
    if (HNL): print("number of retries, events without HNL ",P8gen.nrOfRetries())
    elif (options.DarkPhoton): 
        print("number of retries, events without Dark Photons ",P8gen.nrOfRetries())
        print("total number of dark photons (including multiple meson decays per single collision) ",P8gen.nrOfDP())

print("Output file is ",  outFile) 
print("Parameter file is ",parFile)
print("Real time ",rtime, " s, CPU time ",ctime,"s")

# remove empty events
if simEngine == "MuonBack":
 tmpFile = outFile+"tmp"
 xxx = outFile.split('/')
 check = xxx[len(xxx)-1]
 fin = False
 for ff in ROOT.gROOT.GetListOfFiles():
    nm = ff.GetName().split('/')
    if nm[len(nm)-1] == check: fin = ff
 if not fin: fin   = ROOT.TFile.Open(outFile)
 t     = fin.cbmsim
 fout  = ROOT.TFile(tmpFile,'recreate')
 sTree = t.CloneTree(0)
 nEvents = 0
 pointContainers = []
 for x in sTree.GetListOfBranches():
   name = x.GetName() 
   if not name.find('Point')<0: pointContainers.append('sTree.'+name+'.GetEntries()') # makes use of convention that all sensitive detectors fill XXXPoint containers
 for n in range(t.GetEntries()):
     rc = t.GetEvent(n)
     empty = True 
     for x in pointContainers:
        if eval(x)>0: empty = False
     if not empty:
        rc = sTree.Fill()
        nEvents+=1
 sTree.AutoSave()
 fout.Close()
 print("removed empty events, left with:", nEvents)
 rc1 = os.system("rm  "+outFile)
 rc2 = os.system("mv "+tmpFile+" "+outFile)
 fin.SetWritable(False) # bpyass flush error

 def check_acceptance(hit, bound=(330, 530)):
    """
    :param hit:
    :param bound: acceptance bounds (X,Y) in cm
    :return:
    """
    return abs(hit.GetX()) <= bound[0] and abs(hit.GetY()) <= bound[1]

 def process_file(filename,  muons_output_name = "muons_output", epsilon=1e-9, debug=True,
                 apply_acceptance_cut=False):
    directory = os.path.dirname(os.path.abspath(filename))
    file = ROOT.TFile(filename)

    tree = file.Get("cbmsim")
    print("Total events:{}".format(tree.GetEntries()))

    MUON = 13
    muons_stats = []
    events_with_more_than_two_hits_per_mc = 0
    empty_hits = "Not implemented"

    for index, event in enumerate(tree):
        if index % 5000 == 0:
            print("N events processed: {}".format(index))
        mc_pdgs = []

        for hit in event.MCTrack:
            mc_pdgs.append(hit.GetPdgCode())

        muon_veto_points = defaultdict(list)
        for hit in event.fluxDetPoint:
            if hit.GetTrackID() >= 0 and\
               abs(mc_pdgs[hit.GetTrackID()]):
                if apply_acceptance_cut:
                    if check_acceptance(hit):
                        # Middle or inital stats??
                        pos_begin = ROOT.TVector3()
                        hit.Position(pos_begin)
                        # Extracting only XY coordinates
                        muon_veto_points[hit.GetTrackID()].append([pos_begin.X(), pos_begin.Y()])
                else:
                    pos_begin = ROOT.TVector3()
                    hit.Position(pos_begin)
                    # Extracting only XY coordinates
                    muon_veto_points[hit.GetTrackID()].append([pos_begin.X(), pos_begin.Y()])

        for index, hit in enumerate(event.MCTrack):
            if index in muon_veto_points:
                if debug:
                    print("PDG: {}, mID: {}".format(hit.GetPdgCode(), hit.GetMotherId()))
                    assert abs(hit.GetPdgCode()) == MUON
                muon = [
                    hit.GetPx(),
                    hit.GetPy(),
                    hit.GetPz(),
                    hit.GetStartX(),
                    hit.GetStartY(),
                    hit.GetStartZ(),
                    hit.GetPdgCode(),
                    hit.GetWeight()
                ]
                muons_stats.append(muon + muon_veto_points[index][0])
                if len(muon_veto_points[index]) > 1:
                    events_with_more_than_two_hits_per_mc += 1
                    continue

    print("events_with_more_than_two_hits_per_mc: {}".format(events_with_more_than_two_hits_per_mc))
    print("Stopped muons: {}".format(empty_hits))
    print("Total events returned: {}".format(len(muons_stats)))
    return np.array(muons_stats)
 muons_stats = process_file(os.path.join(options.outputDir,"ship.MuonBack-TGeant4.root"), apply_acceptance_cut=True, debug=False)
 if len(muons_stats) == 0:
        veto_points, muon_kinematics = np.array([]), np.array([])
    else:
        veto_points = muons_stats[:, -2:]
        muon_kinematics = muons_stats[:, :-2]
 returned_params = {
        "w": m,
        "params": [float(strip(par))for par in options.optParams.split(',')],
        "kinematics": muon_kinematics.tolist()
    }
 with open(os.path.join(options.outputDir, "optimise_input.json"), "w") as f:
        json.dump(returned_params, f)
# ------------------------------------------------------------------------
import checkMagFields
def visualizeMagFields():
 checkMagFields.run()
def checkOverlapsWithGeant4():
 # after /run/initialize, but prints warning messages, problems with TGeo volume
 mygMC = ROOT.TGeant4.GetMC()
 mygMC.ProcessGeantCommand("/geometry/test/recursion_start 0")
 mygMC.ProcessGeantCommand("/geometry/test/recursion_depth 2")
 mygMC.ProcessGeantCommand("/geometry/test/run")
