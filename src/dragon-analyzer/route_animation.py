from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib as mpl
from svgpathtools import svg2paths
from svgpath2mpl import parse_path


from speedcoach.reader import SpeedData
from utils import (
    GORINCHEM_BACKGROUND,
    GORINCHEM_BOTTOM,
    GORINCHEM_LEFT,
    GORINCHEM_RIGHT,
    GORINCHEM_TOP,
)


def create_boat_marker() -> Path:
    _, attributes = svg2paths("./src/data/Dragon_boat.svg")
    boat_marker = parse_path(attributes[0]["d"])
    boat_marker.vertices -= boat_marker.vertices.mean(axis=0)
    boat_marker = boat_marker.transformed(mpl.transforms.Affine2D().rotate_deg(180))
    # Make boat face other direction
    # boat_marker = boat_marker.transformed(mpl.transforms.Affine2D().scale(-1,1))
    return boat_marker


def animate_route(speed_data: SpeedData) -> None:
    gorinchem = plt.imread(GORINCHEM_BACKGROUND)
    figure, ax = plt.subplots()

    # Set background
    ax.imshow(
        gorinchem,
        extent=[GORINCHEM_LEFT, GORINCHEM_RIGHT, GORINCHEM_BOTTOM, GORINCHEM_TOP],
    )
    ax.set_xlim([GORINCHEM_LEFT, GORINCHEM_RIGHT])
    ax.set_ylim([GORINCHEM_BOTTOM, GORINCHEM_TOP])

    # Set boat animation
    longitude_values = speed_data.per_stroke_data.gps_lon
    latitude_values = speed_data.per_stroke_data.gps_lat
    boat_location = ax.scatter(
        longitude_values[0], latitude_values[0], marker=create_boat_marker(), s=700
    )

    def animate_boat_location(i):
        boat_location.set_offsets((longitude_values[i], latitude_values[i]))
        return boat_location

    # Animate
    boat_animation = animation.FuncAnimation(
        figure,
        animate_boat_location,
        repeat=True,
        frames=len(longitude_values) - 1,
        interval=50,  # We can make interval function of data to show realtime animation
    )
    print("Print this to avoid formatters removing variable: ", boat_animation)
    plt.show()
