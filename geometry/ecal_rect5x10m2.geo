# Total thickness of absorber is 25 X_0. (No preshower)
# 140 layers of lead and scintillator.
# Thickness of lead tiles: 1 mm
# Thickness of scintillator tiles: 2 mm.
# Modules with 4 readout channels are used.
# Total number of modules: 3696. Channels: 14784
# By //Dr.Sys 2016.05.31
XPos=0		#Position of ECal center	[cm]
YPos=0		#Position of ECal center	[cm]
ZPos=3540	#Position of ECal start		[cm]
NLayers=140	#Number of layers		
ModuleSize=12.0	#Module size			[cm]
Lead=.1		#Absorber thickness in layer	[cm]
Scin=.2		#Scintillator thickness in layer[cm]
Tyveec=.006	#Tyveec thickness in layer	[cm]
HoleRadius=.075 #Radius of hole in the calorimeter		[cm]
FiberRadius=.06 #Radius of fiber				[cm]
Steel=0.01	#Thickness of steel tapes			[cm]
TileEdging=0.01	#Thickness of white coating near tiles edges 	[cm]
XSemiAxis=212	#X semiaxis of keeping volume	[cm]
YSemiAxis=318	#Y semiaxis of keeping volume	[cm]
CF[1]=1		#Is there clear fiber in cell type 1
CF[2]=1		#Is there clear fiber in cell type 2
CF[3]=1		#Is there clear fiber in cell type 3
CF[4]=1		#Is there clear fiber in cell type 4
NH[1]=12	#Number of holes for cell type 1
NH[2]=6		#Number of holes for cell type 2
NH[3]=4		#Number of holes for cell type 3
NH[4]=4		#Number of holes for cell type 4
LightMap[1]=none # Light collection
LightMap[2]=none # efficiency maps for
LightMap[3]=none # efficiency maps for
LightMap[4]=none # different modules
# Be as compatible to CbmEcal in physics as possible 
usesimplegeo=1	#Use simplified geometry
EcalZSize=50.0	#Z size of ECAL container	[cm]
ECut=100e-6	#Geant cuts CUTGAM CUTELE BCUTE BCUTM DCUTE [GeV]
HCut=300e-6	#Geant cuts CUTNEU CUTHAD CUTMUO DCUTM PPCUTM [GeV]
FastMC=0	#0 for full MC (with showers in ECAL), 1 for fast MC (only hits at sensitive plane before ECAL)
absorber=Lead   #Material of the absorber
structure
#Zero for no module here. ECALs with rectangular hole only can be constructed.
#Number means number of divisions of ECAL module in both directions: vertical and horizontal.
#So 2 states for module with 4 cells in it.
#         1         2         3         4    
#12345678901234567890123456789012345678901234
22222222222222222222222222222222222222222222 # 0
22222222222222222222222222222222222222222222 # 1
22222222222222222222222222222222222222222222 # 2
22222222222222222222222222222222222222222222 # 3
22222222222222222222222222222222222222222222 # 4
22222222222222222222222222222222222222222222 # 5
22222222222222222222222222222222222222222222 # 6
22222222222222222222222222222222222222222222 # 7
22222222222222222222222222222222222222222222 # 8
22222222222222222222222222222222222222222222 # 9
22222222222222222222222222222222222222222222 #10
22222222222222222222222222222222222222222222 #11
22222222222222222222222222222222222222222222 #12
22222222222222222222222222222222222222222222 #13
22222222222222222222222222222222222222222222 #14
22222222222222222222222222222222222222222222 #15
22222222222222222222222222222222222222222222 #16
22222222222222222222222222222222222222222222 #17
22222222222222222222222222222222222222222222 #18
22222222222222222222222222222222222222222222 #19
22222222222222222222222222222222222222222222 #20
22222222222222222222222222222222222222222222 #21
22222222222222222222222222222222222222222222 #22
22222222222222222222222222222222222222222222 #23
22222222222222222222222222222222222222222222 #24
22222222222222222222222222222222222222222222 #25
22222222222222222222222222222222222222222222 #26
22222222222222222222222222222222222222222222 #27
22222222222222222222222222222222222222222222 #28
22222222222222222222222222222222222222222222 #29
22222222222222222222222222222222222222222222 #30
22222222222222222222222222222222222222222222 #31
22222222222222222222222222222222222222222222 #32
22222222222222222222222222222222222222222222 #33
22222222222222222222222222222222222222222222 #34
22222222222222222222222222222222222222222222 #35
22222222222222222222222222222222222222222222 #36
22222222222222222222222222222222222222222222 #37
22222222222222222222222222222222222222222222 #38
22222222222222222222222222222222222222222222 #39
22222222222222222222222222222222222222222222 #40
22222222222222222222222222222222222222222222 #41
22222222222222222222222222222222222222222222 #42
22222222222222222222222222222222222222222222 #43
22222222222222222222222222222222222222222222 #44
22222222222222222222222222222222222222222222 #45
22222222222222222222222222222222222222222222 #46
22222222222222222222222222222222222222222222 #47
22222222222222222222222222222222222222222222 #48
22222222222222222222222222222222222222222222 #49
22222222222222222222222222222222222222222222 #50
22222222222222222222222222222222222222222222 #51
22222222222222222222222222222222222222222222 #52
22222222222222222222222222222222222222222222 #53
22222222222222222222222222222222222222222222 #54
22222222222222222222222222222222222222222222 #55
22222222222222222222222222222222222222222222 #56
22222222222222222222222222222222222222222222 #57
22222222222222222222222222222222222222222222 #58
22222222222222222222222222222222222222222222 #59
22222222222222222222222222222222222222222222 #60
22222222222222222222222222222222222222222222 #61
22222222222222222222222222222222222222222222 #62
22222222222222222222222222222222222222222222 #63
22222222222222222222222222222222222222222222 #64
22222222222222222222222222222222222222222222 #65
22222222222222222222222222222222222222222222 #66
22222222222222222222222222222222222222222222 #67
22222222222222222222222222222222222222222222 #68
22222222222222222222222222222222222222222222 #69
22222222222222222222222222222222222222222222 #70
22222222222222222222222222222222222222222222 #71
22222222222222222222222222222222222222222222 #72
22222222222222222222222222222222222222222222 #73
22222222222222222222222222222222222222222222 #74
22222222222222222222222222222222222222222222 #75
22222222222222222222222222222222222222222222 #76
22222222222222222222222222222222222222222222 #77
22222222222222222222222222222222222222222222 #78
22222222222222222222222222222222222222222222 #79
22222222222222222222222222222222222222222222 #80
22222222222222222222222222222222222222222222 #81
22222222222222222222222222222222222222222222 #82
22222222222222222222222222222222222222222222 #83

