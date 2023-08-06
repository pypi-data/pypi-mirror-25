# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from bruker_opus_filereader import OpusReader
from ifg_spectrum_data import Interferogram

sample = OpusReader('..\\data\\a6040_MIR_alignment.0')
sample.readDataBlocks()

lwn = sample['Instrument']['LWN']
lambda_laser = 1 / lwn / 100 * 1E+9

dx = 1 / 2 / lwn
y = sample['IgSm']

ifg = Interferogram(y, dx)
ifg.roll()

spectrum = ifg.spectrum()

plt.close('all')
plt.subplot(2,1,1)
ifg.plot()
plt.subplot(2,1,2)
spectrum.plot('complex')
plt.xlim((6000, 0))
plt.ylim((-2.5, 5))
plt.xlabel('wavenumber [cm$^{-1}$]')