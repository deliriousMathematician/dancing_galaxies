# To Do:
#   - Automatically determine vmin and vmax unless specified otherwise
#   - ffmpeg saving animations poorly (start of .mp4 does not play)
#   - Rendering with time and other quantities
#   - Adjust starting zPos
#   - Allow the position of the pText to be changed
#   - Allow custom Fig size to be chosen
#   - ...

# Bug Fixes:
#   - Animation now starts at 0.00 kpc
#   - ...

# Done:
#   - sideOn/faceOn view to be set by user before running function
#   - Much higher resolution thanks to adjustable dpi
#   - Defined both renderer and writer functions to handle animating
#   - ...

# ----------------------------------------------------------------------------------------------------------------------

# An example as to how one would use the dancingGalaxies Package

import pynbody as pyn
from renderers import z_span
from writers import save_ffmpeg

# Loading Simulation
simu = "simFiles/run708main.01000"
h = pyn.load(simu)

# Converting units and aligning face-on
h.physical_units()
pyn.analysis.angmom.faceon(h)

ani = z_span(h.g, qty="rho")

ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "animations/functions.mp4"

save_ffmpeg(ani, ffmpeg_path, write_path)
