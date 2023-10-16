import matplotlib.pyplot as plt
import matplotlib.animation as animation

from speedcoach.reader import SpeedData
from utils import (
    GORINCHEM_BACKGROUND,
    GORINCHEM_BOTTOM,
    GORINCHEM_LEFT,
    GORINCHEM_RIGHT,
    GORINCHEM_TOP,
)


def animate_route(speed_data: SpeedData) -> None:
    gorinchem = plt.imread(GORINCHEM_BACKGROUND)
    figure, axes = plt.subplots()

    axes.imshow(
        gorinchem,
        extent=[GORINCHEM_LEFT, GORINCHEM_RIGHT, GORINCHEM_BOTTOM, GORINCHEM_TOP],
    )
    axes.set_xlim([GORINCHEM_LEFT, GORINCHEM_RIGHT])
    axes.set_ylim([GORINCHEM_BOTTOM, GORINCHEM_TOP])

    longitude_values = speed_data.per_stroke_data.gps_lon
    latitude_values = speed_data.per_stroke_data.gps_lat
    boat_location = axes.scatter(longitude_values[0], latitude_values[0])

    def animate_boat_location(i):
        boat_location.set_offsets((longitude_values[i], latitude_values[i]))
        return (boat_location,)

    boat_animation = animation.FuncAnimation(
        figure,
        animate_boat_location,
        repeat=True,
        frames=len(longitude_values) - 1,
        interval=50,  # We can make interval function of data to show realtime animation
    )
    print("Print this to avoid formatters removing variable: ", boat_animation)

    plt.show()
