# imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ----------------------------------------------------------------------------------------------------------------------
# user data [REMOVE]
# Loading Simulation
simu = "simFiles/run708main.01000"
h = pyn.load(simu)

# Converting units and aligning face-on
h.physical_units()
pyn.analysis.angmom.faceon(h)
# ----------------------------------------------------------------------------------------------------------------------

# units are defined beforehand
# z_rend == z render
# **kwargs for FuncAnimation

def z_span(sim, qty="rho", width=16, z_shift=0.01, z_max=0.25, z_rend=True, vmin=10**5, vmax=10**10, qtytitle=None,
           show_cbar=True, cmap=plt.cm.turbo, title=None, interval=250, **kwargs):
    """

    Animate SPH images of the given simulation as it varies in the z-axis.

    **Keyword arguments:**

    *sim* : The galaxy object containing the data to visualize.

    *qty* (rho): The name of the array to interpolate

    *width* (16 units): The overall width and height of the plot.
    Units are determined by ``sim['pos']``.

    *z_shift* (0.01 units): The amount to shift in the z-direction per frame.
    Units are determined by ``sim['pos']``.

    *z_max* (0.25 units): Maximum z-distance to cover in the animation.
    Units are determined by ``sim['pos']``.

    *z_rend* (True): Whether the animation renders the current z-position.

    *vmin* (10**5 units): Minimum of the visualization scale.
    Units are determined by ``sim['qty']``.

    *vmax* (10**10 units): Maximum of the visualization scale.
    Units are determined by ``sim['qty']``.

    *qtytitle* (None): Colorbar quantity title.

    *show_cbar* (True): Whether to plot the colorbar.

    *cmap* (plt.cm.turbo): Colormap to be used.

    *title* (None): Plot Title.

    *interval* (250 ms): Amount of time between the drawing of frames.
    Does not affect playback speed of animation.

    **Returns:** Animation Object
    """

    # defining z [TO BE MADE ADJUSTABLE]
    z = 0

    # Calculating the number of frames dynamically
    frames = int(z_max / z_shift) + 1  # +1 to account for frame 0

    # Creating Figure and Axes
    fig, ax = plt.subplots()

    # Starting Plot
    galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

    # Customizing Axes

    # Colorbar
    if show_cbar:
        if qtytitle is None:
            cbar = fig.colorbar(galaxy, ax=ax, label=qty)
        else:
            cbar = fig.colorbar(galaxy, ax=ax, label=qtytitle)

    # Title
    if title is not None:
        axtitle = ax.set_title(title)

    # xyLabels
    xlabel = ax.set_xlabel(f"x/{sim['pos'].units}")
    ylabel = ax.set_ylabel(f"y/{sim['pos'].units}")

    # xyLimits
    xlim = ax.set_xlim(-1 * width / 2, width / 2)
    ylim = ax.set_ylim(-1 * width / 2, width / 2)

    # plotText
    if z_rend:
        ptext = fig.text(0.75, 0.05, f'z = {z:.2f} {sim["pos"].units}', transform=ax.transAxes)

    # Defining Update Function
    def update(frame):
        nonlocal galaxy, z
        if frame == 0:  # if initial frame do not shift_z
            return galaxy
        else:
            # shifting z-position of all particles
            sim['pos'][:, 2] -= z_shift

            # Plotting Next Frame
            galaxy.remove()  # Clear the imshow artist to avoid overlapping images
            galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

            # Updating plotText
            z += z_shift
            ptext.set_text(f'z = {z:.2f} kpc')

            return galaxy

    # Initializing the animation
    ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, **kwargs)

    return ani
