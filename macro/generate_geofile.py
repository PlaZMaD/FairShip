import sys
import numpy as np
import ROOT as r
from array import array
def generate_magnet_geofile(geofile, magnet_parameters):
 default_magnet_config = np.array([70.0, 170.0, 208.0, 207.0, 281.0, 248.0, 305.0,
 242.0, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0,
 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 54.0, 38.0, 46.0, 192.0, 14.0, 9.0, 10.0,
 31.0, 35.0, 31.0, 51.0, 11.0, 3.0, 32.0, 54.0, 24.0, 8.0, 8.0, 22.0, 32.0,
 209.0, 35.0, 8.0, 13.0, 33.0, 77.0, 85.0, 241.0, 9.0, 26.0])

 fixed_ranges = [(0, 2), (8, 20)]
 mask = [index for interval in fixed_ranges for index in range(*interval)]
 fixed_params_mask = np.zeros(len(default_magnet_config), dtype=bool)
 fixed_params_mask[mask] = True

 full_parameters = np.zeros(len(default_magnet_config))
 full_parameters[fixed_params_mask] = default_magnet_config[fixed_params_mask]
 full_parameters[~fixed_params_mask] = np.array([float(x.strip()) for x in magnet_parameters.split(',')], dtype=float)

 f = r.TFile.Open(geofile, 'recreate')
 parray = r.TVectorD(len(full_parameters), array('d', full_parameters))
 parray.Write('params')
 f.Close()
 print('Geofile constructed at ' + geofile)

if __name__ == '__main__':
 generate_magnet_geofile(sys.argv[1], sys.argv[2])