from matplotlib import animation
from route_animation import animate_route
from speedcoach.reader import SpeedData
import matplotlib.pyplot as plt


def plot_speed_data(speed_data: SpeedData) -> None:
    fig, axs = plt.subplots(2, 2)
    plot_0_0 = animate_route(speed_data, fig, axs[0,0])

    plot_1_0 = line_plot(
        fig=fig,
        ax=axs[1,0],
        x=speed_data.per_stroke_data.strokes,
        y=speed_data.per_stroke_data.speed,
        title="Speed (km/h)",
        animated=True)
    plot_0_1 = line_plot(
        fig=fig,
        ax=axs[0,1],
        x=[t.seconds for t in speed_data.per_stroke_data.elapsed_time],
        y=speed_data.per_stroke_data.stroke_rate,
        title="Stroke rate",
        animated=True)
    plot_1_1 = line_plot(
        fig=fig,
        ax=axs[1,1],
        x=[t.seconds for t in speed_data.per_stroke_data.elapsed_time],
        y=speed_data.per_stroke_data.cal_per_hour,
        title="Cal. per hour",
    )

    plt.show()


def line_plot(fig, ax, x, y, title=None, animated=False):
    ax.plot(x, y)
    ax.set_title(title)
    if animated:
        animated_marker = ax.scatter(x,y)

        def animate_line(i):
            animated_marker.set_offsets((x[i], y[i]))
            return animated_marker
        
        return animation.FuncAnimation(
            fig, animate_line, repeat=True, frames=len(x) - 1, interval=50,
        )
