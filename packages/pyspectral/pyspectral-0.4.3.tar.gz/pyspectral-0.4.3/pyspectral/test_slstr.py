from datetime import datetime

from satpy.scene import Scene
from satpy.utils import debug_on

debug_on()

if __name__ == '__main__':

    scn = Scene(
        sensor='slstr',
        start_time=datetime(2017, 2, 13, 5, 0),
        end_time=datetime(2017, 2, 13, 5, 10),
        base_dir="/data/lang/satellit/polar/sentinel-3/tropicaldisturbance5",
        reader='nc_slstr'
    )

    composite = 'day_microphysics'

    scn.load([composite, 'S2', 10.8])
    scn.show(10.8)

    newscn = scn.resample('moll')
    # newscn.show(10.8)
    newscn.show(composite)
