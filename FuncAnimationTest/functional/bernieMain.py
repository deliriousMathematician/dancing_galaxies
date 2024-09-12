# Imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import os

# Variables
vmin = 10 ** 5  # Colormap minimum
vmax = 10 ** 10  # Colormap maximum
z_shift = 0.01  # Distance (kpc) to be shifted per frame [avoid values <= 0.001]
z_max = 0.25  # Maximum z-distance to cover in the animation (kpc)
interval = 250  # Time (ms) between frames
z = 0
width = 16  # x and y plot range
cmap = plt.cm.turbo # colormap

# Calculating the number of frames dynamically
frames = int(z_max / z_shift)

# Loading Simulation
# sim = input("Enter Simulation Path: ")  # User input
sim = "simFiles/run708main.01000"
try:
    h = pyn.load(sim)
except FileNotFoundError:
    raise FileNotFoundError("Simulation file not found. Check your file path.")

# Converting units and aligning face-on
h.physical_units()
pyn.analysis.angmom.faceon(h)

# Creating Figure and Axes
fig, ax = plt.subplots()

# Starting Plot
galaxy = pyn.plot.sph.image(h.g, width=width, qty='rho', vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

# Customizing Plot
cBar = fig.colorbar(galaxy, ax=ax, label="cbar")
title = ax.set_title("test")
xLabel = ax.set_xlabel("x/kpc")
yLabel = ax.set_ylabel("y/kpc")
xLim = ax.set_xlim(-1 * width/2, width/2)
yLim = ax.set_ylim(-1 * width/2, width/2)

# Plot Text
pText = fig.text(0.75, 0.05, f'z = {z:.2f} kpc', transform=ax.transAxes)

# Animation Functions


def shift_z(height):

    """Shift the galaxy slice in the z direction."""

    h.g['pos'][:, 2] -= height
    return None


def update(frame):

    """Update the animation for each frame."""

    global galaxy, z, width, vmin, vmax, cmap

    # Shift particles
    shift_z(z_shift)
    z += z_shift

    # Update plot
    galaxy.remove()  # Clear the imshow artist to avoid overlapping images
    galaxy = pyn.plot.sph.image(h.g, width=width, qty='rho', vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

    # Updating the height text
    pText.set_text(f'z = {z:.2f} kpc')

    return galaxy


# Initializing the animation
ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, repeat=False)

# Writing to disk using ffmpeg
# ffmpeg_path = input("Enter the ffmpeg file path: ") # User input
ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError("FFmpeg not found. Check your ffmpeg installation path.")

matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path  # Set path as source
writer = animation.FFMpegWriter(fps=5, bitrate=-1)  # -1 for automatic best bitrate
ani.save('animations/bernie.mp4', writer=writer)

# Cleanup and closing plot to free memory
plt.close(fig)
