#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 Adam.Dybbroe

# Author(s):

#   Adam.Dybbroe <adam.dybbroe@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A very basic (example) plotting program to display spectral responses for a
set of satellite instruments for a give wavelength range

"""

import matplotlib.pyplot as plt
from pyspectral.rsr_reader import RelativeSpectralResponse
from pyspectral.utils import get_bandname_from_wavelength
import numpy as np

if __name__ == "__main__":

    # SAT_INSTR = [('NOAA-18', 'avhrr/3'), ('Metop-B', 'avhrr/3'),
    #              ('Suomi-NPP', 'viirs'),
    #              ('Envisat', 'aatsr'), ('Sentinel-3A', 'slstr')]

    SAT_INSTR = [('NOAA-19', 'avhrr/3'), ('Metop-B', 'avhrr/3'),
                 ('NOAA-18', 'avhrr/3'), ('Metop-A', 'avhrr/3'),
                 ('NOAA-17', 'avhrr/3'), ('NOAA-16', 'avhrr/3'),
                 ('NOAA-15', 'avhrr/3'),
                 ('NOAA-14', 'avhrr/2'), ('NOAA-12', 'avhrr/2'),
                 ('NOAA-11', 'avhrr/2'), ('NOAA-9', 'avhrr/2'),
                 ('NOAA-7', 'avhrr/2'), ('NOAA-10', 'avhrr/1'),
                 ('NOAA-8', 'avhrr/1'), ('NOAA-6', 'avhrr/1'),
                 ('TIROS-N', 'avhrr/1'),
                 ]

    import argparse
    parser = argparse.ArgumentParser(
        description='Plot spectral responses for a set of satellite imagers')

    parser.add_argument('req_wvl', metavar='wavelength', type=float,
                        help='the approximate spectral wavelength in micron')

    parser.add_argument("-r", "--range", nargs='*',
                        help="The wavelength range for the plot",
                        default=[None, None], type=float)

    parser.add_argument("-t", "--minimum_response",
                        help=("Minimum response: Any response lower than " +
                              "this will be ignored when plotting"),
                        default=0.015, type=float)

    args = parser.parse_args()
    minimum_response = args.minimum_response
    wvlmin, wvlmax = args.range
    req_wvl = args.req_wvl

    plt.figure(figsize=(10, 5))

    for platform, sensor in SAT_INSTR:
        rsr = RelativeSpectralResponse(platform, sensor)

        band = get_bandname_from_wavelength(req_wvl, rsr.rsr)
        if not band:
            continue

        detectors = rsr.rsr[band].keys()
        # for det in detectors:
        det = detectors[0]
        resp = rsr.rsr[band][det]['response']
        wvl = rsr.rsr[band][det]['wavelength']

        resp = np.ma.masked_less_equal(resp, minimum_response)
        wvl = np.ma.masked_array(wvl, resp.mask)
        resp.compressed()
        wvl.compressed()

        plt.plot(wvl, resp, label='{} - {}'.format(platform, sensor))

    wmin, wmax = plt.xlim()
    wmax = wmax + (wmax - wmin) / 4.0
    if wvlmin:
        wmin = wvlmin
    if wvlmax:
        wmax = wvlmax

    plt.xlim((wmin, wmax))
    plt.title('Relative Spectral Responses')
    plt.legend(loc='lower right')
    plt.savefig('rsr_band_{:>04d}.png'.format(int(100 * req_wvl)))
