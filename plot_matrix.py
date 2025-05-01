
# This program generates a Risk Matrix as a PNG file given the initial Inherent Risk Rating (IR)
# and the Residual Risk Rating (RR).
# The model is based on our 5*5 Risk Matrix.
# license CC
import matplotlib.pyplot as plt
import math
from matplotlib.patches import FancyArrowPatch
# Function to create the risk matrix


def create_risk_matrix(fig, nrows, ncols, colors, risks):
    axes = [fig.add_subplot(nrows, ncols, r * ncols + c + 1) for r in range(nrows) for c in range(ncols)]
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        # 3. Ensure the entire axis is not visible (including tick lines and labels)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # 4. Ensure tick parameters have zero length and no labels
        ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)

        # --- E
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)

    for color, risk_level in zip(colors, risks):
        for idx in color:
            axes[idx].set_facecolor(risk_level[0])
            # Set risk level text to background
            axes[idx].text(2.5, 2.5, risk_level[1], fontweight='bold', fontsize=14.0, ha='center', va='center', zorder=0)
    return axes

# Variables
nrows, ncols = 5, 5
colors = [
    [5, 10, 15, 16, 20, 21, 22],  # Green
    [0, 1, 6, 11, 12, 17, 18, 23],  # Yellow
    [2, 7, 8, 13, 19,24],  # Orange
    [3, 4, 9, 14]  # Red
]
risks = [('green', 'L'), ('yellow', 'M'), ('orange', 'H'), ('red', 'E')]

# Main plot setup
fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0)
plt.xlabel('Impact', fontweight='bold', fontsize=14.0)
plt.ylabel('Likelihood', fontweight='bold', fontsize=14.0)
plt.title('Risk Analysis', fontweight='bold', fontsize=14.0)

axes = create_risk_matrix(fig, nrows, ncols, colors, risks)

# Variables to hold clicked block coordinates
clicks = []

# Click event handler
def onclick(event):
    global clicks
    if event.inaxes:  # Check if the click was inside an axis
        ax_index = axes.index(event.inaxes)
        clicks.append(ax_index)
        if len(clicks) == 2:  # If two clicks are made, draw an arrow
            init, end = clicks
            draw_arrow_between_circles(init, end)
            plt.draw()
            for ax in fig.axes:
                if ax.get_legend() is not None:  # Check if there's a legend first
                    ax.get_legend().remove()

            fig.savefig("arrow_with_annotate.png")
            print(f"Saved figure as 'arrow_with_annotate.png'")

# Function to draw an arrow connecting circle borders



def draw_arrow_between_circles(init, end):
    init_ax = axes[init]
    end_ax = axes[end]
    print(init_ax, end_ax)
    # Get the center of the initial and end axes
    init_center = init_ax.get_position().get_points().mean(axis=0)
    end_center = end_ax.get_position().get_points().mean(axis=0)

    # Define circle radius relative to the square (scaled fraction)
    radius_fraction = 0.05  # Adjust this value based on the size of the circle
    dx, dy = end_center[0] - init_center[0], end_center[1] - init_center[1]
    distance = math.sqrt(dx**2 + dy**2)

    # Calculate start and end points at circle borders
    start_x = init_center[0] + (dx / distance * radius_fraction)
    start_y = init_center[1] + (dy / distance * radius_fraction)
    end_x = end_center[0] - (dx / distance * radius_fraction)
    end_y = end_center[1] - (dy / distance * radius_fraction)
    # Calculate the intermediate point for the two-segment line
    # This point has the x-coordinate of the end and the y-coordinate of the start
    intermediate_point = (init_center[0], end_center[1])
    print("init", init_center)
    print(end_center, intermediate_point)
    if ((end_center[0] == intermediate_point[0]) and
        (end_center[1] == intermediate_point[1])):
        end_ax.annotate("RR", xy=(0.5, 0.30), xycoords="axes fraction", ha="center", va="top",
                        bbox=dict(boxstyle="circle", fc="white"))
        # Create the first segment (vertical line)
        line1 = FancyArrowPatch(posA=init_center, posB=intermediate_point, transform=fig.transFigure,
                                color='blue', arrowstyle='-|>', lw=2,mutation_scale=20)  # No arrow on the first segment
        fig.patches.extend([line1])
    else:
        end_ax.annotate("RR", xy=(0.5, 0.90), xycoords="axes fraction", ha="center", va="top",
                        bbox=dict(boxstyle="circle", fc="white"))
        # Create the first segment (vertical line)
        line1 = FancyArrowPatch(posA=init_center, posB=intermediate_point, transform=fig.transFigure,
                                color='blue', arrowstyle='-', lw=2)  # No arrow on the first segment
        # Create the second segment (horizontal line) with the arrow head
        line2 = FancyArrowPatch(posA=intermediate_point, posB=end_center, transform=fig.transFigure,
                                color='blue', arrowstyle='-|>', lw=2, mutation_scale=20)  # Arrow on the second segment

        # Add both segments to the figure's patches
        fig.patches.extend([line1, line2])
    # Place "IR" and "RR" just below the risk labels
    init_ax.annotate("IR", xy=(0.5, 0.90), xycoords="axes fraction", ha="center", va="top",
                     bbox=dict(boxstyle="circle", fc="white"))


# Connect the click event
fig.canvas.mpl_connect('button_press_event', onclick)

# Display the plot
plt.show()

