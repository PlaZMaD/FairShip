import shipunit as u
from ShipGeoConfig import AttrDict, ConfigRegistry
import ROOT
# the following params should be passed through 'ConfigRegistry.loadpy' method
# none for the moment
with ConfigRegistry.register_config("basic") as c:
    c.optParams = ""

    if "muShieldStepGeo" not in globals():
        muShieldStepGeo = False
    if "muShieldWithCobaltMagnet" not in globals():
        muShieldWithCobaltMagnet = 0
    if "muShieldDesign" not in globals():
        muShieldDesign = 20
    if "muShieldGeo" not in globals():
        muShieldGeo = None


    # target absorber muon shield setup, decayVolume.length = nominal EOI length, only kept to define z=0
    c.decayVolume            =  AttrDict(z=0*u.cm)
    c.decayVolume.length     =   50*u.m

    c.Beam = AttrDict(z=-250 * u.cm)

    c.Goliath = AttrDict(z=0 * u.cm)
    # Spectrometer
    # Parameters for Goliath by Annarita
    c.Goliath.LS = 4.5 * u.m
    c.Goliath.TS = 3.6 * u.m
    # c.Spectrometer.CoilR = 1.*u.m
    c.Goliath.CoilR = 1.6458 * u.m
    c.Goliath.UpCoilH = 45 * u.cm
    c.Goliath.LowCoilH = 30 * u.cm
    # c.Spectrometer.CoilD = 105*u.cm
    c.Goliath.CoilD = 103.5575 * u.cm
    # c.Spectrometer.BasisH = 57*u.cm
    c.Goliath.BasisH = 50.22125 * u.cm
    c.Goliath.H = 2 * c.Goliath.BasisH + c.Goliath.CoilD + c.Goliath.UpCoilH + c.Goliath.LowCoilH

    # c.Spectrometer.DX = 2. * u.m
    # c.Spectrometer.DY = 1.6 * u.m
    # c.Spectrometer.DZ = 16. * u.cm


    c.Goliath.goliathcentre_to_beam = 17.32*u.cm + (c.Goliath.UpCoilH-c.Goliath.LowCoilH)/2.
    c.Goliath.goliathcentre = 0*u.cm #351.19*u.cm


    # c.MufluxSpectrometer.DX = 2.*u.m
    # c.MufluxSpectrometer.DY = 1.6*u.m
    # c.MufluxSpectrometer.DZ = 11.72*u.cm

    #### MUON SHIELD
    c.muShield = AttrDict(z=0 * u.cm)
    c.muShieldDesign = muShieldDesign
    c.muShield.LE = 0 * u.m  # - 0.5 m air - Goliath: 4.5 m - 0.5 m air - nu-tau mu-det: 3 m - 0.5 m air. finally 10m asked by Giovanni
    c.muShield.dZ0 = 1 * u.m
    c.muShield.dZgap = 0.01 * u.m

    c.muShieldStepGeo = muShieldStepGeo
    c.muShieldWithCobaltMagnet = muShieldWithCobaltMagnet

    # zGap to compensate automatic shortening of magnets
    zGap = 0.5 * c.muShield.dZgap  # halflengh of gap
    if muShieldDesign == 9:
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
        
    elif muShieldDesign == 20:
        c.muShield.Gap = 0.05*u.m
        c.muShield.Field = 1.7  # Tesla
        c.muShield.Start_Z = 3. * u.m # + zGap
        c.muShield.Z = 0.25 * u.m
        c.muShield.H1 = 1.5 * u.m
        c.muShield.length =  2*(c.muShield.Z * 4  + c.muShield.Gap * 3)


    if muShieldDesign in range(7, 10):
        c.muShield.length = 2 * (
                c.muShield.dZ1 + c.muShield.dZ2 +
                c.muShield.dZ3 + c.muShield.dZ4 +
                c.muShield.dZ5 + c.muShield.dZ6 +
                c.muShield.dZ7 + c.muShield.dZ8
        ) + c.muShield.LE


    c.SensPlane = AttrDict(z=0 * u.cm)
    c.SensPlane.z_1 = c.Goliath.goliathcentre - c.Goliath.LS / 2 - 10 * u.cm
    c.SensPlane.z_2 = c.Goliath.goliathcentre + c.Goliath.LS / 2 + 10 * u.cm

    c.muShield.z = c.SensPlane.z_2 + 1*u.m + c.muShield.length / 2
    c.SensPlane.z_3 = c.muShield.z + 1*u.m + c.muShield.length / 2


    c.hadronAbsorber = AttrDict(z=0 * u.cm)
    c.hadronAbsorber.WithConstField = True
    c.muShield.WithConstField = True

    # Unused parameters to be able to run shield constructor
    c.cave = AttrDict(z=0 * u.cm)
    c.cave.floorHeightMuonShield = 0 * u.m
    c.Yheight = 0 * u.m



