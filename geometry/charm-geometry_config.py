import shipunit as u
from ShipGeoConfig import AttrDict, ConfigRegistry
import ROOT
# the following params should be passed through 'ConfigRegistry.loadpy' method
# none for the moment
with ConfigRegistry.register_config("basic") as c:

    # c.Bfield = AttrDict(z=0 * u.cm)
    # c.Bfield.max = 0 # 1.4361*u.kilogauss  # was 1.15 in EOI
    # c.Bfield.y   = 0.
    # c.Bfield.x   = 0.

    c.MufluxSpectrometer = AttrDict(z = 0*u.cm)  
    # False = charm cross-section; True = muon flux measurement 
    
    if "targetOpt" not in globals():
       targetOpt = 18 # add extra 20cm of tungsten as per 13/06/2017

    if "Setup" not in globals(): #muon flux or charm xsec measurement
      Setup = 0    

    if "cTarget" not in globals():
      cTarget = 3

    if Setup == 0: 
     c.MufluxSpectrometer.muflux = True
    else: 
     c.MufluxSpectrometer.muflux = False

    if "muShieldStepGeo" not in globals():
        muShieldStepGeo = False
    if "muShieldWithCobaltMagnet" not in globals():
        muShieldWithCobaltMagnet = 0
    if "muShieldDesign" not in globals():
        muShieldDesign = 5
    if "muShieldGeo" not in globals():
        muShieldGeo = None

    c.target = AttrDict(z0=0*u.cm)
     
    c.MufluxTargetStation=AttrDict(z0=0* u.cm)
    c.MufluxTargetStation.absorber_x=120 *u.cm
    c.MufluxTargetStation.absorber_y=97.5*u.cm
    c.MufluxTargetStation.absorbercutout_x=102* u.cm
    c.MufluxTargetStation.absorbercutout_y=27.5*u.cm
    c.MufluxTargetStation.ironshield_x=20.*u.cm
    c.MufluxTargetStation.ironshield_y=82.5*u.cm
    c.MufluxTargetStation.ironshield_z=160*u.cm
    c.MufluxTargetStation.concreteshield_x=40*u.cm
    c.MufluxTargetStation.concreteshield_y=82.5*u.cm
    c.MufluxTargetStation.concreteshield_z=160.*u.cm
    c.MufluxTargetStation.abovetargetshield_x=120*u.cm
    c.MufluxTargetStation.abovetargetshield_y=42.5*u.cm
    c.MufluxTargetStation.abovetargetshield_z=160*u.cm
    c.MufluxTargetStation.aboveabsorbershield_x=120*u.cm
    c.MufluxTargetStation.aboveabsorbershield_y=40*u.cm
    c.MufluxTargetStation.aboveabsorbershield_z=80*u.cm
    c.MufluxTargetStation.aboveabovetargetshield_y=40*u.cm
    c.MufluxTargetStation.floor_x=500.*u.cm
    c.MufluxTargetStation.floor_y=80.*u.cm
    c.MufluxTargetStation.floor_z=800.*u.cm

    # target absorber muon shield setup, decayVolume.length = nominal EOI length, only kept to define z=0
    c.decayVolume            =  AttrDict(z=0*u.cm)
    c.decayVolume.length     =   50*u.m

    c.hadronAbsorber              =  AttrDict(z=0*u.cm)
    c.hadronAbsorber.length =  2.4*u.m    
    
    c.hadronAbsorber.z     =   - c.hadronAbsorber.length/2.

    c.target               =  AttrDict(z=0*u.cm)
    c.targetOpt            = targetOpt

    c.target.M1 = "molybdenummisis"
    c.target.L1 = 8.52*u.cm
    c.target.M2 = "molybdenummisis"
    c.target.L2 = 2.8*u.cm
    c.target.M3 = "molybdenummisis"
    c.target.L3 = 2.8*u.cm
    c.target.M4 = "molybdenummisis"
    c.target.L4 = 2.8*u.cm
    c.target.M5 = "molybdenummisis"
    c.target.L5 = 2.8*u.cm
    c.target.M6 = "molybdenummisis"
    c.target.L6 = 2.8*u.cm
    c.target.M7 = "molybdenummisis"
    c.target.L7 = 2.8*u.cm
    c.target.M8 = "molybdenummisis"
    c.target.L8 = 2.8*u.cm
    c.target.M9 = "molybdenummisis"
    c.target.L9 = 5.4*u.cm
    c.target.M10 = "molybdenummisis"
    c.target.L10 = 5.4*u.cm
    c.target.M11 = "molybdenummisis"
    c.target.L11 = 6.96*u.cm
    c.target.M12 = "molybdenummisis"
    c.target.L12 = 8.52*u.cm
    c.target.M13 = "molybdenummisis"
    c.target.L13 = 8.52*u.cm
    c.target.M14 = "tungstenmisis"
    c.target.L14 = 5.17*u.cm
    c.target.M15 = "tungstenmisis"
    c.target.L15 = 8.3*u.cm
    c.target.M16 = "tungstenmisis"
    c.target.L16 = 10.39*u.cm
    c.target.M17 = "tungstenmisis"
    c.target.L17 = 20.82*u.cm
    c.target.M18 = "tungstenmisis"
    c.target.L18 = 36.47*u.cm
    c.target.sl  =  0.54459*u.cm  # H20 slit *17 times; to get to the measured length by survey 
    c.target.xy  = 10.*u.cm   # new diameter of muflux target    
    
    # 5.0 cm is for front and endcaps
    
    c.target.length = 154.328*u.cm   #from survey 
    # interaction point, start of target
    
    c.target.z   =  c.hadronAbsorber.z - c.hadronAbsorber.length/2. - c.target.length/2.
    c.target.z0  =  c.target.z - c.target.length/2.

    #### MUON SHIELD
    c.muShield = AttrDict(z=0 * u.cm)
    c.muShieldDesign = muShieldDesign
    c.muShield.Field = 1.8  # in units of Tesla expected by ShipMuonShield
    # design 4,5,6
    c.muShield.LE = 0 * u.m  # - 0.5 m air - Goliath: 4.5 m - 0.5 m air - nu-tau mu-det: 3 m - 0.5 m air. finally 10m asked by Giovanni
    c.muShield.dZ0 = 2.5 * u.m if muShieldDesign == 6 else 1 * u.m
    c.muShield.dZ1 = 3.5 * u.m
    c.muShield.dZ2 = 6. * u.m
    c.muShield.dZ3 = 2.5 * u.m
    c.muShield.dZ4 = 3. * u.m
    c.muShield.dZ5 = 0. * u.m  # 28Oct #5 removed
    c.muShield.dZ6 = 3. * u.m
    c.muShield.dZ7 = 3. * u.m
    c.muShield.dZ8 = 3. * u.m
    c.muShield.dXgap = 0.2 * u.m
    c.muShield.dZgap = 0.01 * u.m

    c.muShieldStepGeo = muShieldStepGeo
    c.muShieldWithCobaltMagnet = muShieldWithCobaltMagnet

    # zGap to compensate automatic shortening of magnets
    zGap = 0.5 * c.muShield.dZgap  # halflengh of gap
    if muShieldDesign == 7:
        c.muShield.dZ1 = 0.7 * u.m + zGap
        c.muShield.dZ2 = 1.7 * u.m + zGap
        c.muShield.dZ3 = 2.0 * u.m + zGap
        c.muShield.dZ4 = 2.0 * u.m + zGap
        c.muShield.dZ5 = 2.75 * u.m + zGap
        c.muShield.dZ6 = 2.4 * u.m + zGap
        c.muShield.dZ7 = 3.0 * u.m + zGap
        c.muShield.dZ8 = 2.35 * u.m + zGap
        c.muShield.dXgap = 0. * u.m
    elif muShieldDesign == 9:
        c.muShield.Field = 1.7  # Tesla
        c.muShield.dZ1 = 0. * u.m # + zGap
        c.muShield.dZ2 = 0. * u.m # + zGap
        c.muShield.dZ3 = 2.08 * u.m + zGap
        c.muShield.dZ4 = 2.07 * u.m + zGap
        c.muShield.dZ5 = 2.81 * u.m + zGap
        c.muShield.dZ6 = 2.48 * u.m + zGap
        c.muShield.dZ7 = 3.05 * u.m + zGap
        c.muShield.dZ8 = 2.42 * u.m + zGap
        c.muShield.dXgap = 0. * u.m
        c.muShield.half_X_max = 179 * u.cm
        c.muShield.half_Y_max = 317 * u.cm
    elif muShieldDesign == 8:
        assert muShieldGeo
        c.muShieldGeo = muShieldGeo
        print("Load geo")
        f = ROOT.TFile.Open(muShieldGeo)
        params = ROOT.TVectorD()
        params.Read('params')
        f.Close()
        c.muShield.dZ1 = 0. * u.m #+ zGap
        c.muShield.dZ2 = 0. * u.m #+ zGap
        c.muShield.dZ3 = params[2]
        c.muShield.dZ4 = params[3]
        c.muShield.dZ5 = params[4]
        c.muShield.dZ6 = params[5]
        c.muShield.dZ7 = params[6]
        c.muShield.dZ8 = params[7]
        c.muShield.dXgap = 0. * u.m

        offset = 7
        c.muShield.half_X_max = 0
        c.muShield.half_Y_max = 0
        for index in range(2, 8):
            f_l = params[offset + index * 6 + 1]
            f_r = params[offset + index * 6 + 2]
            h_l = params[offset + index * 6 + 3]
            h_r = params[offset + index * 6 + 4]
            g_l = params[offset + index * 6 + 5]
            g_r = params[offset + index * 6 + 6]
            c.muShield.half_X_max = max(c.muShield.half_X_max, 2 * f_l + g_l, 2 * f_r + g_r)
            c.muShield.half_Y_max = max(c.muShield.half_Y_max, h_l + f_l, h_r + f_r)
        c.muShield.half_X_max += 15 * u.cm
        c.muShield.half_Y_max += 15 * u.cm

    if muShieldDesign in range(7, 10):
        c.muShield.length = 2 * (
                c.muShield.dZ1 + c.muShield.dZ2 +
                c.muShield.dZ3 + c.muShield.dZ4 +
                c.muShield.dZ5 + c.muShield.dZ6 +
                c.muShield.dZ7 + c.muShield.dZ8
        ) + c.muShield.LE
        c.muShield.z = c.hadronAbsorber.z + c.hadronAbsorber.length / 2 + c.muShield.length / 2 + 0 * u.m
        c.SensPlane = AttrDict(z=0 * u.cm)
        c.SensPlane.z = c.muShield.z + c.muShield.length / 2 + 0.5 * u.m

    c.hadronAbsorber.WithConstField = True
    c.muShield.WithConstField = True

    # Unused parameters to be able to run shield constructor
    c.cave = AttrDict(z=0 * u.cm)
    c.cave.floorHeightMuonShield = 0 * u.m
    c.Yheight = 0 * u.m




